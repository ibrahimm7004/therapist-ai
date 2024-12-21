from flask import Flask, render_template, request, jsonify, url_for
import os
import requests
from chatbot import give_analysis, chat_with_model, chat_history
from utils import plot_emotion_graph, upload_to_s3

app = Flask(__name__)

# Ensure the static directory exists
os.makedirs(os.path.join(app.root_path, 'static'), exist_ok=True)

# Global list to store detected emotions
emotion_results = []


@app.route('/')
def screen1():
    return render_template('screen1.html')


@app.route('/screen2')
def screen2():
    return render_template('screen2.html')


@app.route('/screen3')
def screen3():
    return render_template('screen3.html')


@app.route('/screen4')
def screen4():
    print("Debugging: Entered /screen4 route")

    # Log the current emotion results
    print("Emotion Results:", emotion_results)

    # Generate the analysis using the chat history and emotions
    try:
        analysis = give_analysis(chat_history, emotion_results)
        print("Analysis Output:", analysis)  # Debugging: log the analysis output
    except Exception as e:
        analysis = f"Error generating analysis: {e}"
        print("Error in analysis generation:", e)

    # Generate the line graph
    try:
        graph_filename = plot_emotion_graph(emotion_results, os.path.join(app.root_path, 'static'))
        graph_url = url_for('static', filename=graph_filename) if graph_filename else None
        print("Graph URL:", graph_url)  # Debugging: log the graph URL
    except Exception as e:
        graph_url = None
        print("Error generating graph:", e)

    return render_template('screen4.html', analysis=analysis, graph_url=graph_url)



@app.route('/save_image', methods=['POST'])
def save_image():
    image = request.files['image']
    temp_path = os.path.join(app.root_path, 'static', 'temp.jpg')
    image.save(temp_path)

    try:
        # Upload image to S3 and get the object URL
        object_url = upload_to_s3(temp_path, os.getenv("BUCKET_NAME"))

        if not object_url:
            print("Failed to upload image to S3.")
            return '', 500

        # Call the DeepFace API with the object URL
        api_url = "https://deepface-api-call.onrender.com/analyze"
        payload = {'img_path': object_url}
        response = requests.post(api_url, json=payload)

        if response.status_code == 200:
            emotion = response.json().get('dominant_emotion')
            if emotion:
                emotion_results.append(emotion)
        else:
            print("Error from API:", response.json().get('error'))

    except Exception as e:
        print("Error processing image:", str(e))

    return '', 204


@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400

    response, _ = chat_with_model(user_message)
    return jsonify({'response': response})


if __name__ == '__main__':
    app.run(debug=True)
