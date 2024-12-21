import boto3
from botocore.exceptions import NoCredentialsError
import plotly.graph_objects as go
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
BUCKET_NAME = os.getenv("BUCKET_NAME")


def upload_to_s3(file_path, bucket_name, object_name=None):
    if object_name is None:
        object_name = os.path.basename(file_path)

    try:
        s3_client = boto3.client(
            's3',
            aws_access_key_id=AWS_ACCESS_KEY,
            aws_secret_access_key=AWS_SECRET_KEY
        )
        s3_client.upload_file(file_path, bucket_name, object_name)

        # Return the S3 object URL
        object_url = f"https://{bucket_name}.s3.amazonaws.com/{object_name}"
        return object_url
    except FileNotFoundError:
        print(f"The file {file_path} was not found.")
    except NoCredentialsError:
        print("AWS credentials not available.")
    except Exception as e:
        print(f"An error occurred: {e}")
    return None


def plot_emotion_graph(emotion_list, output_path):
    try:
        if len(emotion_list) >= 5:  # Only create the graph if there are at least 10 emotions
            # Map emotions to numerical values
            emotion_mapping = {
                'angry': 1,
                'disgust': 2,
                'fear': 2,
                'happy': 5,
                'sad': 1,
                'surprise': 4,
                'neutral': 3
            }
            emotion_values = [emotion_mapping.get(emotion.lower(), 0) for emotion in emotion_list]

            # Create the line graph using Plotly
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=list(range(1, len(emotion_values) + 1)),
                y=emotion_values,
                mode='lines+markers',
                line=dict(color='#4a90e2', width=2),
                marker=dict(size=8),
                name='Emotions'
            ))

            # Update layout
            fig.update_layout(
                xaxis=dict(title='Time (Chat Progression)', showgrid=True),
                yaxis=dict(title='Emotional Intensity', showgrid=True),
                plot_bgcolor='white',
                margin=dict(l=40, r=40, t=20, b=40),
                height=300
            )

            # Save the graph as an HTML file in the static folder
            graph_filename = "emotions_graph.html"
            graph_path = os.path.join(output_path, graph_filename)
            fig.write_html(graph_path)

            return graph_filename
    except Exception as e:
        print(f"Error generating graph: {e}")
        return None
