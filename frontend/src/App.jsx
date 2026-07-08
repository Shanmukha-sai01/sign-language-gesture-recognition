import { useState, useEffect, useRef } from "react";
import "./App.css";

const API_URL = "http://127.0.0.1:8000";

function App() {
  const [gesture, setGesture] = useState("Waiting for gesture...");
  const [confidence, setConfidence] = useState(0);
  const [log, setLog] = useState([]);
  const [cameraError, setCameraError] = useState(null);
  const [isDetecting, setIsDetecting] = useState(false);
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const intervalRef = useRef(null);

  useEffect(() => {
    startCamera();
    return () => {
      stopCamera();
      clearInterval(intervalRef.current);
    };
  }, []);

  const startCamera = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: true,
        audio: false,
      });
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
      }
    } catch (err) {
      setCameraError("Camera access denied or not available.");
      console.error("Camera error:", err);
    }
  };

  const stopCamera = () => {
    if (videoRef.current && videoRef.current.srcObject) {
      videoRef.current.srcObject.getTracks().forEach((track) => track.stop());
    }
  };

  const captureAndDetect = async () => {
    if (!videoRef.current || !canvasRef.current) return;

    const video = videoRef.current;
    const canvas = canvasRef.current;
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    const ctx = canvas.getContext("2d");
    ctx.drawImage(video, 0, 0);

    canvas.toBlob(async (blob) => {
      if (!blob) return;

      const formData = new FormData();
      formData.append("file", blob, "frame.jpg");

      try {
        const response = await fetch(`${API_URL}/detect`, {
          method: "POST",
          body: formData,
        });

        const data = await response.json();

        setGesture(data.gesture || "Unknown");
        setConfidence(data.confidence || 0);

        if (data.gesture && data.gesture !== "No hand detected") {
          const now = new Date();
          const time = now.toLocaleTimeString();
          setLog((prev) => [
            { time, gesture: data.gesture, confidence: data.confidence },
            ...prev.slice(0, 19),
          ]);
        }
      } catch (err) {
        console.error("Detection error:", err);
        setGesture("API connection error");
      }
    }, "image/jpeg");
  };

  const toggleDetection = () => {
    if (isDetecting) {
      clearInterval(intervalRef.current);
      setIsDetecting(false);
      setGesture("Detection stopped");
    } else {
      intervalRef.current = setInterval(captureAndDetect, 1000);
      setIsDetecting(true);
      setGesture("Detecting...");
    }
  };

  return (
    <div className="app">
      <header className="header">
        <h1>🤟 Sign Language Recognition</h1>
        <p>Real-time gesture detection powered by AI</p>
      </header>

      <main className="main">
        {/* Left: Webcam Panel */}
        <div className="webcam-panel">
          <h2>📷 Camera Feed</h2>
          {cameraError ? (
            <div className="webcam-placeholder">
              <p>⚠️ {cameraError}</p>
            </div>
          ) : (
            <video
              ref={videoRef}
              autoPlay
              playsInline
              muted
              className="webcam-video"
            />
          )}
          <canvas ref={canvasRef} style={{ display: "none" }} />
          <button
            className={`detect-btn ${isDetecting ? "active" : ""}`}
            onClick={toggleDetection}
          >
            {isDetecting ? "⏹ Stop Detection" : "▶ Start Detection"}
          </button>
        </div>

        {/* Right: Output Panel */}
        <div className="output-panel">
          <div className="gesture-box">
            <h2>🖐 Detected Gesture</h2>
            <div className="gesture-result">{gesture}</div>
            <div className="confidence">
              Confidence: <strong>{confidence}%</strong>
            </div>
          </div>

          <div className="log-box">
            <h2>📝 Conversation Log</h2>
            {log.length === 0 ? (
              <p className="empty-log">No gestures detected yet.</p>
            ) : (
              <ul>
                {log.map((entry, index) => (
                  <li key={index}>
                    <span className="log-time">{entry.time}</span>
                    <span className="log-gesture">{entry.gesture}</span>
                    <span className="log-confidence">{entry.confidence}%</span>
                  </li>
                ))}
              </ul>
            )}
            <button className="clear-btn" onClick={() => setLog([])}>
              Clear Log
            </button>
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;