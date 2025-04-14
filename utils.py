import numpy as np
import tensorflow as tf
import cv2
import random
from datetime import datetime
from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# MongoDB Atlas setup
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["pothole_db"]
collection = db["detections"]

# Model setup
IMG_SIZE = 32
MODEL_PATH = "model/model.tflite"
interpreter = tf.lite.Interpreter(model_path=MODEL_PATH)
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

def preprocess_image(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        return None
    image = cv2.resize(image, (IMG_SIZE, IMG_SIZE))
    image = np.expand_dims(image, axis=(0, -1))  # Add batch and channel dimensions
    image = ((image / 255.0) * 255 - 128).astype(np.int8)
    return image

def simulate_gps():
    # Generate random GPS coordinates (simulate GPS)
    latitude = round(random.uniform(18.5, 19.5), 6)
    longitude = round(random.uniform(73.5, 74.5), 6)
    return latitude, longitude

def predict(image_path):
    img = preprocess_image(image_path)
    if img is None:
        return "Error: Could not process image.", None
    interpreter.set_tensor(input_details[0]['index'], img)
    interpreter.invoke()
    output_data = interpreter.get_tensor(output_details[0]['index'])
    predicted_class = np.argmax(output_data)
    label = "🚧 Pothole Detected!" if predicted_class == 1 else "✅ No Pothole Detected."

    if predicted_class == 1:
        lat, lon = simulate_gps()
        record = {
            "filename": os.path.basename(image_path),
            "prediction": label,
            "latitude": lat,
            "longitude": lon,
            "timestamp": datetime.utcnow()
        }
        collection.insert_one(record)

    return label, predicted_class
