import openai
import os
import base64
from PIL import Image
from io import BytesIO
from api import LLAMA_API_KEY


# API_KEY = os.environ["LLAMA_API_KEY"]
API_KEY = LLAMA_API_KEY
print(API_KEY)
BASE_URL = "https://api.deepinfra.com/v1/openai"  # EDIT THIS

llm_client = openai.OpenAI(api_key=API_KEY, base_url=BASE_URL)
model = "meta-llama/Llama-3.2-11B-Vision-Instruct"
# llm_client = openai.OpenAI()
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
    out = llm_client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": SYSTEM_PROMPT},
                ]
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"Incorrect answers so far - don't choose these: {missed_guesses}"
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/png;base64,{image_base64}"}
                    },
                ],
            }
        ],
    )
    return out.choices[0].message.content


if __name__ == "__main__":
    out = describe_image("images/doodle.png")
    print(out)
