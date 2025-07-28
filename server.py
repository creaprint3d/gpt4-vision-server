import os
from flask import Flask, request, jsonify

app = Flask(__name__)
last_description = ""  # Variable globale

@app.route('/receive_gpt_description', methods=['POST'])
def receive_description():
    global last_description
    data = request.json
    description = data.get("description", "")
    print("📩 Description reçue du script local :\n", description)
    last_description = description
    return jsonify({"status": "success", "message": "Description reçue"}), 200

@app.route('/get_last_description', methods=['GET'])
def get_last_description():
    return jsonify({"description": last_description}), 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Récupère le port utilisé par Render
    app.run(host='0.0.0.0', port=port)
