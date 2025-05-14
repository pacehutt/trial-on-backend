import torch
import numpy as np
import cv2
from torchvision import models, transforms

# 1) Load once at import time
model = models.segmentation.deeplabv3_resnet101(pretrained=True).eval()

# 2) Preprocessing pipeline
preprocess = transforms.Compose([
    transforms.ToPILImage(),
    transforms.Resize((520, 520)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225]),
])

def segment_person(frame: np.ndarray) -> np.ndarray:
    """
    Returns a binary mask (0/255) of the person class.
    Later you can fine-tune or swap for a clothing-specific model.
    """
    h, w = frame.shape[:2]
    inp = preprocess(frame).unsqueeze(0)         # [1,3,520,520]
    with torch.no_grad():
        out = model(inp)['out'][0]              # [C, H, W]
    mask  = out.argmax(0).byte().cpu().numpy()   # [H, W]
    # Resize back to original size and threshold on the “person” index (15)
    mask = cv2.resize(mask.astype(np.uint8), (w, h), interpolation=cv2.INTER_NEAREST)
    return (mask == 15).astype(np.uint8) * 255    # 255 where person

