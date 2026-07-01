import { useState } from "react";
import "./App.css";

function App() {
  const [gesture, setGesture] = useState("Waiting for gesture...");
  const [confidence, setConfidence] = useState(0);
  const [log, setLog] = useState([]);

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
          <div className="webcam-placeholder">
            <p>Camera will appear here</p>
          </div>
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