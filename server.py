from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import openai
import os

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
