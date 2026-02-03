import os
from fastapi import WebSocket
from redis import Redis
import json
import asyncio
import ssl

redis_client = Redis(
    host=os.getenv("REDIS_HOST"),
    port=int(os.getenv("REDIS_PORT")),
    password=os.getenv("REDIS_PASSWORD"),
    decode_responses=True,
    ssl=True,
    ssl_cert_reqs=None
    )

async def websocket_result_handler(websocket: WebSocket, job_id: str) -> None:
    await websocket.accept()

	# Check if result already exists in case job completed before websocket connection
    existing = redis_client.get(f"vlm_result:{job_id}")
    if existing:
        await websocket.send_json(json.loads(existing))
        await websocket.close()
        return

	# Subscribe to Redis channel for real-time updates
    pubsub = redis_client.pubsub()
    pubsub.subscribe(f"vlm_channel:{job_id}")

    try:
        while True:
            # Listen for new messages
            message = pubsub.get_message(ignore_subscribe_messages=True)

            if message:
                await websocket.send_json(json.loads(message["data"]))
                break
			# Avoid busy waiting
            await asyncio.sleep(0.1)

    finally:
        pubsub.close()
        await websocket.close()

