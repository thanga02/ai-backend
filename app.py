from flask import Flask, request, jsonify
from PIL import Image
import pytesseract
import joblib
import io

app = Flask(__name__)

model = joblib.load("model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

@app.route("/")
def home():
    return "Backend Running ✅"

@app.route("/upload", methods=["POST"])
def upload():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        file = request.files['file']

        if file.filename == "":
            return jsonify({"error": "Empty file"}), 400

        # 🔥 FIX: read file properly
        img_bytes = file.read()
        img = Image.open(io.BytesIO(img_bytes))

        text = pytesseract.image_to_string(img)

        X = vectorizer.transform([text])
        prediction = model.predict(X)[0]

        result = "Real Offer Letter ✅" if prediction == 1 else "Fake ❌"

        return jsonify({"text": text, "result": result})

    except Exception as e:
        print("ERROR:", e)
        return jsonify({"error": str(e)}), 500
