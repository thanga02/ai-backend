from flask import Flask, request, jsonify
from flask_cors import CORS
import pytesseract
from PIL import Image

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "Backend Running ✅"

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files['file']
    img = Image.open(file)

    text = pytesseract.image_to_string(img)

    if "offer" in text.lower():
        result = "Valid Offer Letter ✅"
    else:
        result = "Fake ❌"

    return jsonify({
        "text": text,
        "result": result
    })