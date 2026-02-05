import base64
import os
import tempfile
from redis import Redis
import json

TMP_ROOT = os.path.join(tempfile.gettempdir(), "video_uploads")

def encode_video_to_base64(video_path: str) -> str:
    with open(video_path, "rb") as video_file:
        return base64.b64encode(video_file.read()).decode('utf-8')

def enqueue_video_for_processing(job_id: str) -> None:
	redis_client = Redis(
    host=os.getenv("REDIS_HOST"),
    port=int(os.getenv("REDIS_PORT")),
    password=os.getenv("REDIS_PASSWORD"),
    decode_responses=True,
    ssl=True,
    ssl_cert_reqs=None
    )
	job = {
		"job_id": job_id,
		"video_path": f"{TMP_ROOT}/{job_id}/input.mp4"
	}
	redis_client.rpush('video_jobs', json.dumps(job))
