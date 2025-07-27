from flask import Flask, request, jsonify

app = Flask(__name__)

# Variable globale pour stocker la dernière description reçue
description_from_webcam = "Aucune donnée reçue."

@app.route("/camera_vision_report", methods=["GET"])
def get_description():
    return jsonify({"description": description_from_webcam})

@app.route("/update_description", methods=["POST"])
def update_description():
    global description_from_webcam
    data = request.get_json()
    description_from_webcam = data.get("description", "Donnée manquante.")
    return jsonify({"message": "Description mise à jour."})

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
