# Invisibility Cloak (using OpenCV)

This is a Flask-based web application that creates an invisibility cloak effect using OpenCV. The app dynamically detects a chosen cloak color and replaces it with a pre-captured background.


## Features

- **Automatic HSV Adjustment:**  
  Automatically calculates HSV thresholds for detecting the cloak.
  
- **Real-time Video Processing:**  
  Processes the live webcam feed and applies an invisibility effect by replacing the cloak area with a captured background.

- **Error Handling:**  
  Checks if the webcam is opened successfully before processing.


## Requirements

- Python
- OpenCV
- NumPy
- HTML/CSS/Javascript
- Flask
