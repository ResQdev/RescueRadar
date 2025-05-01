from flask import Flask, render_template, request, redirect, url_for, session, jsonify
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

# SQL-Datenbank konfigurieren
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

from admin_routes import admin_bp
app.register_blueprint(admin_bp)

with app.app_context():
    db.create_all()

# Login & Startseite
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

# Dashboard
@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("index"))
    user = db.session.get(User, session["user_id"])
    return render_template("dashboard.html", vehicle_id=user.vehicle_id)

# Standortupdate Einsatzfahrzeug
@app.route("/update_location", methods=["POST"])
def update_location():
    if "user_id" not in session:
        return "Nicht angemeldet", 403

    data = request.json
    vehicle_id = data["vehicle_id"]

    # Sicherheitscheck: Behördenfahrzeuge dürfen nicht mit "session-" beginnen
    if vehicle_id.startswith("session-"):
        return "Ungültige vehicle_id", 400

    new_location = Location(
        vehicle_id=vehicle_id,
        latitude=data["latitude"],
        longitude=data["longitude"]
    )
    db.session.add(new_location)
    db.session.commit()
    return "OK", 200

# Logout
@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('index'))

# Standortupdate Endnutzer + Matching
@app.route("/update_location_public", methods=["POST"])
def update_location_public():
    data = request.json

    # Session ID aus Request oder neu generieren
    session_id = data.get("session_id") or f"session-{uuid.uuid4()}"

    lat_user = float(data["latitude"])
    lon_user = float(data["longitude"])

    # Fahrzeuge der letzten 60 Sekunden abrufen (nur Behördenfahrzeuge)
    cutoff_vehicle = datetime.now(timezone.utc) - timedelta(seconds=60)
    vehicle_locations = Location.query.filter(
        Location.timestamp >= cutoff_vehicle,
        ~Location.vehicle_id.like("session-%")
    ).all()

    def haversine(lat1, lon1, lat2, lon2):
        R = 6371000  # Erdradius in Metern
        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        dphi = math.radians(lat2 - lat1)
        dlambda = math.radians(lon2 - lon1)
        a = math.sin(dphi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2)**2
        return R * (2 * math.atan2(math.sqrt(a), math.sqrt(1 - a)))

    nearby = False
    for vehicle in vehicle_locations:
        distance = haversine(lat_user, lon_user, vehicle.latitude, vehicle.longitude)
        if distance <= 100:
            nearby = True
            break

    # Nutzer-Standort speichern
    user_entry = Location(
        vehicle_id=session_id,
        latitude=lat_user,
        longitude=lon_user
    )
    db.session.add(user_entry)

    # Alte Endnutzer-Einträge (älter als 5 Minuten) löschen (Fallback)
    cutoff_user = datetime.now(timezone.utc) - timedelta(minutes=5)
    db.session.query(Location).filter(
        Location.vehicle_id.like("session-%"),
        Location.timestamp < cutoff_user
    ).delete()

    db.session.commit()

    return jsonify({"nearby": nearby}), 200

# Tracking beenden
@app.route("/stop_tracking", methods=["POST"])
def stop_tracking():
    data = request.json
    session_id = data.get("session_id")

    if session_id and session_id.startswith("session-"):
        locations = Location.query.filter_by(vehicle_id=session_id).all()
        for loc in locations:
            db.session.delete(loc)
        db.session.commit()
        return "OK", 200

    return "Ungültige Session-ID", 400

# Einsatzdaten löschen bei „Einsatz beenden“
@app.route("/stop_mission", methods=["POST"])
def stop_mission():
    if "user_id" not in session:
        return "Nicht angemeldet", 403

    import json

    # Unterstützung für JSON via sendBeacon (text/plain)
    try:
        data = request.get_json(force=True)
    except:
        data = json.loads(request.data.decode())

    vehicle_id = data.get("vehicle_id")


    if vehicle_id != session.get("vehicle_id"):
        return "Falsche Fahrzeug-ID", 403

    Location.query.filter_by(vehicle_id=vehicle_id).delete()
    db.session.commit()
    return "OK", 200

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0")