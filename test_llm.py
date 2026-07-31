import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.getenv("NVIDIA_API_KEY")
)

response = client.chat.completions.create(
    model="meta/llama-3.2-3b-instruct",
    messages=[
        {
            "role": "user",
            "content": """
            Identify the license in this text:

            This work is licensed under a
            Creative Commons Attribution-NonCommercial
            4.0 International License.

            Return:
            License name
            License family
            Commercial use allowed
            Modification allowed
            Attribution required
            Evidence
            """
        }
    ],
    temperature=0.2,
    max_tokens=500
)

print(response.choices[0].message.content)