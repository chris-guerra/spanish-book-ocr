import fitz  # PyMuPDF for PDF processing
from PIL import Image
import pytesseract
import io
import cv2
import numpy as np
import re
import os
from transformers import AutoTokenizer, AutoModelForCausalLM

# Enable parallelism for the tokenizer
os.environ["TOKENIZERS_PARALLELISM"] = "true"

# Load the LLaMA model and tokenizer
model_name = "Kukedlc/Llama-7b-spanish"  # Replace with your chosen LLaMA model
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto", torch_dtype="auto")

# Path to your PDF file
pdf_path = 'test.pdf'

def preprocess_with_opencv(img):
    """
    Preprocess the image using OpenCV to prepare it for OCR.
    """
    img_gray = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2GRAY)
    img_blur = cv2.GaussianBlur(img_gray, (5, 5), 0)
    _, img_binary = cv2.threshold(img_blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return img_binary

def detect_page_number(text):
    """
    Detect lines with no alphabetic characters at the start or end of the text.
    """
    lines = text.splitlines()
    if lines and not any(char.isalpha() for char in lines[-1]):
        return lines[-1]
    elif lines and not any(char.isalpha() for char in lines[0]):
        return lines[0]
    else:
        return None

# Initialize an empty list to hold the text for each page
pages_text = []
corrected_pages_text = []

# Open the PDF file
with fitz.open(pdf_path) as pdf_document:
    for page_num in range(pdf_document.page_count):
        # Get each page as a pixmap (image)
        page = pdf_document.load_page(page_num)
        pix = page.get_pixmap(dpi=300)

        print("converting_image")
        # Convert pixmap to PIL image
        img = Image.open(io.BytesIO(pix.tobytes("png")))

        # Preprocess the image with OpenCV
        preprocessed_img = preprocess_with_opencv(img)

        # Convert the processed OpenCV image back to a PIL image for Tesseract
        preprocessed_pil_img = Image.fromarray(preprocessed_img)

        # Perform OCR on the preprocessed image using Spanish language
        page_text = pytesseract.image_to_string(preprocessed_pil_img, lang='spa').strip()
        print("OCR correction")
        # Detect and remove the first or last line if they don't contain letters
        page_number_text = detect_page_number(page_text)
        if page_number_text is not None:
            page_text = page_text.replace(page_number_text, "")

        # Join words if they are cut at the end of the line
        page_text = re.sub(r"-\n\s*", "", page_text)
        page_text = re.sub(r"(?<!\n)\n(?!\n)", " ", page_text)
        page_text = page_text.replace("\n\n", "\n")

        print("LLM")
        # Correct the spelling and grammar errors using LLaMA
        corrected_text = correct_text_with_llama(page_text)
        print(corrected_text)
        pages_text.append(page_text)
        corrected_pages_text.append(corrected_text)

# Print the original and corrected text for each page
for i, (original, corrected) in enumerate(zip(pages_text, corrected_pages_text)):
    print(f"--- Page {i + 1} ---")
    print("Original Text:")
    print(original)
    print("\nCorrected Text:")
    print(corrected)
    print("\n" + "=" * 40 + "\n")