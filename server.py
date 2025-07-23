from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from openai import OpenAI
import os

app = Flask(__name__)
CORS(app)
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/respond", methods=["POST"])
def respond():
    try:
        user_text = request.json["message"]

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a supportive, calming, and empathetic AI therapist. "
                        "Speak in a warm and understanding tone, like a trusted friend who genuinely listens. "
                        "Give thoughtful, detailed, and emotionally intelligent responses. "
                        "Avoid generic advice. Reflect on what the user says and help them feel heard and validated. "
                        "Always be encouraging, never judgmental. If they sound unsure or emotional, gently reassure them."
                    )
                },
                {"role": "user", "content": user_text}
            ]
        )

        reply = response.choices[0].message.content
        return jsonify({"reply": reply})

    except Exception as e:
        print(" Error with OpenAI:", e)
        return jsonify({"error": "Therapist bot is having a moment "}), 500

@app.route("/")
def home():
    return "TheraBot is running!"

if __name__ == "__main__":
    app.run(debug=True)
