import gradio as gr
from parser.llm_parser import LLMParser
from parser.validator import ensure_schema
from utils.file_handler import pdf_to_image

SYSTEM_PROMPT = """
Extract structured CV into JSON:

{
  "nama": "",
  "experience": [
    {
      "posisi": "",
      "start": "",
      "end": "",
      "description": ""
    }
  ],
  "education": [
    {
      "degree": "",
      "univ": "",
      "start": "",
      "end": "",
      "field": ""
    }
  ],
  "skills": {
    "softskills": [],
    "hardskills": []
  }
}

Rules:
- Fill empty if missing
- Return ONLY JSON
"""

parser = LLMParser(SYSTEM_PROMPT)

def process(file):
    path = pdf_to_image(file.name)   # handle PDF
    result = parser.parse(path)
    result = ensure_schema(result)
    return result

app = gr.Interface(
    fn=process,
    inputs=gr.File(),
    outputs=gr.JSON(),
    title="CV Ekstrak"
)

app.launch()