from fastapi import FastAPI
from app.routes import process


app = FastAPI()

app.include_router(process.router, prefix="/api", tags=["Processing"])
