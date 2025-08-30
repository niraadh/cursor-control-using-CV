import cv2
import mediapipe as mp
import numpy as np
import pyautogui

# Initialize MediaPipe hands and drawing utilities
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils

# Get screen dimensions
screen_width, screen_height = pyautogui.size()

# Function to check if fingers are pinched for a click
def is_pinching(landmarks):
    thumb_tip = landmarks[4]
    index_tip = landmarks[8]

    # Calculate the distance between thumb tip and index tip
    distance = np.linalg.norm(np.array(thumb_tip) - np.array(index_tip))

    # If the distance is small, consider it as a pinching gesture
    return distance < 40  # Adjust this threshold if necessary

# Function to control mouse using hand gestures
def control_mouse():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    pinch_active = False  # Track if pinch gesture is currently active

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            break

        # Convert the frame to RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(frame_rgb)

        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                # Draw the hand landmarks on the frame
                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                wrist_position = hand_landmarks.landmark[0]
                wrist_x = int(wrist_position.x * frame.shape[1])
                wrist_y = int(wrist_position.y * frame.shape[0])

                # Define a smaller central region of the camera frame for tracking
                camera_x_min, camera_x_max = frame.shape[1] * 0.25, frame.shape[1] * 0.75
                camera_y_min, camera_y_max = frame.shape[0] * 0.25, frame.shape[0] * 0.75

                 # Map the wrist position in this smaller range to the full screen coordinates
                screen_x = np.interp(wrist_x, [camera_x_min, camera_x_max], [screen_width, 0])
                screen_y = np.interp(wrist_y, [camera_y_min, camera_y_max], [0, screen_height])

                # Move mouse to the mapped position
                pyautogui.moveTo(screen_x, screen_y)

                # Check for pinch gesture for clicking
                landmarks = [[id, lm.x * frame.shape[1], lm.y * frame.shape[0]]
                             for id, lm in enumerate(hand_landmarks.landmark)]
                
                if is_pinching(landmarks):
                   if not pinch_active:  # Trigger click on first pinch detection
                    pyautogui.click()
                    pinch_active = True  # Set pinch_active to prevent repeated clicks
                else:
                    pinch_active = False  # Reset pinch detection when gesture stops

        # Show the video feed with landmarks
        cv2.imshow('Hand Gesture Mouse Control', frame)

        # Exit the loop when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Main execution
if __name__ == "__main__":
    control_mouse()
