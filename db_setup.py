from flask import Flask
from models import db, User
import os
from dotenv import load_dotenv

load_dotenv()  # .env-Datei laden

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = os.getenv("SECRET_KEY", "fallback_secret")

db.init_app(app)

users = [
    {"username": "anna.schmidt", "password": "einsatz2025", "vehicle_id": "RTW-101"},
    {"username": "ben.mueller", "password": "feuerwehr42", "vehicle_id": "HLF-203"},
    {"username": "clara.meier", "password": "rettung!", "vehicle_id": "NEF-304"},
    {"username": "david.schulz", "password": "einsatzbereit", "vehicle_id": "KTW-112"},
    {"username": "eva.fischer", "password": "sos-evakuierung", "vehicle_id": "RTW-220"},
    {"username": "felix.wagner", "password": "rettung24", "vehicle_id": "GW-405"},
    {"username": "greta.hoffmann", "password": "notruf789", "vehicle_id": "RTW-330"},
    {"username": "henrik.braun", "password": "hilfeJETZT", "vehicle_id": "HLF-117"},
    {"username": "isabel.schneider", "password": "einsatzJETZT", "vehicle_id": "NEF-808"},
    {"username": "jan.lehmann", "password": "rescueRADAR", "vehicle_id": "KTW-909"}
]

with app.app_context():
    db.drop_all()
    db.create_all()
    for u in users:
        user = User(username=u["username"], password=u["password"], vehicle_id=u["vehicle_id"])
        db.session.add(user)
    db.session.commit()
    print("🚨 Datenbank und Benutzer erfolgreich erstellt.")

