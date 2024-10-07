import openai
import os
import base64
from PIL import Image
from io import BytesIO

# Enable debug logging
openai.log = "debug"

# Fetch API Key and Deployment ID from environment variables
API_KEY = os.environ.get("DEEPINFRA_API_KEY")
DEPLOYMENT_ID = os.environ.get("DEEPINFRA_DEPLOYMENT_ID")

if not API_KEY or not DEPLOYMENT_ID:
    raise ValueError("API key and deployment ID must be set.")

# Set API key and base URL
openai.api_key = API_KEY
openai.api_base = 'https://api.deepinfra.com/v1/openai'

# Model name (ensure this matches your deployment)
MODEL_NAME = 'meta-llama/Llama-3.2-11B-Vision-Instruct'

SYSTEM_PROMPT = """
You are a pictionary player. I'll give you an image of a doodle and you must output what this image is.
"""


def image_to_base64(image_path, size=(300, 300)):
    with Image.open(image_path) as img:
        img = img.resize(size, Image.LANCZOS)
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        encoded_string = base64.b64encode(buffered.getvalue())
    return encoded_string.decode("utf-8")


def describe_image(image, missed_guesses=[], options={}):
    image_base64 = image_to_base64(image)
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Incorrect answers so far - don't choose these: {missed_guesses}"},
        {"role": "user",
            "content": f"![Image](data:image/png;base64,{image_base64})"},
        {"role": "image-url", "image-url": {"url": f"data:image/png;base64, {image_base64}"}},

    ]
    response = openai.ChatCompletion.create(
        model=MODEL_NAME,
        messages=messages,
        deployment_id=DEPLOYMENT_ID
    )
    return response.choices[0].message["content"]


if __name__ == "__main__":
    out = describe_image("images/doodle.png")
    print(out)
