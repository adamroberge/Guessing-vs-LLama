import random
from flask_cors import CORS
from llm_api_calls import *
from flask import Flask, request, jsonify
import logging


topics = [
    {
        "concept": "cat sitting on a table",
        "targets": ["cat", "table"]
    },
    {
        "concept": "dog eating a bone",
        "targets": ["dog", "bone"]
    },
    {
        "concept": "factory emitting smoke",
        "targets": ["factory", "smoke"]
    },
    {
        "concept": "An apple and a banana",
        "targets": ["apple", "banana"]
    },
    {
        "concept": "waterfalls with sun",
        "targets": ["waterfall", "sun"]
    },
    {
        "concept": "mountains and river",
        "targets": ["mountain", "river"]
    },
    {
        "concept": "trees and birds flying around",
        "targets": ["tree", "birds"]
    },
    {
        "concept": "man riding bicycle",
        "targets": ["man", "bicycle"]
    }
]

current_topic = None

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:8000"}})
app.config['CORS_HEADERS'] = 'Content-Type'


def check_correctness(llm_pred):
    return all([(t in llm_pred) for t in current_topic["targets"]])


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

    logging.basicConfig(level=logging.INFO)
    logging.info(f"Description being returned: {description}")
    logging.info(f"Correct: {correct}")

    return jsonify({"description": description, "correct": correct})


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
    # app.run(debug=True)
