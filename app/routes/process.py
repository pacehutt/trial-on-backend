from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from app.services.image_processor import apply_design_to_clothing
from app.utils.io_utils      import read_image
import io, cv2

router = APIRouter()

@router.post("/apply-design/")
async def apply_design(
    person_image: UploadFile = File(...),
    design_image: UploadFile = File(...)
):
    frame  = read_image(person_image)
    design = read_image(design_image)

    result = apply_design_to_clothing(frame, design)
    if result is None:
        raise HTTPException(400, "Could not detect clothing region.")

    _, buf = cv2.imencode(".png", result)
    return StreamingResponse(io.BytesIO(buf.tobytes()), media_type="image/png")
