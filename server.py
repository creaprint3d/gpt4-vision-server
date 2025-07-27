# server.py
from flask import Flask, request, jsonify
import base64
import io
from PIL import Image
import openai
import os

app = Flask(__name__)

# === Configuration ===
OPENAI_API_KEY = "sk-P3mdbWLcTmbVYiHvtli5Pejo2gsaVVDZD7kHYEMB_0T3BlbkFJAHeXlhwJuC1ry05XqtEPog5T2fGRyMJN_X9lqxO-kA"
openai.api_key = OPENAI_API_KEY

# === Route principale attendue par Convai ===
@app.route('/camera_vision_report', methods=['POST'])
def camera_vision_report():
    try:
        data = request.get_json()
        image_base64 = data.get("image")

        if not image_base64:
            return jsonify({"error": "Aucune image fournie."}), 400

        # Decode base64 image
        image_bytes = base64.b64decode(image_base64)
        image = Image.open(io.BytesIO(image_bytes))

        # Appel GPT-4o
        print("🧠 Analyse de l'image avec GPT-4o...")
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Tu es un assistant qui décrit précisément ce qu’il voit sur une image, y compris l’émotion si un visage est visible."},
                {"role": "user", "content": [
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}}
                ]}
            ],
            max_tokens=300
        )

        result = response.choices[0].message.content
        print("✅ Description :", result)

        return jsonify({"description": result})

    except Exception as e:
        print("❌ Erreur :", str(e))
        return jsonify({"error": str(e)}), 500


@app.route('/', methods=['GET'])
def home():
    return "OK: serveur en ligne"

# === Lancer le serveur localement ===
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
