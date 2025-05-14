import cv2
import numpy as np
from .segmentation import segment_person

# (keep your existing color_ranges here…)

def apply_design_to_clothing(frame: np.ndarray, design: np.ndarray) -> np.ndarray:
    # 1) Get a person mask
    person_mask = segment_person(frame)

    # 2) (Optional) intersect with a color range if you still need color filtering
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # e.g. green shirt only
    lower, upper = np.array([25,52,72]), np.array([102,255,255])
    color_mask = cv2.inRange(hsv, lower, upper)

    # Combine masks: you could OR all colors, but AND with the person region
    clothing_mask = cv2.bitwise_and(person_mask, color_mask)

    # 3) Clean up mask
    kernel = np.ones((5,5), np.uint8)
    clothing_mask = cv2.morphologyEx(clothing_mask, cv2.MORPH_CLOSE, kernel, iterations=2)
    clothing_mask = cv2.morphologyEx(clothing_mask, cv2.MORPH_OPEN,  kernel, iterations=2)

    # 4) Create 3‑channel mask
    mask_3ch = cv2.merge([clothing_mask]*3)
    inv_mask = cv2.bitwise_not(clothing_mask)
    inv_3ch  = cv2.merge([inv_mask]*3)

    # 5) Carve out original shirt region
    bg = cv2.bitwise_and(frame, inv_3ch)

    # 6) Resize design to full image, then carve it to clothing region
    design_resized = cv2.resize(design, (frame.shape[1], frame.shape[0]))
    fg = cv2.bitwise_and(design_resized, mask_3ch)

    # 7) Blend
    return cv2.addWeighted(bg, 1.0, fg, 1.0, 0)
