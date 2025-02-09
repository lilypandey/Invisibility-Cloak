# Invisibility Cloak (using OpenCV, Manual HSV Adjuster)

This project demonstrates an "Invisibility Cloak" effect using computer vision techniques in Python. It uses OpenCV to capture a video feed from your webcam, allows manual adjustment of HSV (Hue, Saturation, Value) thresholds via trackbars, and then processes the video to replace the area of a cloak with a pre-captured background, creating an invisibility effect.


## Features

- **Manual HSV Adjustment:**  
  Use trackbars to adjust the HSV thresholds for detecting the cloak.
  
- **Real-time Video Processing:**  
  Processes the live webcam feed and applies an invisibility effect by replacing the cloak area with a captured background.

- **Error Handling:**  
  Checks if the webcam is opened successfully before processing.


## Requirements

- Python
- OpenCV
- NumPy