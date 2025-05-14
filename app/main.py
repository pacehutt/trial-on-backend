from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import process


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins. Replace with specific domains for better security.
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods.
    allow_headers=["*"],  # Allows all headers.
)

app.include_router(process.router, prefix="/api", tags=["Processing"])
