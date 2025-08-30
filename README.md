# Hand Gesture Mouse Control

This project allows you to control your computer mouse using hand gestures captured via webcam.
It uses **MediaPipe** for real-time hand tracking and **PyAutoGUI** to move the cursor and perform clicks.

---

## Features
- Cursor movement using **index finger**.
- **Left click** by pinching index finger and thumb together.
- Real-time webcam feed with visual hand landmarks.

---

## Requirements
- Python 3.8+
- Webcam
- Required Python packages (install via `requirements.txt`):
  - opencv-python
  - mediapipe
  - numpy
  - pyautogui

---

## Installation
1. Clone or download this repository.
2. Navigate to the project directory.
3. Install the required packages:
   ```bash
   pip install -r requirements.txt
