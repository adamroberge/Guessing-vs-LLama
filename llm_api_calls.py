import openai
import os
import base64
from PIL import Image
from io import BytesIO


# DeepInfra API key
API_KEY = os.environ.get("DEEPINFRA_API_KEY")
# DeepInfra Deployment ID
DEPLOYMENT_ID = os.environ.get("DEEPINFRA_DEPLOYMENT_ID")


# Check if API key is set
if not API_KEY:
    raise ValueError("Please set the DEEPINFRA_API_KEY environment variable.")

# Set the base URL for DeepInfra's OpenAI-compatible API
openai.api_key = API_KEY
openai.api_base = 'https://api.deepinfra.com/v1/deployment/openai'

# Model name (ensure it matches your deployment)
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

    return encoded_string.decode('utf-8')


def describe_image(image, missed_guesses=[], options={}):
    image_base64 = image_to_base64(image)

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": f"Incorrect answers so far - don't choose these: {missed_guesses}"
        },
        {
            "role": "user",
            "content": f"![Image](data:image/png;base64,{image_base64})"
        }
    ]

    # Create the chat completion
    response = openai.ChatCompletion.create(
        model=MODEL_NAME,
        messages=messages,
        deployment_id=DEPLOYMENT_ID  # Include your deployment ID here
    )

    # Extract the assistant's reply
    return response.choices[0].message['content']


if __name__ == "__main__":
    out = describe_image("images/doodle.png")
    print(out)
