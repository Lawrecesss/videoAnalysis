import os
from fastapi import FastAPI, UploadFile, File, HTTPException, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request

from src.services.websocket import websocket_result_handler
from src.core.client import upload_video

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

app = FastAPI()

templates = Jinja2Templates(
    directory=os.path.join(BASE_DIR, "templates")
)

TMP_ROOT = "./tmp"
os.makedirs(TMP_ROOT, exist_ok=True)

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        "upload.html",
        {"request": request}
    )

@app.post("/upload")
async def upload(video: UploadFile = File(...)):
    if not video:
        raise HTTPException(status_code=400, detail="No video uploaded")

    job_id = await upload_video(video)

    return {
        "job_id": job_id,
        "status": "queued"
    }

@app.websocket("/result/{job_id}")
async def websocket_endpoint(websocket: WebSocket, job_id: str):
    await websocket_result_handler(websocket, job_id)
    
