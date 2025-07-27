from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route("/receive_gpt_description", methods=["POST"])
def receive_gpt_description():
    data = request.json
    description = data.get("description")

    if description:
        print("📨 Description reçue :", description)
        return jsonify({
            "status": "received",
            "message": "Description bien reçue par le serveur.",
            "description": description
        })
    else:
        return jsonify({
            "status": "error",
            "message": "Aucune description reçue."
        }), 400

# Pour Render : expose bien le port attendu
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
