from flask import Flask, render_template, Response, jsonify
import cv2
import numpy as np
import time

app = Flask(__name__)

log_messages =[]
cap = None

def log(message):
    global log_messages
    log_messages.append(message)
    print(message)

def auto_calibrate(hsv_frame, tol_h=10, tol_s =50 , tol_v=50):
    height, width = hsv_frame.shape[:2]
    w, h = 100, 100
    x= width//2 -50
    y = height//2 -50
    roi = hsv_frame[y:y+h, x:x+w]

    mean_hsv = cv2.mean(roi)[:3]
    mean_hsv = np.array(mean_hsv, dtype=np.uint8)

    lower_bound = np.array([max(0, mean_hsv[0]-tol_h), max(0, mean_hsv[1]-tol_s), max(0, mean_hsv[2]-tol_v)], dtype=np.uint8)
    upper_bound = np.array([min(180, mean_hsv[0]+tol_h), min(255, mean_hsv[1]+tol_s), min(255, mean_hsv[2]+tol_v)], dtype=np.uint8)
    print("Auto calibrated lower HSV: ", lower_bound)
    print("Auto calibrated upper HSV: ", upper_bound)
    return lower_bound, upper_bound

def capture_background(cap, delay=0.05, num_frames=60):
    frames=[]
    log("Capturing Background. No one should be in frame for next three seconds.")
    for i in range(num_frames):
        ret, frame = cap.read()
        if ret:
            frames.append(frame.astype(np.float32))
        time.sleep(delay)
    
    if frames:
        avg_frame = np.mean(frames, axis=0).astype(np.uint8)
    else:
        avg_frame = None

    return avg_frame

def process_frame(frame, background, lower_hsv, upper_hsv, kernel):
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv_frame, lower_hsv, upper_hsv)
    #mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=2) #removes noise
    mask = cv2.medianBlur(mask, 3)
    mask = cv2.dilate(mask, kernel, 8)
    #mask  = cv2.GaussianBlur(mask, (5,5), 0)

    mask_inv = 255-mask

    b, g, r = frame[:,:,0], frame[:, :, 1], frame[:, :, 2]
    b = cv2.bitwise_and(b, mask_inv)
    g = cv2.bitwise_and(g, mask_inv)
    r = cv2.bitwise_and(r, mask_inv)
    non_cloak_area = cv2.merge((b, g, r))

    b, g, r = cv2.split(background)
    cloak_area = cv2.merge((cv2.bitwise_and(b, mask), cv2.bitwise_and(g, mask), cv2.bitwise_and(r, mask)))

    output = cv2.bitwise_or(non_cloak_area, cloak_area)

    return output

def generate_frames():
    global cap
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        log("Error: Camera Not Found")
        return
    
    kernel = np.ones((3,3), np.uint8)

    init_frame = capture_background(cap, delay = 0.05, num_frames = 60)
    if init_frame is None:
        log("Failed to Capture Background")
        return

    log("Background Captured.")
    log("Please position your cloak in the center of frame for calibration and wait for 5 seconds")
    time.sleep(5)

    ret, frame = cap.read()

    if not ret:
        log("Failed to capture frame for calibration")
        return

    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_hsv, upper_hsv = auto_calibrate(hsv_frame, tol_h=10, tol_s =50 , tol_v=50)

    log("Invisibilty effect is active.")
    while True:
        ret, frame = cap.read()
        if not ret:
            log("Error, can't capture frame")
            break
        
        final = process_frame(frame, init_frame, lower_hsv, upper_hsv, kernel)
        _, buffer = cv2.imencode('.jpg', final)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n'+ frame_bytes + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/camera')
def camera():
    return render_template('camera.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/stop_stream', methods=['POST'])
def stop_stream():
    global cap, log_messages
    if cap is not None:
        cap.release()
        cv2.destroyAllWindows()
        cap = None
    log_messages = []
    return '', 204

@app.route('/logs')
def get_logs():
    return jsonify(log_messages)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)