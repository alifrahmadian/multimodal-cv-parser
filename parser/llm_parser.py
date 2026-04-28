from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
import json
import base64
from openai import OpenAI
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

class LLMParser:
    def __init__(self, system_prompt: str):
        self.llm = ChatOpenAI(
            model="gpt-4o",
            temperature=0
        )
        self.system_prompt = system_prompt

    def encode_image(self, file_path: str):
        with open(file_path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")

    def parse(self, file_path: str):
        base64_img = self.encode_image(file_path)

        message = HumanMessage(
            content=[
                {"type": "text", "text": "Parse this CV into JSON."},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{base64_img}"
                    }
                }
            ]
        )

        response = self.llm.invoke([
            SystemMessage(content=self.system_prompt),
            message
        ])

        try:
            return json.loads(response.content)
        except:
            return {
                "error": "Invalid JSON",
                "raw": response.content
            }