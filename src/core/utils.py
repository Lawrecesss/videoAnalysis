import base64
from redis import Redis
import json

def encode_video_to_base64(video_path: str) -> str:
    with open(video_path, "rb") as video_file:
        return base64.b64encode(video_file.read()).decode('utf-8')

def enqueue_video_for_processing(job_id: str) -> None:
	redis_client = Redis(host='localhost', port=6379, db=0, decode_responses=True)
	job = {
		"job_id": job_id,
		"video_path": f"./tmp/{job_id}/input.mp4"
	}
	redis_client.rpush('video_jobs', json.dumps(job))
