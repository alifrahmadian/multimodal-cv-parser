# app.py
import gradio as gr
import json
from parser.ocr import extract_text          # Step 2-3
from parser.llm_parser import parse_cv       # Step 4
from parser.validator import validate_and_format  # Step 5
from dotenv import load_dotenv

load_dotenv()

def process_cv(file):
    # Step 2-3: Ekstrak teks dari file
    text = extract_text(file)

    # Step 4: Parse dengan LLM
    raw_json = parse_cv(text)

    # Step 5: Validasi & format
    result = validate_and_format(raw_json)

    # Step 6: Kembalikan sebagai JSON string yang rapi
    return json.dumps(result, indent=2, ensure_ascii=False)

# Step 6: Bangun UI Output Layer
with gr.Blocks(title="CV Parser") as demo:
    gr.Markdown("## 📄 Multimodal CV Parser")

    with gr.Row():
        file_input = gr.File(
            label="Upload CV (PDF/JPG/PNG)",
            file_types=[".pdf", ".jpg", ".png"]
        )

    parse_btn = gr.Button("Parse CV", variant="primary")

    # Output: Tampilkan JSON
    json_output = gr.Code(
        label="Hasil Parsing (JSON)",
        language="json"
    )

    # Output: Tombol download
    download_btn = gr.DownloadButton(label="Download JSON")

    parse_btn.click(
        fn=process_cv,
        inputs=file_input,
        outputs=json_output
    )

if __name__ == "__main__":
    demo.launch()