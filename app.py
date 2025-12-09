from flask import Flask, request, jsonify
from flask_cors import CORS
import time, datetime

app = Flask(__name__)
CORS(app)

locations = {}  # { id: {lat, lng, accuracy, timestamp} }
check_times = {}  # { id: {"checkin": [...], "checkout": [...]} }

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

# NUEVAS RUTAS para check in / out
@app.route("/check/<check_type>", methods=["POST"])
def check_action(check_type):
    data = request.json
    device_id = data.get("id")
    
    if check_type not in ["checkin", "checkout"]:
        return jsonify({"error": "tipo inválido"}), 400

    now = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

    if device_id not in check_times:
        check_times[device_id] = {"checkin": [], "checkout": []}

    check_times[device_id][check_type].append(now)

    return jsonify({"status": "ok", "type": check_type, "timestamp": now})

