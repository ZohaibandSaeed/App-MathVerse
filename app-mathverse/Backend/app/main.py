from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

from app.api.routes import router

app = FastAPI(title="Mathly AI Backend")

# Add CORS Middleware so React Frontend can talk to this Backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://appmathverse.netlify.app",
        "http://localhost:5173", # For local Vite development
        "http://localhost:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the API router
app.include_router(router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Mathly AI API Backend!"}
