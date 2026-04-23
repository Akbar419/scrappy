import os
import requests
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__)

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

@app.route("/")
def index():
    import os
    base_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(base_dir, "scrappy.html"), encoding="utf-8") as f:
        return f.read()

@app.route("/api/chat", methods=["POST"])
def chat():
    if not GEMINI_API_KEY:
        return jsonify({"error": "API key not set"}), 500

    data = request.get_json()
    prompt = data.get("prompt", "")

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
    payload = {"contents": [{"parts": [{"text": prompt}]}]}

    resp = requests.post(url, json=payload)
    result = resp.json()
    text = result.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")

    return jsonify({"text": text})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
