import eventlet
eventlet.monkey_patch()

from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, emit, join_room
from models import db, User, Location
from sqlalchemy import func
import os
from dotenv import load_dotenv
import uuid
import math
from datetime import datetime, timedelta, timezone

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "fallback_if_missing")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_pre_ping": True,       # prüft vor jedem Query ob die Verbindung noch lebt
    "pool_recycle": 280          # recycelt Verbindungen vor Ablauf (Sekunden)
}

db.init_app(app)
socketio = SocketIO(app, async_mode="eventlet")

from admin_routes import admin_bp
app.register_blueprint(admin_bp)

with app.app_context():
    db.create_all()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter_by(username=username).first()
        if user and user.verify_password(password):
            session["user_id"] = user.id
            session["vehicle_id"] = user.vehicle_id
            return redirect(url_for("dashboard"))
        else:
            return render_template("index.html", error="❌ Falsche Anmeldedaten")
    return render_template("index.html", error=None)

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("index"))
    user = db.session.get(User, session["user_id"])
    return render_template("dashboard.html", vehicle_id=user.vehicle_id)

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route("/stop_mission", methods=["POST"])
def stop_mission():
    if "user_id" not in session:
        return "Nicht angemeldet", 403

    data = request.json
    vehicle_id = data.get("vehicle_id")

    if vehicle_id != session.get("vehicle_id"):
        return "Falsche Fahrzeug-ID", 403

    # sicheres Löschen über ORM
    entries = Location.query.filter_by(vehicle_id=vehicle_id).all()
    deleted_count = 0
    for e in entries:
        db.session.delete(e)
        deleted_count += 1

    db.session.commit()
    print(f"🗑️ Einsatzdaten gelöscht: {deleted_count} Einträge für Fahrzeug {vehicle_id}", flush=True)

    return "OK", 200


@app.route("/stop_tracking", methods=["POST"])
def stop_tracking():
    data = request.json
    session_id = data.get("session_id")
    if not session_id or not session_id.startswith("session-"):
        return "Ungültige Sitzung", 400
    Location.query.filter_by(vehicle_id=session_id).delete()
    db.session.commit()
    return "OK", 200

@socketio.on("public_location_update")
def handle_public_location(data):
    session_id = data.get("session_id")
    lat_user = data.get("latitude")
    lon_user = data.get("longitude")

    if not session_id or not lat_user or not lon_user:
        print("⚠️ Ungültige Standortdaten empfangen", flush=True)
        return

    print(f"📥 Standort erhalten von {session_id}: {lat_user}, {lon_user}", flush=True)

    # Standort speichern
    entry = Location(vehicle_id=session_id, latitude=lat_user, longitude=lon_user)
    db.session.add(entry)

    # Alte Nutzer-Daten löschen (kein bulk-delete)
    cutoff = datetime.now(timezone.utc) - timedelta(minutes=10)
    old_entries = Location.query.filter(
        Location.vehicle_id.like("session-%"),
        Location.timestamp < cutoff
    ).all()

    deleted_count = 0
    for old in old_entries:
        db.session.delete(old)
        deleted_count += 1

    print(f"🧹 Alte Nutzerdaten gelöscht: {deleted_count}", flush=True)

    # Fahrzeuge der letzten 60 Sekunden
    cutoff_vehicle = datetime.now(timezone.utc) - timedelta(seconds=60)
    vehicles = Location.query.filter(
        Location.timestamp >= cutoff_vehicle,
        ~Location.vehicle_id.like("session-%")
    ).all()

    def haversine(lat1, lon1, lat2, lon2):
        R = 6371000
        phi1, phi2 = math.radians(lat1), math.radians(lat2)
        dphi = math.radians(lat2 - lat1)
        dlambda = math.radians(lon2 - lon1)
        a = math.sin(dphi/2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda/2)**2
        return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    for v in vehicles:
        distance = haversine(lat_user, lon_user, v.latitude, v.longitude)
        print(f"📏 Distanz zu {v.vehicle_id}: {distance:.2f} m", flush=True)
        if distance <= 100:
            print(f"🚨 WARNUNG an {session_id} — Fahrzeug in der Nähe: {v.vehicle_id}", flush=True)
            emit("warn_user", {"nearby": True}, to=session_id)
            break

    db.session.commit()
    emit("location_saved", {"status": "ok"})

@socketio.on("vehicle_location_update")
def handle_vehicle_location(data):
    vehicle_id = data.get("vehicle_id")
    lat = data.get("latitude")
    lon = data.get("longitude")

    if not vehicle_id or not lat or not lon:
        return

    entry = Location(vehicle_id=vehicle_id, latitude=lat, longitude=lon)
    db.session.add(entry)
    db.session.commit()

    emit("location_saved", {"status": "ok"})

@socketio.on("connect")
def on_connect():
    session_id = request.args.get("session_id")
    if session_id:
        join_room(session_id)
        print(f"🔗 WebSocket verbunden und Session-ID '{session_id}' dem Raum beigetreten", flush=True)
    else:
        print("⚠️ Keine session_id beim Verbindungsaufbau übergeben", flush=True)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # 5000 als Fallback für lokalen Betrieb
    socketio.run(app, host="0.0.0.0", port=port)