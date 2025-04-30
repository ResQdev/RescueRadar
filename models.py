from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    vehicle_id = db.Column(db.String(50), unique=True, nullable=False)

    @property
    def password(self):
        raise AttributeError("Passwort kann nicht gelesen werden.")

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = generate_password_hash(plain_text_password)

    def verify_password(self, plain_text_password):
        return check_password_hash(self.password_hash, plain_text_password)

class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.String(50), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
