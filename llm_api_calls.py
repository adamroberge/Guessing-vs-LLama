import os
import requests
import base64
from PIL import Image
from io import BytesIO
from api import DeepInfra_API

# Access your DeepInfra API key from environment variables
API_KEY = DeepInfra_API
BASE_URL = "https://api.deepinfra.com/v1/openai/chat/completions"

# Model name to use
model = "meta-llama/Llama-3.2-11B-Vision-Instruct"

# System prompt for the LLM to act as a Pictionary player
SYSTEM_PROMPT = """
You are a pictionary player. I'll give you an image of a doodle and you must output what this image is.
"""


# Function to convert an image to base64
def image_to_base64(image_path, size=(300, 300)):
    with Image.open(image_path) as img:
        img = img.resize(size, Image.LANCZOS)
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        encoded_string = base64.b64encode(buffered.getvalue())

    return encoded_string.decode('utf-8')


# Function to send the image and prompt to the model and get a description
def describe_image(image, missed_guesses=[], options={}):
    image_base64 = image_to_base64(image)

    # Prepare the payload for DeepInfra API
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Incorrect guesses: {missed_guesses}"},
            {"role": "user", "content": f"Here is the image: data:image/png;base64,{image_base64}"}
        ]
    }

    # Headers for the API request (including authorization with API key)
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    # Make a POST request to the DeepInfra OpenAI-compatible API
    response = requests.post(BASE_URL, json=payload, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        return f"Error: {response.status_code}, {response.text}"


# Main code to test the describe_image function
if __name__ == "__main__":
    # Call the function with a test image
    result = describe_image("images/doodle.png")
    print(result)
