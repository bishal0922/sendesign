import cv2
import mediapipe as mp
# Function to recognize gestures
def recognize_gesture(hand_landmarks):
    # Define the landmarks for each finger
    index_finger_tip = hand_landmarks[8]
    middle_finger_tip = hand_landmarks[12]
    ring_finger_tip = hand_landmarks[16]
    pinky_tip = hand_landmarks[20]
    thumb_tip = hand_landmarks[4]

     # Check if all fingers except thumb are up (No gesture)
    if index_finger_tip[1] > middle_finger_tip[1] and \
            index_finger_tip[1] > ring_finger_tip[1] and \
            index_finger_tip[1] > pinky_tip[1] and \
            thumb_tip[1] > index_finger_tip[1]:
        return "Gesture: No"

    # Check if only the index finger is up (Yes gesture)
    elif index_finger_tip[1] < middle_finger_tip[1] and \
            index_finger_tip[1] < ring_finger_tip[1] and \
            index_finger_tip[1] < pinky_tip[1] and \
            thumb_tip[1] < index_finger_tip[1]:
        return "Gesture: Yes"

    # If none of the recognized gestures
    else:
        return "No Gesture Detected"

# Initialize MediaPipe Hands model
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Capture video from webcam
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the image to RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame with MediaPipe Hands
    results = hands.process(frame_rgb)

    # If hands are detected
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Convert landmarks to list of tuples (x, y)
            hand_landmarks_list = [(int(l.x * frame.shape[1]), int(l.y * frame.shape[0])) for l in hand_landmarks.landmark]
            
            # Draw the landmarks on the frame
            for landmark in hand_landmarks_list:
                cv2.circle(frame, landmark, 5, (0, 255, 0), -1)

            # Recognize gesture
            gesture = recognize_gesture(hand_landmarks_list)
            cv2.putText(frame, gesture, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # Display the frame
    cv2.imshow('Hand Gesture Recognition', frame)

    # Check for key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()

# Release MediaPipe hands model
hands.close()
