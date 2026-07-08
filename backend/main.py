from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import numpy as np
import cv2
import os
import urllib.request
import pickle
import json
from tensorflow import keras

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Download hand landmarker model if needed
MODEL_PATH = "hand_landmarker.task"
if not os.path.exists(MODEL_PATH):
    print("Downloading hand landmarker model...")
    url = "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task"
    urllib.request.urlretrieve(url, MODEL_PATH)
    print("Model downloaded.")

# Load MediaPipe hand detector
base_options = python.BaseOptions(model_asset_path=MODEL_PATH)
options = vision.HandLandmarkerOptions(
    base_options=base_options,
    num_hands=1,
    min_hand_detection_confidence=0.7,
    min_tracking_confidence=0.5
)
detector = vision.HandLandmarker.create_from_options(options)

# Load trained gesture model
print("Loading gesture model...")
gesture_model = keras.models.load_model("gesture_model.keras")

# Load label encoder and gesture names
with open("label_encoder.pkl", "rb") as f:
    label_encoder = pickle.load(f)

with open("gesture_names.json", "r") as f:
    gesture_names = json.load(f)

print(f"Loaded {len(gesture_names)} gestures: {gesture_names}")

CONFIDENCE_THRESHOLD = 0.7

@app.get("/")
def read_root():
    return {
        "message": "Sign Language Recognition API is running",
        "gestures": gesture_names
    }

@app.post("/detect")
async def detect_gesture(file: UploadFile = File(...)):
    # Read and decode image
    contents = await file.read()
    np_arr = np.frombuffer(contents, np.uint8)
    frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    if frame is None:
        return {"error": "Invalid image"}

    # Run MediaPipe hand detection
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
    results = detector.detect(mp_image)

    if not results.hand_landmarks:
        return {
            "gesture": "No hand detected",
            "confidence": 0,
            "landmarks": []
        }

    # Extract 63 landmark values (21 x 3)
    landmarks = []
    row = []
    for lm in results.hand_landmarks[0]:
        row += [lm.x, lm.y, lm.z]
        landmarks.append({
            "x": round(lm.x, 4),
            "y": round(lm.y, 4),
            "z": round(lm.z, 4)
        })

    # Run gesture classification
    input_data = np.array([row])
    predictions = gesture_model.predict(input_data, verbose=0)
    confidence = float(np.max(predictions))
    predicted_index = np.argmax(predictions)
    predicted_gesture = label_encoder.inverse_transform([predicted_index])[0]

    # Apply confidence threshold
    if confidence < CONFIDENCE_THRESHOLD:
        predicted_gesture = "Unknown Gesture"

    return {
        "gesture": predicted_gesture,
        "confidence": round(confidence * 100, 1),
        "landmarks": landmarks,
        "hands_count": len(results.hand_landmarks)
    }

@app.get("/gestures")
def get_gestures():
    return {"gestures": gesture_names}