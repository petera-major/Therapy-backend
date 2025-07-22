from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import openai
import os
import requests
import time

app = Flask(__name__)       
CORS(app)  
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/respond", methods=["POST"])
def respond():
    user_text = request.json["message"]
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You're a friendly and calming AI therapist."},
            {"role": "user", "content": user_text}
        ]
    )
    reply = response["choices"][0]["message"]["content"]
    return jsonify({"reply": reply})

@app.route("/video-response", methods=["POST"])
def video_response():
    user_text = request.json["message"]

    payload = {
        "avatar_id": "d3e10d9e9af54911afb9fa6e3d546565",
        "script": {
            "type": "text",
            "input": user_text
        },
        "voice_id": "QcORZQeJrCddkWN0ZHla",  
        "test": False
    }

    headers = {
        "Authorization": f"Bearer {os.getenv('HEYGEN_API_KEY')}",
        "Content-Type": "application/json"
    }

    response = requests.post("https://api.heygen.com/v1/video.create", json=payload, headers=headers)
    data = response.json()

    if "data" not in data or "video_id" not in data["data"]:
        return jsonify({"error": "HeyGen video creation failed"}), 500

    video_id = data["data"]["video_id"]

    # Step 2: Poll for video status
    status_url = f"https://api.heygen.com/v1/video.status?video_id={video_id}"
    video_url = None

    for _ in range(20):  # Try for ~60 seconds
        time.sleep(3)
        status_res = requests.get(status_url, headers=headers)
        status_data = status_res.json()

        if status_data["data"]["status"] == "done":
            video_url = status_data["data"]["video_url"]
            break
        elif status_data["data"]["status"] == "error":
            return jsonify({"error": "HeyGen video generation failed"}), 500

    if video_url:
        return jsonify({"videoUrl": video_url})
    else:
        return jsonify({"error": "Timed out waiting for video"}), 504
