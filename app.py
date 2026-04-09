from flask import Flask, request, jsonify
from PIL import Image
import pytesseract
import joblib
import io
import os

app = Flask(__name__)

# 🔥 Load your AI model and vectorizer
model = joblib.load("model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

# 🔥 FIX: Set Tesseract executable path
# For Linux / Render servers
pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"
# For Windows (if testing locally), use:
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

@app.route("/")
def home():
    return "Backend Running ✅"

@app.route("/upload", methods=["POST"])
def upload():
    try:
        # Check file presence
        if 'file' not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        file = request.files['file']

        if file.filename == "":
            return jsonify({"error": "Empty file"}), 400

        # Read file and convert to PIL Image
        img_bytes = file.read()
        img = Image.open(io.BytesIO(img_bytes))

        # 🔥 Extract text using Tesseract
        text = pytesseract.image_to_string(img)

        if not text.strip():
            return jsonify({"error": "No text detected in image"}), 400

        # Transform text using vectorizer and predict
        X = vectorizer.transform([text])
        prediction = model.predict(X)[0]

        result = "Real Offer Letter ✅" if prediction == 1 else "Fake ❌"

        return jsonify({"text": text, "result": result})

    except Exception as e:
        print("ERROR:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # 🔥 Ensure app listens to Render's PORT
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
