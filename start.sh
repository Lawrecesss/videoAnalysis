# Start worker in background
python3 -u -m src.services.worker &

# Start FastAPI web service
uvicorn src.api.app:app --host 0.0.0.0 --port $PORT
