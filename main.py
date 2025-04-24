from flask import Flask, render_template, request, redirect, url_for, session
from models import db, User, Location
import time
import os

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "fallback_if_missing")

# SQL-Datenbank konfigurieren
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://rr_admin:Sch4ll3riku5@db4free.net/rescueradar_db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Datenbank mit App verbinden
db.init_app(app)

#Datenbanktabellen erstellen, falls nicht vorhanden
with app.app_context():
    db.create_all()

# Login & Startseite
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session["user_id"] = user.id
            session["vehicle_id"] = user.vehicle_id
            return redirect(url_for("dashboard"))
        else:
            return render_template("index.html", error="❌ Falsche Anmeldedaten")
    return render_template("index.html", error=None)

# Dashboard mit Radar-Button
@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("index"))
    user = User.query.get(session["user_id"])
    return render_template("dashboard.html", vehicle_id=user.vehicle_id)

# AJAX-Endpunkt für Standort-Update
@app.route("/update_location", methods=["POST"])
def update_location():
    if "user_id" not in session:
        return "Nicht angemeldet", 403
    data = request.json
    new_location = Location(
        vehicle_id=data["vehicle_id"],
        latitude=data["latitude"],
        longitude=data["longitude"]
    )
    db.session.add(new_location)
    db.session.commit()
    return "OK", 200

# App Route für Logout (Standortdaten entfernen)
@app.route('/logout', methods=['POST'])
def logout():
    if 'vehicle_id' in session:
        vehicle_id = session['vehicle_id']

        # Alle Einträge zu diesem Fahrzeug löschen
        Location.query.filter_by(vehicle_id=vehicle_id).delete()
        db.session.commit()

    session.clear()  # Session beenden
    return redirect(url_for('index'))  # Zurück zur Login-Page

# Datenbank einmalig beim Start erstellen
#@app.before_first_request
#def create_tables():
#    db.create_all()

# Alle Datenbankeinträge löschen (zum löschen unkommentieren)
#with app.app_context():
#    Location.query.delete()
#    db.session.commit()
#    print("Alle Location-Einträge wurden gelöscht.")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
