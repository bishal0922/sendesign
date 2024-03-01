from flask import Flask, jsonify, render_template, Response, url_for
import cv2

app = Flask(__name__)

# Dummy data to mimic the Go struct
status_data = {
    "cupsInHand": 5,
    "cleanCups": 10,
    "usedCups": 3,
    "coffeeLeft": 1.5,  # Liters
    "batteryLevel": 80,  # Percentage
    "timeTillRefill": 2
}

@app.route("/")
def index():
    video_feed_url = url_for('video_feed')  # Get the URL for the video feed
    return render_template('index.html', video_feed_url=video_feed_url)

@app.route("/api/status", methods=["GET"])
def status():
    # Return the status data as JSON
    return jsonify(status_data)

def gen_frames():
    camera = cv2.VideoCapture(2)
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True)
