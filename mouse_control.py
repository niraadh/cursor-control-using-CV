import cv2
import mediapipe as mp
import numpy as np
import pyautogui
import os

# Suppress TensorFlow and Mediapipe logs
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

# Screen dimensions for cursor mapping
screen_width, screen_height = pyautogui.size()

def is_touching(landmarks, frame):
    """Check if thumb and index finger are touching."""
    thumb_tip = np.array([landmarks[4][0], landmarks[4][1]])
    index_tip = np.array([landmarks[8][0], landmarks[8][1]])
    distance = np.linalg.norm(thumb_tip - index_tip)
    return distance < 20  # Adjust sensitivity as needed

def control_cursor():
    """Main function to control cursor using hand gestures."""
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not access webcam.")
        return

    click_active = False  # Prevent multiple clicks while fingers stay together

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            break

        frame = cv2.flip(frame, 1)  # Mirror image for natural control
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                landmarks = []
                for id, lm in enumerate(hand_landmarks.landmark):
                    x, y = int(lm.x * frame.shape[1]), int(lm.y * frame.shape[0])
                    landmarks.append((x, y))

                # Use wrist (id=0) or index finger base (id=5) to move cursor
                cursor_x = np.interp(landmarks[0][0], [100, frame.shape[1]-100], [0, screen_width])
                cursor_y = np.interp(landmarks[0][1], [100, frame.shape[0]-100], [0, screen_height])
                pyautogui.moveTo(cursor_x, cursor_y)

                # Left click when index and thumb touch
                if is_touching(landmarks, frame):
                    if not click_active:
                        pyautogui.click()
                        click_active = True
                else:
                    click_active = False

        # Display feed (optional)
        try:
            cv2.imshow("Cursor Control", frame)
        except cv2.error:
            pass  # Skip if OpenCV GUI not supported

        # Exit with 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    control_cursor()
