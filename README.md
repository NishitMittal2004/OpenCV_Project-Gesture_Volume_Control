# OpenCV Project - Gesture Volume Control
---
### Control your computer's volume using hand gestures captured through a webcam! This project utilizes Python, OpenCV, and the pycaw library to detect hand landmarks and adjust the system volume based on hand movements.

---
# How It Works
### The volume control project uses a combination of computer vision techniques and the pycaw library to interact with the Windows Core Audio API.

### 1. It captures video frames from the webcam using OpenCV.
### 2. The HandTrackingModule is used to detect hand landmarks and calculate the distance between specific landmarks (e.g., thumb and index finger).
### 3. The distance is mapped to the system volume range (-65 to 0 decibels) using interpolation.
### 4. The system volume is adjusted accordingly using the pycaw library.
### 5. The volume percentage and visual feedback (color-changing circle) are displayed on the screen.

---
### Mediapipe version used :- 0.8.3.1
