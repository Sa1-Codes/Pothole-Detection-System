from flask import Flask, request, render_template, send_from_directory
import os
from utils import predict

app = Flask(__name__)

# Folder where uploaded images will be saved
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure uploads folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None
    uploaded_img = None

    if request.method == "POST":
        file = request.files.get("image")
        if file and file.filename != "":
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            label, _ = predict(filepath)  # Unpack label and prediction class
            prediction = label
            uploaded_img = file.filename

    return render_template("index.html", prediction=prediction, image=uploaded_img)

# ✅ Serve uploaded images securely
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# ✅ Run the Flask app on port 8000
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
