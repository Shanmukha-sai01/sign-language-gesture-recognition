import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import csv
import os
import time

# Gestures we want to collect data for
GESTURES = [
    "Hi", "Bye", "Thank You", "Please", "Help",
    "Yes", "No", "OK", "I Love You", "Sorry",
    "Stop", "Come Here", "Emergency", "I Need Water",
    "I Need Food", "I Am in Pain", "Happy", "Sad"
]

# Setup MediaPipe
MODEL_PATH = "hand_landmarker.task"
base_options = python.BaseOptions(model_asset_path=MODEL_PATH)
options = vision.HandLandmarkerOptions(
    base_options=base_options,
    num_hands=1,
    min_hand_detection_confidence=0.7,
    min_tracking_confidence=0.5
)
detector = vision.HandLandmarker.create_from_options(options)

# CSV file setup
CSV_FILE = "gesture_data.csv"
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        # Header: gesture label + 63 values (21 landmarks x 3 coords)
        header = ["gesture"]
        for i in range(21):
            header += [f"x{i}", f"y{i}", f"z{i}"]
        writer.writerow(header)
    print(f"Created {CSV_FILE}")

def collect_gesture(gesture_name, num_samples=100):
    cap = cv2.VideoCapture(0)
    samples_collected = 0
    collecting = False

    print(f"\n--- Collecting: {gesture_name} ---")
    print("Get ready to perform the gesture.")
    print("Press SPACE to start collecting, Q to quit early.\n")

    while samples_collected < num_samples:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
        results = detector.detect(mp_image)

        # Draw landmarks
        if results.hand_landmarks:
            for hand_landmarks in results.hand_landmarks:
                for lm in hand_landmarks:
                    h, w, _ = frame.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    cv2.circle(frame, (cx, cy), 5, (0, 255, 0), -1)

        # UI text
        status = f"Collecting: {samples_collected}/{num_samples}" if collecting else "Press SPACE to start"
        cv2.putText(frame, f"Gesture: {gesture_name}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)
        cv2.putText(frame, status, (10, 65),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, "Q: quit this gesture", (10, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

        cv2.imshow("Data Collection", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('q'):
            print(f"Skipped. Collected {samples_collected} samples.")
            break
        elif key == ord(' '):
            collecting = True
            print("Collecting...")

        # Save landmark data
        if collecting and results.hand_landmarks:
            row = [gesture_name]
            for lm in results.hand_landmarks[0]:
                row += [round(lm.x, 4), round(lm.y, 4), round(lm.z, 4)]
            with open(CSV_FILE, "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(row)
            samples_collected += 1
            time.sleep(0.05)  # Small delay between samples

    cap.release()
    cv2.destroyAllWindows()
    print(f"Done. Collected {samples_collected} samples for '{gesture_name}'.")

# Main
print("=== Sign Language Data Collection Tool ===")
print(f"Will collect data for {len(GESTURES)} gestures.")
print("For each gesture you will collect 100 samples.\n")

for i, gesture in enumerate(GESTURES):
    print(f"[{i+1}/{len(GESTURES)}] Next gesture: {gesture}")
    input("Press ENTER when ready (or Ctrl+C to stop completely)...")
    collect_gesture(gesture, num_samples=100)

print("\n✅ Data collection complete!")
print(f"Dataset saved to: {CSV_FILE}")
