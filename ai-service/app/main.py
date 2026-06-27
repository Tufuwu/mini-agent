import sys
from pathlib import Path

from fastapi import FastAPI

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.api.chat import router as chat_router

app = FastAPI()
app.include_router(chat_router)

@app.get("/")
def root():
    return {"message": "Hello FastAPI"}
