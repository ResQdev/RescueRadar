from models import db, Location
from flask import Flask

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://rr_admin:Sch4ll3riku5@db4free.net/rescueradar_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.session.query(Location).delete()
    db.session.commit()
    print("✅ Alle Location-Einträge gelöscht.")
