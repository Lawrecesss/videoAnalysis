import json
import os
from multiprocessing import Process
from redis import Redis
from src.core.model import process_video

def worker():
    redis_client = Redis(host='localhost', port=6379, db=0, decode_responses=True)
    print(f"Worker started PID={os.getpid()}", flush=True)

    while True:
        job_data = redis_client.blpop('video_jobs', timeout=5)
        if not job_data:
            continue

        _, job_json = job_data
        job = json.loads(job_json)
        job_id = job["job_id"]

        try:
            result = process_video(job, "Categorize the content of the video")
            redis_client.set(
                f"vlm_result:{job_id}",
                json.dumps(result)
            )
            print(f"Completed job {job_id}", flush=True)

        except Exception as e:
            redis_client.set(
                f"vlm_error:{job_id}",
                str(e)
            )
            print(f"Failed job {job_id}: {e}", flush=True)

def multi_process_worker(num_workers):
    processes = []
    for _ in range(num_workers):
        p = Process(target=worker)
        p.daemon = False
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

if __name__ == "__main__":
    multi_process_worker(num_workers=4)
