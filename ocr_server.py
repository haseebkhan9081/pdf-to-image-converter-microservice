import requests
import base64
from io import BytesIO
from pdf2image import convert_from_bytes
import pytesseract
from flask import Flask, request, jsonify

app = Flask(__name__)

# Function to fetch PDF from URL and convert to base64
def pdf_to_base64(pdf_url):
    # Fetch the PDF from the URL
    response = requests.get(pdf_url)
    # Check if request was successful
    if response.status_code == 200:
        # Convert PDF content to base64
        pdf_base64 = base64.b64encode(response.content)
        print(pdf_base64[:3])
        return pdf_base64
    else:
        return None  # Return None if failed to fetch PDF

# Function to perform OCR on base64-encoded PDF content
def perform_ocr(pdf_base64):
    # Decode base64 content
    pdf_content = base64.b64decode(pdf_base64)
    # Convert PDF content to list of PIL Image objects
    pdf_images = convert_from_bytes(pdf_content)
    
    # Initialize empty string to store OCR results
    ocr_text = ""
    
    # Perform OCR on each page of the PDF
    for page in pdf_images:
        # Perform OCR using Tesseract
        ocr_text += pytesseract.image_to_string(page)
    
    return ocr_text

@app.route('/perform_ocr', methods=['POST'])
def ocr_endpoint():
    data = request.get_json()
    pdf_url = data.get('pdf_url')
    pdf_base64 = pdf_to_base64(pdf_url)
    if pdf_base64:
        ocr_text = perform_ocr(pdf_base64)
        return jsonify({'ocr_text': ocr_text})
    else:
        return jsonify({'error': 'Failed to fetch PDF from URL'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
