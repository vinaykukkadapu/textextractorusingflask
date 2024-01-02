from flask import Flask, render_template, request, redirect
import fitz  # PyMuPDF
from PIL import Image
import pytesseract

app = Flask(_name_)

# Set Tesseract path
pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"


def pdf_to_images(pdf_path):
    images = []
    pdf_document = fitz.open(pdf_path)
    for page_number in range(pdf_document.page_count):
        page = pdf_document[page_number]
        pixmap = page.get_pixmap()
        image = Image.frombytes("RGB", [pixmap.width, pixmap.height], pixmap.samples)
        images.append(image)
    return images


def ocr_on_pdf(pdf_path):
    images = pdf_to_images(pdf_path)
    extracted_text = []
    for image in images:
        text = pytesseract.image_to_string(image)
        extracted_text.append(text)
    return extracted_text


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "file" not in request.files:
            return redirect(request.url)

        file = request.files["file"]
        if file.filename == "":
            return redirect(request.url)

        if file:
            file_path = "uploads/sample.pdf"
            file.save(file_path)
            result = ocr_on_pdf(file_path)
            return render_template("result.html", result=result)

    return render_template("index.html")


if _name_ == "_main_":
    app.run(debug=True)