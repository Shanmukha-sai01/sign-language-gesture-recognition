from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import numpy as np
import cv2
import os
import urllib.request

app = FastAPI()

# Allow React frontend to talk to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Download model if not present
MODEL_PATH = "hand_landmarker.task"
if not os.path.exists(MODEL_PATH):
    print("Downloading hand landmarker model...")
    url = "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task"
    urllib.request.urlretrieve(url, MODEL_PATH)
    print("Model downloaded.")

# Initialize MediaPipe hand detector
base_options = python.BaseOptions(model_asset_path=MODEL_PATH)
options = vision.HandLandmarkerOptions(
    base_options=base_options,
    num_hands=2,
    min_hand_detection_confidence=0.7,
    min_tracking_confidence=0.5
)
detector = vision.HandLandmarker.create_from_options(options)

@app.get("/")
def read_root():
    return {"message": "Sign Language Recognition API is running"}

@app.post("/detect")
async def detect_gesture(file: UploadFile = File(...)):
    # Read image bytes from request
    contents = await file.read()
    np_arr = np.frombuffer(contents, np.uint8)
    frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    if frame is None:
        return {"error": "Invalid image"}

    # Convert BGR to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

    # Run hand detection
    results = detector.detect(mp_image)

    if not results.hand_landmarks:
        return {
            "gesture": "No hand detected",
            "confidence": 0,
            "landmarks": []
        }

    # Extract landmarks from first hand
    landmarks = []
    for lm in results.hand_landmarks[0]:
        landmarks.append({
            "x": round(lm.x, 4),
            "y": round(lm.y, 4),
            "z": round(lm.z, 4)
        })

    return {
        "gesture": "Hand detected",
        "confidence": 95,
        "landmarks": landmarks,
        "hands_count": len(results.hand_landmarks)
    }