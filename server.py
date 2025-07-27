from flask import Flask, request, jsonify
import base64
import io
from PIL import Image
import openai
import os

app = Flask(__name__)

# 🔐 Clé API OpenAI
openai.api_key = "sk-...TA_CLÉ_IA..."

@app.route("/camera_vision_report", methods=["POST"])
def camera_vision_report():
    data = request.get_json()

    if not data or "description" not in data:
        return jsonify({"error": "Missing 'description' field."}), 400

    description = data["description"]
    print("📸 Description reçue :", description)

    # → Ici tu pourrais faire quelque chose avec GPT ou un autre traitement

    return jsonify({
        "message": "✅ Description reçue avec succès.",
        "received_description": description
    })

# Pour le test : route GET simple
@app.route("/", methods=["GET"])
def index():
    return "✅ Serveur en ligne. Utilise POST /camera_vision_report"

# Exécute l’app Flask sur le bon port (pour Render)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=True)
