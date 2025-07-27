import base64
import io
from flask import Flask, request, jsonify
from PIL import Image
import openai

# === CONFIGURATION ===
openai.api_key = "sk-P3mdbWLcTmbVYiHvtli5Pejo2gsaVVDZD7kHYEMB_0T3BlbkFJAHeXlhwJuC1ry05XqtEPog5T2fGRyMJN_X9lqxO-kA"
MODEL = "gpt-4o"  # modèle GPT avec vision

app = Flask(__name__)

@app.route("/camera_vision_report", methods=["POST"])
def camera_vision_report():
    try:
        data = request.get_json()

        if not data or "image_base64" not in data:
            return jsonify({"error": "image_base64 is required"}), 400

        image_base64 = data["image_base64"]
        image_bytes = base64.b64decode(image_base64)

        result = openai.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Décris précisément cette image et ce que la caméra voit, en analysant l’environnement et les émotions si possible."},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_base64}"
                            }
                        }
                    ],
                }
            ],
            max_tokens=400,
        )

        description = result.choices[0].message.content
        print("📸 Résultat :", description)
        return jsonify({"camera_description": description})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# === Lancement serveur ===
if __name__ == "__main__":
    app.run(debug=True)
