from flask import Flask, request, jsonify
from deepface import DeepFace

app = Flask(__name__)

# C:\Users\hp\Desktop\freelance\my_scripts\therapist_bot\FYP2\static\temp.jpg


@app.route('/')
def home():
    return "DeepFace API is running. Use the /analyze endpoint to analyze images.", 200


@app.route('/analyze', methods=['POST'])
def analyze_image():
    try:
        data = request.get_json()
        img_path = data.get('img_path')

        if not img_path:
            return jsonify({'error': 'No img_path provided'}), 400

        # Analyze the image
        result = DeepFace.analyze(img_path=img_path, actions=['emotion'])
        emotion = result[0]['dominant_emotion']

        return jsonify({'dominant_emotion': emotion}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    # Running on port 5001 to avoid conflicts with App1
    app.run(port=5001, debug=True)
