from flask import Flask, jsonify, render_template, Response, url_for
import cv2
import mediapipe as mp

app = Flask(__name__)

# Initialize MediaPipe Hands module
handsModule = mp.solutions.hands
drawingModule = mp.solutions.drawing_utils

# Initialize MediaPipe Hands object
hands = handsModule.Hands(static_image_mode=False, min_detection_confidence=0.7, min_tracking_confidence=0.7, max_num_hands=2)
# Dummy data to mimic the Go struct
status_data = {
    "cupsInHand": 5,
    "cleanCups": 10,
    "usedCups": 3,
    "coffeeLeft": 1.5,  # Liters
    "batteryLevel": 80,  # Percentage
    "timeTillRefill": 2
}

def recognize_gesture(hand_landmarks):
    if hand_landmarks is None:
        return "No hand landmarks detected"

    index_finger_tip = (hand_landmarks[8].x, hand_landmarks[8].y)
    middle_finger_tip = (hand_landmarks[12].x, hand_landmarks[12].y)
    ring_finger_tip = (hand_landmarks[16].x, hand_landmarks[16].y)
    pinky_tip = (hand_landmarks[20].x, hand_landmarks[20].y)
    thumb_tip = (hand_landmarks[4].x, hand_landmarks[4].y)


    print("Hand Landmarks:")
    print(f"Index Finger Tip:   ({index_finger_tip[0]:.4f}, {index_finger_tip[1]:.4f})")
    print(f"Middle Finger Tip:  ({middle_finger_tip[0]:.4f}, {middle_finger_tip[1]:.4f})")
    print(f"Ring Finger Tip:    ({ring_finger_tip[0]:.4f}, {ring_finger_tip[1]:.4f})")
    print(f"Pinky Tip:          ({pinky_tip[0]:.4f}, {pinky_tip[1]:.4f})")
    print(f"Thumb Tip:          ({thumb_tip[0]:.4f}, {thumb_tip[1]:.4f})")
    print()

    # Define other finger tips
    other_finger_tips = [index_finger_tip, middle_finger_tip, ring_finger_tip, pinky_tip]

    # Check gestures based on thumb and other finger positions
    if thumb_tip[1] > max([finger[1] for finger in other_finger_tips]):
        return "Gesture: Thumbs Down"
    elif thumb_tip[1] < min([finger[1] for finger in other_finger_tips]):
        return "Gesture: Thumbs Up"
    else:
        return "No Gesture Detected"

@app.route("/")
def index():
    video_feed_url = url_for('video_feed')  # Get the URL for the video feed
    return render_template('index.html', video_feed_url=video_feed_url)

@app.route("/api/status", methods=["GET"])
def status():
    # Return the status data as JSON
    return jsonify(status_data)

def gen_frames():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Flip the frame horizontally for better usability
        frame = cv2.flip(frame, 1)
        
        # Detect hands in the frame
        results = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        
        # Draw hand landmarks on the frame
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                drawingModule.draw_landmarks(frame, hand_landmarks, handsModule.HAND_CONNECTIONS)
                
                # Recognize gesture if landmarks are available
                if hand_landmarks is not None:
                    gesture = recognize_gesture(hand_landmarks.landmark)
                    print(gesture)

                    # Display recognized gesture on the video frame
                    cv2.putText(frame, gesture, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        # Encode the frame to JPEG format
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True)
