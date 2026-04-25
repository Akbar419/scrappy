import os
import re
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

@app.route("/")
def index():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(base_dir, "landing.html"), encoding="utf-8") as f:
        return f.read()

@app.route("/app")
def app_page():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(base_dir, "scrappy.html"), encoding="utf-8") as f:
        return f.read()

@app.route("/api/chat", methods=["POST"])
def chat():
    if not GROQ_API_KEY:
        return jsonify({"error": "API key not set"}), 500

    data = request.get_json()
    prompt = data.get("prompt", "")

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 1000
    }

    resp = requests.post(url, json=payload, headers=headers)
    result = resp.json()

    raw = result.get("choices", [{}])[0].get("message", {}).get("content", "")
    cleaned = re.sub(r"```(?:json)?", "", raw).strip()

    return jsonify({"text": cleaned})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
