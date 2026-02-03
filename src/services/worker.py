import json
import os
import threading
from redis import Redis
from src.core.model import process_video
import ssl

def worker():
    redis_client = Redis(
    host=os.getenv("REDIS_HOST"),
    port=int(os.getenv("REDIS_PORT")),
    password=os.getenv("REDIS_PASSWORD"),
    decode_responses=True,
    ssl=True,
    ssl_cert_reqs=None
    )
    print(f"Worker started PID={os.getpid()}", flush=True)

    while True:
        try:
            job_data = redis_client.blpop('video_jobs', timeout=5)
            if not job_data:
                continue

            _, job_json = job_data
            job = json.loads(job_json)
            job_id = job["job_id"]

            result = process_video(job, "Categorize the content of the video")

            # Store result in Redis
            redis_client.set(f"vlm_result:{job_id}", json.dumps(result))

            # Publish result to websocket channel
            redis_client.publish(f"vlm_channel:{job_id}", json.dumps(result))

            print(f"Completed job {job_id}", flush=True)

        except Exception as e:
            # Use fallback job_id if exists, else log general error
            try:
                redis_client.set(f"vlm_error:{job_id}", str(e))
            except NameError:
                print(f"Worker error before job_id was set: {e}", flush=True)


def start_workers(num_workers=4):
    threads = []
    for _ in range(num_workers):
        t = threading.Thread(target=worker)
        t.daemon = True  # Daemon so threads exit when main process exits
        t.start()
        threads.append(t)
    for t in threads:
        t.join()

if __name__ == "__main__":
    start_workers()
