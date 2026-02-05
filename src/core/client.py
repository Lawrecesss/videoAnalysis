import os
import uuid
from fastapi import UploadFile
from src.core.utils import enqueue_video_for_processing

TMP_ROOT = "./tmp"
os.makedirs(TMP_ROOT, exist_ok=True)

async def upload_video(file: UploadFile) -> str:
    job_id = str(uuid.uuid4())

    job_dir = os.path.join(TMP_ROOT, job_id)
    os.makedirs(job_dir, exist_ok=True)

    video_path = os.path.join(job_dir, "input.mp4")

    await file.seek(0)

    with open(video_path, "wb") as f:
        while True:
            chunk = await file.read(8192)
            if not chunk:
                break
            f.write(chunk)

    enqueue_video_for_processing(job_id)

    return job_id
