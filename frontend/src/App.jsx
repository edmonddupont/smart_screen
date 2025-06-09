import React from "react";
import "./App.css";

function App() {
  return (
    <div className="dashboard">
      <div className="tile camera">
        <h2>📷 Local Camera</h2>
        <img
          src="/placeholder_camera.jpg"
          alt="Basler Placeholder"
          className="thumbnail"
        />
        <p>Waiting for camera connection...</p>
      </div>

      <div className="tile rtsp">
        <h2>📺 Lorex RTSP Stream</h2>
        <img
          src="/placeholder_rtsp.jpg"
          alt="RTSP Placeholder"
          className="thumbnail"
        />
        <p>Waiting for live feed...</p>
      </div>

      <div className="tile calendar">
        <h2>📅 Google Calendar</h2>
        <ul>
          <li>Meeting with team — 10:00 AM</li>
          <li>Lunch with Jane — 12:30 PM</li>
          <li>Hardware sync — 3:00 PM</li>
        </ul>
        <p>(Connected placeholder)</p>
      </div>

      <div className="tile notes">
        <h2>🧭 Project Notes</h2>
        <p>This area can be used for system messages or alerts.</p>
      </div>
    </div>
  );
}

export default App;
