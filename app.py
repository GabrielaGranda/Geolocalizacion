from flask import Flask, request, jsonify
from flask_cors import CORS
import time, datetime

app = Flask(__name__)
CORS(app)  # Permite que tu frontend haga fetch desde otro dominio

# Guardamos ubicaciones en memoria
locations = {}  # { device_id: {lat, lng, accuracy, timestamp} }

# Guardamos check-ins y check-outs
check_times = {}  # { device_id: {"checkin": [...], "checkout": [...]} }

# -----------------------------
# Endpoint para recibir ubicación
# -----------------------------
@app.route("/receive_location", methods=["POST"])
def receive_location():
    data = request.json
    device_id = data.get("id")

    # Guardar la ubicación
    locations[device_id] = {
        "lat": data["lat"],
        "lng": data["lng"],
        "accuracy": data["accuracy"],
        "timestamp": int(time.time())
    }

    print(f"Recibido ubicación: {locations[device_id]}")  # Para debug en Render
    return jsonify({"status": "ok"})

# -----------------------------
# Endpoint para obtener ubicación actual
# -----------------------------
@app.route("/get_location/<device_id>")
def get_location(device_id):
    return jsonify(locations.get(device_id, {"error": "no data"}))

# -----------------------------
# Endpoint para check in / check out
# -----------------------------
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

    print(f"{check_type} para {device_id} a las {now}")  # Debug
    return jsonify({"status": "ok", "type": check_type, "timestamp": now})

# -----------------------------
# Endpoint para obtener check-ins / check-outs
# -----------------------------
@app.route("/get_checks/<device_id>")
def get_checks(device_id):
    if device_id not in check_times:
        return jsonify({"checkin": [], "checkout": []})
    return jsonify(check_times[device_id])

# -----------------------------
# Run
# -----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

