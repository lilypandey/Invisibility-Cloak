import cv2
import numpy as np
import time

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
    print("Capturing Background. No one should be in frame")
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

def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Camera Not Found")
        exit()
    
    kernel = np.ones((3,3), np.uint8)

    init_frame = capture_background(cap, delay = 0.05, num_frames = 60)
    if init_frame is None:
        print("Failed to Capture Background")
        exit()

    print("Background Captured.")
    print("Please position your cloak in the center of frame for calibration and wait for 5 seconds")
    time.sleep(5)

    ret, frame = cap.read()

    if not ret:
        print("Failed to capture frame for calibration")
        exit()

    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_hsv, upper_hsv = auto_calibrate(hsv_frame, tol_h=10, tol_s =50 , tol_v=50)

    print("Invisibilty effect is active.")
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error, can't capture frame")
            break
        
        final = process_frame(frame, init_frame, lower_hsv, upper_hsv, kernel)
        cv2.putText(final, "Invisibility active! Press  'q' to exit.", (10, 30), cv2.FONT_ITALIC, 1, (0,0,0), 2, cv2.LINE_AA)
        cv2.imshow("Harry's Invisibility Cloak", final)

        if cv2.waitKey(3) == ord('q'):
            break

    cv2.destroyAllWindows()
    cap.release()

if __name__ == "__main__":
    main()
