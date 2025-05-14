import numpy as np
import cv2
from fastapi import UploadFile

def read_image(upload_file: UploadFile):
    content = upload_file.file.read()
    nparr = np.frombuffer(content, np.uint8)
    return cv2.imdecode(nparr, cv2.IMREAD_COLOR)
