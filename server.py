from flask import Flask, request, jsonify

app = Flask(__name__)
last_description = ""  # Variable globale pour stocker la dernière description reçue

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
    app.run(debug=True, port=10000)
