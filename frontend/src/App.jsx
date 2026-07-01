import { useState, useEffect, useRef } from "react";
import "./App.css";

function App() {
  const [gesture, setGesture] = useState("Waiting for gesture...");
  const [confidence, setConfidence] = useState(0);
  const [log, setLog] = useState([]);
  const [cameraError, setCameraError] = useState(null);
  const videoRef = useRef(null);

  useEffect(() => {
    startCamera();
    return () => stopCamera();
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

  return (
    <div className="app">
      {/* Header */}
      <header className="header">
        <h1>🤟 Sign Language Recognition</h1>
        <p>Real-time gesture detection powered by AI</p>
      </header>

      {/* Main Content */}
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
        </div>

        {/* Right: Output Panel */}
        <div className="output-panel">
          {/* Detected Gesture */}
          <div className="gesture-box">
            <h2>🖐 Detected Gesture</h2>
            <div className="gesture-result">{gesture}</div>
            <div className="confidence">
              Confidence: <strong>{confidence}%</strong>
            </div>
          </div>

          {/* Conversation Log */}
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