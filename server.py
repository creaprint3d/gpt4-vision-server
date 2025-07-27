import os
import base64
import io
from flask import Flask, request, jsonify
from PIL import Image
import openai

app = Flask(__name__)

# === Config ===
openai.api_key = "sk-P3mdbWLcTmbVYiHvtli5Pejo2gsaVVDZD7kHYEMB_0T3BlbkFJAHeXlhwJuC1ry05XqtEPog5T2fGRyMJN_X9lqxO-kA"
model = "gpt-4o"  # ou "gpt-4-turbo" sans image

@app.route("/camera_vision_report", methods=["POST"])
def camera_vision_report():
    try:
        data = request.get_json()
        image_b64 = data.get("image")
        if not image_b64:
            return jsonify({"error": "No image provided"}), 400

        # Décodage image
        image_bytes = base64.b64decode(image_b64)
        image = Image.open(io.BytesIO(image_bytes))

        # Envoi à GPT
        response = openai.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Décris précisément ce que tu vois sur cette image."},
                        {"type": "image_url", "image_url": {"url": "data:image/jpeg;base64," + image_b64}}
                    ]
                }
            ],
            max_tokens=300
        )

        result = response.choices[0].message.content
        return jsonify({"description": result})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# === Lancer le serveur sur le bon port ===
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
