import os
from dotenv import load_dotenv
import requests
from src.core.utils import encode_video_to_base64

load_dotenv()
API_KEY_REF = os.getenv("API_KEY_REF")

url = "https://openrouter.ai/api/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {API_KEY_REF}",
    "Content-Type": "application/json"
}

def prompt_video_analysis(video_path: str, prompt_text: str) -> list:
	prompt = [{
			"role": "user",
			"content": [
				{
					"type": "text",
					"text": prompt_text
				},
				{
					"type": "video_url",
					"video_url": {
						"url": video_path
					}
				}
			]
		}]
	return prompt

def process_video(job, prompt_text: str) -> dict:
	job_id = job["job_id"]
	video_path = job["video_path"]
	print(f"Processing video for job {job_id} at path {video_path}")
	base64_video = encode_video_to_base64(video_path)
	video = f"data:video/mp4;base64,{base64_video}"
	prompt = prompt_video_analysis(video, prompt_text)
	payload = {
		"model": "nvidia/nemotron-nano-12b-v2-vl:free",
		"messages": prompt
	}
	response = requests.post(url, headers=headers, json=payload)
	return response.json()
