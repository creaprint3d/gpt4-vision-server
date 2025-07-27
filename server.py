from flask import Flask, request, jsonify
import cv2
import base64
import requests
import openai
import os

# === CONFIG ===
convai_character_id = "09d3029c-2e6f-11ef-a9c5-42010a7be00e"
convai_api_key = "7b148d49ac82ee6f8dc76b5672c00977"
openai.api_key = "sk-P3mdbWLcTmbVYiHvtli5Pejo2gsaVVDZD7kHYEMB_0T3BlbkFJAHeXlhwJuC1ry05XqtEPog5T2fGRyMJN_X9lqxO-kA"
MODEL_NAME = "gpt-4o"

app = Flask(__name__)

def capture_image():
    cam = cv2.VideoCapture(0)
    ret, frame = cam.read()
    cam.release()
    if not ret:
        return None
    _, buffer = cv2.imencode('.jpg', frame)
    return base64.b64encode(buffer).decode('utf-8')

def send_to_gpt4_vision(image_b64):
    response = openai.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": "Tu es un assistant qui décrit précisément ce que la caméra voit, y compris les émotions si visibles."
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_b64}"
                        }
                    }
                ]
            }
        ],
        max_tokens=300
    )
    return response.choices[0].message.content

def send_to_convai(description):
    url = f"https://api.convai.com/character/getResponse"
    payload = {
        "character_id": convai_character_id,
        "user_input": f"Analyse caméra : {description}",
        "voice_enabled": False
    }
    headers = {
        "Authorization": f"Bearer {convai_api_key}",
        "Content-Type": "application/json"
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()

@app.route("/camera_vision_report", methods=["POST"])
def camera_vision_report():
    try:
        print("📸 Capture image...")
        image_b64 = capture_image()
        if not image_b64:
            return jsonify({"error": "Échec capture webcam"}), 500

        print("🧠 Analyse par GPT-4 Vision...")
        description = send_to_gpt4_vision(image_b64)
        print("📝 Résultat :", description)

        print("🎯 Envoi à Convai...")
        convai_response = send_to_convai(description)

        return jsonify({
            "description": description,
            "convai_reply": convai_response
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
