# RescueRadar 🚨

**RescueRadar** ist ein Proof-of-Concept für eine Web-Anwendung zur Erhöhung der Sicherheit im Straßenverkehr bei Einsatzfahrten. Ziel ist es, Verkehrsteilnehmer frühzeitig zu warnen, wenn sich ein Einsatzfahrzeug nähert.

![Logo](static/RescueRadar_v2.png)

## 🔍 Funktionen


- Behörden-Login mit Zugangsdaten, die über das Admin-Portal erstellt werden können
- Einsatz-Dashboard mit Start/Stopp-Button für die Standortübertragung
- Speicherung der Fahrzeugpositionen dynamisch (10 Sekunden bei Stillstand, 2 Sekunden bei Bewegung)
- Endbenutzeransicht mit automatischer Standorterkennung im Browser
- Tracking-Button für Endnutzer: Manuelles Starten und Stoppen der eigenen Standortübertragung
- **Live-Abgleich** zwischen Einsatzfahrzeugen und Endnutzern (Radius: 100 Meter)
- **Session-ID-Tracking** für Endnutzer ohne Login
- **Automatische Entfernung** der Endnutzerstandorte nach Beendigung des Trackings
- Warnhinweis auf der Startseite bei Annäherung eines Einsatzfahrzeugs im Radius von 100 m
- Automatische Löschung der Standortdaten:
    - Einsatzfahrzeug: Nach "Einsatz beenden"
    - Endnutzer: Nach Beendigung des Trackings
- **Admin-Portal** zur Verwaltung von Benutzern und Fahrzeugen
- **Responsive UI** für Desktop und mobile Geräte
- **Audio-Warnung** bei Gefahrensituation

## 🛠️ Tech Stack

- **Frontend:** HTML, CSS, Bootstrap 5, JavaScript
- **Backend:** Python 3, Flask
- **Datenbank:** SQLAlchemy + MySQL (oder SQLite für Tests)
- **Kommunikation:** REST-basierte Standortübertragung via AJAX

## ⚙️ Letzte Verbesserungen
- Rückkehr zur stabilen REST-Architektur (ohne WebSockets)
- Verlässliche Datenlöschung bei Einsatzende
- Verbesserte Browserkompatibilität und Session-Verwaltung
- Erweiterte mobile Optimierung (responsive Radar-Ansicht)
- Zeitmanagement vollständig auf UTC umgestellt (timezone=True)

## 🧪 Lokales Setup

```bash
# Voraussetzungen
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt

# .env Datei erstellen
cp .env.example .env  # falls vorhanden oder selbst anlegen

# Datenbank initialisieren
python db_setup.py

# Server starten
python main.py
```

## 🔐 Admin-Login (Beispiel)
Benutzername: `admin`  
Kennwort: *(aus deiner .env Datei)*

## 📁 Struktur

```plaintext
├── main.py              # Zentrale Anwendung (Flask + SocketIO)
├── models.py            # Datenbankmodelle
├── db_setup.py          # Initiales Setup für DB + Admin
├── templates/           # HTML-Dateien für Admin & UI
├── static/              # Warnsound, Logo, Favicon
├── requirements.txt     # Abhängigkeiten
└── .env                 # (nicht im Repo) Datenbank-URL & Secret
```

## 📦 Deployment

Die Anwendung läuft produktionsbereit auf:

- **Frontend + Backend:** [Render](https://render.com)
- **Datenbank:** [Railway (MySQL)](https://railway.app)

### 🔧 .env Datei (Beispiel)

```env
DATABASE_URL=mysql+pymysql://root:<PASSWORD>@tramway.proxy.rlwy.net:29341/railway
SECRET_KEY=dein_geheimer_schlüssel

## ⚠️ Hinweise

Dieses Projekt ist rein zu Testzwecken und zur Demonstration konzipiert.  
Es darf **ausschließlich** im Rahmen rechtlich zulässiger und ethischer Szenarien verwendet werden.

**Bei produktivem Einsatz sind folgende Punkte zu beachten:**
- Nutzung einer eigenen SQL-Datenbank
- Absicherung durch HTTPS und Authentifizierungsmechanismen
- Optimierung durch Redis, Load-Balancing, echte Geräte-IDs etc.

## 📄 Lizenz
Siehe [LICENSE](LICENSE)