import pytesseract
from PIL import Image, ImageDraw, ImageFont
import cv2
import numpy as np
import fitz

def pdf_to_text(path):
    doc = fitz.open(str(path))
    text = ""
    for page in doc:
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        text += pytesseract.image_to_string(img)
    return text

def image_to_text(path):
    img = Image.open(path)
    return pytesseract.image_to_string(img)

def extract_text(file):
    if file.name.endswith(".pdf"):
        return pdf_to_text(file.name)
    else:
        return image_to_text(file.name)
        