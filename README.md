# sign-language-gesture-recognition
AI-powered real-time sign language gesture recognition web app


🤟 Sign Language Gesture Recognition

A real-time AI-powered web application that recognizes sign language gestures through a webcam and converts them into text — helping deaf/non-speaking people communicate with hearing people.


🎯 What It Does


Opens your webcam in the browser
Detects your hand using MediaPipe (21 landmark points)
Classifies the gesture using a trained neural network (98.24% accuracy)
Displays the gesture name and confidence score in real time
Logs all detected gestures with timestamps



🧠 Supported Gestures (17)

GestureMeaning👋 HiHello👋 ByeGoodbye🙏 Thank YouExpress gratitude🙏 PleasePolite request🆘 HelpNeed assistance👍 YesAffirmative👎 NoNegative❤️ I Love YouExpress love🤝 SorryApologize✋ StopStop action👉 Come HereRequest presence🚑 EmergencyUrgent help needed💧 I Need WaterRequest water🍽️ I Need FoodRequest food😖 I Am in PainExpress pain😊 HappyExpress happiness😢 SadExpress sadness


🛠️ Tech Stack

Backend


Python 3.12 — Backend language
FastAPI — REST API framework
Uvicorn — ASGI server
MediaPipe — Hand landmark detection (Google)
OpenCV — Image processing
TensorFlow/Keras — Neural network training and inference
scikit-learn — Data preprocessing and evaluation
NumPy — Numerical computing
Pandas — Dataset handling


Frontend


React.js — UI framework
Vite — Build tool and dev server
ESLint — Code linting
getUserMedia API — Browser webcam access


DevOps


Git + GitHub — Version control
dev/main branch workflow — Industry-standard branching strategy



📁 Project Structure

sign-language-gesture-recognition/
├── backend/
│   ├── main.py                 # FastAPI app with /detect endpoint
│   ├── collect_data.py         # Data collection tool
│   ├── train_model.py          # Model training script
│   ├── gesture_data.csv        # Training dataset (1700 samples)
│   ├── gesture_model.keras     # Trained neural network
│   ├── gesture_names.json      # List of gesture class names
│   ├── label_encoder.pkl       # Scikit-learn label encoder
│   ├── test_mediapipe.py       # MediaPipe standalone test
│   ├── requirements.txt        # Python dependencies
│   └── venv/                   # Python virtual environment (not committed)
├── frontend/
│   ├── src/
│   │   ├── App.jsx             # Main React component
│   │   ├── App.css             # Component styles
│   │   └── index.css           # Global styles
│   ├── index.html              # HTML entry point
│   ├── package.json            # Node dependencies
│   └── vite.config.js          # Vite configuration
├── docs/                       # Project documentation
├── .gitignore                  # Files excluded from Git
└── README.md                   # This file


🚀 Getting Started

Prerequisites


Python 3.12
Node.js 18+
Git
A webcam
