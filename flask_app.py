# flask_app.py

from flask import Flask, request, jsonify
from llm_api_calls import describe_image
from flask_cors import CORS
import random
import base64
from PIL import Image
from io import BytesIO
from topics import topics

app = Flask(__name__)

# Adjust CORS settings as needed
CORS(app, resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

topics = topics  # from topics.py
current_topic = None


def check_correctness(llm_pred):
    return all([(t in llm_pred.lower()) for t in current_topic["targets"]])


@app.route("/begin_pictionary", methods=["GET"])
def api_begin_pictionary():
    global current_topic
    current_topic = random.choice(topics)
    return jsonify({"topic": current_topic["concept"]})


@app.route('/describe_image', methods=['POST'])
def api_describe_image():
    base64_image = request.form.get('image')
    if not base64_image:
        return jsonify({"error": "No image data provided"}), 400

    image_data = base64.b64decode(base64_image)
    image = Image.open(BytesIO(image_data)).convert("RGB")

    image_path = 'images/drawing.png'
    image.save(image_path)

    description = describe_image(image_path)

    correct = check_correctness(description)
    print(f"Description being returned: {description}")
    print(f"Correct: {correct}")

    return jsonify({"description": description, "correct": correct})


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5001)
