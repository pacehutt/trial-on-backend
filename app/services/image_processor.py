import numpy as np
import cv2

color_ranges = {
    "red": [(np.array([0, 120, 70]), np.array([10, 255, 255])),
            (np.array([170, 120, 70]), np.array([180, 255, 255]))],
    "green": [(np.array([25, 52, 72]), np.array([102, 255, 255]))],
    "blue": [(np.array([100, 150, 50]), np.array([140, 255, 255]))],
    "yellow": [(np.array([20, 100, 100]), np.array([30, 255, 255]))],
    "black": [(np.array([0, 0, 0]), np.array([180, 255, 50]))],
    "white": [(np.array([0, 0, 200]), np.array([180, 55, 255]))]
}

def apply_design_to_clothing(frame, design):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    detected_color = None
    mask_white = None

    for color, ranges in color_ranges.items():
        mask = None
        for lower, upper in ranges:
            if mask is None:
                mask = cv2.inRange(hsv, lower, upper)
            else:
                mask = cv2.bitwise_or(mask, cv2.inRange(hsv, lower, upper))

        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=2)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=2)

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            mask = np.zeros_like(mask)
            cv2.drawContours(mask, [largest_contour], -1, (255), thickness=cv2.FILLED)

        if np.sum(mask) > 500000:
            detected_color = color
            mask_white = mask
            break

    if detected_color is None or mask_white is None:
        return None

    mask_black = cv2.bitwise_not(mask_white)

    mask_black_3CH = cv2.merge([mask_black]*3)
    mask_white_3CH = cv2.merge([mask_white]*3)

    tshirt_area = cv2.bitwise_and(frame, mask_black_3CH)

    design = cv2.resize(design, (frame.shape[1], frame.shape[0]))
    design_masked = cv2.bitwise_and(design, mask_white_3CH)

    final_output = cv2.addWeighted(tshirt_area, 1, design_masked, 1, 0)
    return final_output
