from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/receive_gpt_description', methods=['POST'])
def receive_gpt_description():
    try:
        data = request.get_json()
        description = data.get('description', 'Aucune description reçue.')
        print("📩 Description reçue du script local :")
        print(description)
        return jsonify({
            "status": "success",
            "message": "Description reçue avec succès",
            "description": description
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

# Port automatique pour Render
if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port, debug=True)
