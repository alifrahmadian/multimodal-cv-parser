from __future__ import annotations

import json
import os

from openai import OpenAI

# ─── System prompt ────────────────────────────────────────────────────────────

_SYSTEM_PROMPT = """
Kamu adalah parser CV profesional. Tugasmu adalah mengekstrak informasi dari teks CV
dan mengembalikannya sebagai JSON yang valid, tanpa teks tambahan apapun.

Kembalikan HANYA JSON dengan struktur persis seperti ini:
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

Aturan:
- Kembalikan HANYA JSON, tanpa penjelasan, tanpa markdown, tanpa backtick
- Jika informasi tidak ditemukan, gunakan string kosong "" atau array kosong []
- Format tanggal bebas, gunakan apa yang tertera di CV (misal: "Jan 2020", "2019", "2020-2023")
- Pisahkan skills: softskills (komunikasi, leadership, dll), hardskills (Python, Excel, dll)
""".strip()

def parse_cv(text: str) -> str:
    """
    Kirim teks OCR ke OpenAI, terima JSON string terstruktur.

    Args:
        text : Teks mentah hasil extract_text() dari ocr.py.

    Returns:
        JSON string mentah dari OpenAI (belum divalidasi).
        validator.py yang akan memvalidasi & memformat hasilnya.
    """
    if not text.strip():
        return json.dumps({"error": "Teks kosong, OCR mungkin gagal"})

    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0,                  # Deterministik untuk parsing
        response_format={"type": "json_object"},  # Paksa output JSON
        messages=[
            {"role": "system", "content": _SYSTEM_PROMPT},
            {"role": "user", "content": f"Ekstrak data dari CV berikut:\n\n{text}"},
        ],
    )

    return response.choices[0].message.content