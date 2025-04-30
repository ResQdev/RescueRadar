from flask import Flask
from models import db, User
import os
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash

load_dotenv()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = os.getenv("SECRET_KEY", "fallback_secret")

db.init_app(app)

with app.app_context():
    db.create_all()
    print("🚨 Tabellen erstellt (ohne Benutzer) 🚨")

    admin_username = os.getenv("ADMIN_USERNAME", "admin")
    admin_password = os.getenv("ADMIN_PASSWORD", "admin123")
    vehicle_id = "ADMIN-CTRL"

    # Nur hinzufügen, wenn dieser Benutzer noch nicht existiert
    if not User.query.filter_by(username=admin_username).first():
        admin_user = User(username=admin_username, vehicle_id=vehicle_id)
        admin_user.password = admin_password  # wird automatisch gehasht über @password.setter
        db.session.add(admin_user)
        db.session.commit()
        print(f"✅ Admin-Benutzer '{admin_username}' erfolgreich angelegt.")
    else:
        print(f"ℹ️ Admin-Benutzer '{admin_username}' existiert bereits.")
