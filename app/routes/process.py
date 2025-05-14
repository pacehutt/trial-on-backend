from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from app.services.image_processor import apply_design_to_clothing
from app.utils.io_utils import read_image
import io
import cv2

router = APIRouter()

@router.post("/apply-design/")
async def apply_design(
    person_image: UploadFile = File(...),
    design_image: UploadFile = File(...)
):
    frame = read_image(person_image)
    design = read_image(design_image)

    final_output = apply_design_to_clothing(frame, design)

    if final_output is None:
        raise HTTPException(status_code=400, detail="No prominent clothing color detected.")

    _, encoded_img = cv2.imencode(".png", final_output)
    return StreamingResponse(io.BytesIO(encoded_img.tobytes()), media_type="image/png")
