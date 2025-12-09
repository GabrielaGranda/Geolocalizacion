from flask import Flask, request, jsonify
from flask_cors import CORS 
import time

app = Flask(__name__)
CORS(app)

# Aquí guardamos las ubicaciones en memoria:
locations = {}  # { "ABC123": {"lat":.., "lng":.., "timestamp":.. } }

@app.route("/receive_location", methods=["POST"])
def receive_location():
    data = request.json
    device_id = data.get("id")

    locations[device_id] = {
        "lat": data["lat"],
        "lng": data["lng"],
        "accuracy": data["accuracy"],
        "timestamp": int(time.time())
    }

    return jsonify({"status": "ok"})

@app.route("/get_location/<device_id>")
def get_location(device_id):
    return jsonify(locations.get(device_id, {"error": "no data"}))
