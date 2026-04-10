from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
import pytesseract
import io
import os
import joblib

app = Flask(__name__)
CORS(app)

# --- PERMANENT FIX FOR WINDOWS OCR ---
# 1. Ensure you have installed Tesseract from: https://github.com/UB-Mannheim/tesseract/wiki
# 2. Update this path to where YOU installed it:
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Load your AI models
model = joblib.load("model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

@app.route("/upload", methods=["POST"])
def upload_image():
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400
    
    file = request.files['image']
    
    try:
        # 1. Open the image using Pillow (PIL)
        img = Image.open(file.stream)
        
        # 2. Run OCR to get text
        extracted_text = pytesseract.image_to_string(img)
        
        # 3. Use your AI model (example logic)
        # prediction = model.predict(vectorizer.transform([extracted_text]))
        
        return jsonify({
            "status": "success",
            "text": extracted_text
        })
        
    except Exception as e:
        # This will print the REAL error in your VS Code terminal
        print(f"ERROR: {str(e)}")
        return jsonify({"status": "failed", "error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
