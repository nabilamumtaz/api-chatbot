from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# ✅ JWT Token dari Local Storage
JWT_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjM1OWM3MjMwLTBkZDEtNDVmZC05NTcxLTc4OGVhZWRkZmEzMSJ9.m6tfgIoXnHft6yqySA_HkRFTJc5VdcS-coC_QFCbHpM"

# ✅ URL API Open Web UI
OPEN_WEB_UI_API = "http://localhost:3000/api/chat/completions"

# ✅ Model yang tersedia (Cek dari `/api/models`)
MODEL_NAME = "qwen2.5:7b" 
@app.route("/")
def home():
    return jsonify({"message": "Chatbot API Flask is running!"})

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")

    # 🔹 Cek jika pesan kosong
    if not user_message:
        return jsonify({"error": "Pesan tidak boleh kosong"}), 400

    try:
        # 🔹 Kirim request ke Open Web UI API
        response = requests.post(
            OPEN_WEB_UI_API,
            json={
                "model": MODEL_NAME,  # ✅ Gunakan model yang tersedia
                "messages": [{"role": "user", "content": user_message}]
            },
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {JWT_TOKEN}"  # Gunakan JWT Token
            }
        )

        # 🔹 Tangani response dari API
        if response.status_code == 200:
            bot_reply = response.json().get("choices", [{}])[0].get("message", {}).get("content", "Maaf, tidak ada respons.")
            return jsonify({"reply": bot_reply})
        else:
            return jsonify({"error": f"Error dari Open Web UI: {response.status_code}, {response.text}"}), response.status_code

    except Exception as e:
        return jsonify({"error": f"Gagal menghubungi API Open Web UI: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)  # Bisa diakses dari luar juga
