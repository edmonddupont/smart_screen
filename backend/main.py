from fastapi import FastAPI, UploadFile, WebSocket
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from pypylon import pylon
import cv2
import base64
import numpy as np
import threading
from fastapi.responses import JSONResponse

app = FastAPI()
# Replace this with your Lorex RTSP URL
RTSP_URL = "rtsp://admin:M1ghty1sH3*@192.168.1.86:554/cam/realmonitor?channel=1&subtype=1"

# CORS setup to allow frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files (for frontend or media if needed)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def root():
    return {"message": "Smart Screen backend running"}

# Placeholder endpoint for image stream
@app.websocket("/ws/facestream")
async def face_stream(websocket: WebSocket):
    await websocket.accept()
    while True:
        await websocket.send_text("frame_placeholder")

@app.get("/camera/frame")
def get_camera_frame():
    try:
        # Connect to camera
        camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
        camera.Open()
        camera.StartGrabbingMax(1)
        grab_result = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

        if grab_result.GrabSucceeded():
            image = grab_result.Array

            # Convert to BGR for JPEG
            image_bgr = cv2.cvtColor(image, cv2.COLOR_BAYER_RG2BGR)
            _, jpeg = cv2.imencode(".jpg", image_bgr)
            jpg_bytes = jpeg.tobytes()
            b64_bytes = base64.b64encode(jpg_bytes).decode("utf-8")

            camera.StopGrabbing()
            camera.Close()
            return JSONResponse(content={"image": b64_bytes})

        else:
            return JSONResponse(content={"error": "Grab failed"}, status_code=500)

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

# Shared frame buffer
latest_frame = None
lock = threading.Lock()

def rtsp_worker():
    global latest_frame
    cap = cv2.VideoCapture(RTSP_URL)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            continue
        ret, jpeg = cv2.imencode(".jpg", frame)
        if ret:
            with lock:
                latest_frame = jpeg.tobytes()

@app.get("/lorex_stream")
def lorex_stream():
    def generate():
        while True:
            with lock:
                if latest_frame is not None:
                    yield (
                        b"--frame\r\n"
                        b"Content-Type: image/jpeg\r\n\r\n" + latest_frame + b"\r\n"
                    )
    return Response(generate(), media_type="multipart/x-mixed-replace; boundary=frame")

# Start thread on boot
threading.Thread(target=rtsp_worker, daemon=True).start()
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
