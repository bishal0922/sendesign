from flask import Flask, jsonify

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
    with open("index.html") as f:
        return f.read()

@app.route("/api/status", methods=["GET"])
def status():
    # Return the status data as JSON
    return jsonify(status_data)

if __name__ == "__main__":
    app.run(port=8080)
