import os
import uuid
from redis import Redis
from src.core.utils import enqueue_video_for_processing
import json

TMP_ROOT = "./tmp"
os.makedirs(TMP_ROOT, exist_ok=True)

def upload_video(file):
    job_id = str(uuid.uuid4())
    job_dir = os.path.join(TMP_ROOT, job_id)
    os.makedirs(job_dir)

    video_path = os.path.join(job_dir, "input.mp4")
    with open(video_path, "wb") as f:
        while True:
            chunk = file.read(8192)
            if not chunk:
                break
            f.write(chunk)

    enqueue_video_for_processing(job_id)
    return job_id

def get_result(job_id):
	r = Redis(decode_responses=True)
	data = r.get(f"vlm_result:{job_id}")
	return json.loads(data) if data else None
