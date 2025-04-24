# RescueRadar 🚨

**RescueRadar** ist ein Proof-of-Concept für eine Web-Anwendung zur Erhöhung der Sicherheit im Straßenverkehr bei Einsatzfahrten. Ziel ist es, Verkehrsteilnehmer frühzeitig zu warnen, wenn sich ein Einsatzfahrzeug nähert.

## 🔍 Funktionen

- Behörden-Login mit vordefinierten Zugangsdaten
- Einsatz-Dashboard mit Start/Stopp-Button für Standortübertragung
- Speicherung der Fahrzeugpositionen alle 2 Sekunden
- Endbenutzeransicht mit automatischer Standorterkennung
- Warnhinweis bei Annäherung eines Einsatzfahrzeugs (Radius: 100 Meter)
- Automatische Löschung der Standortdaten nach Logout der Einsatzkraft

## 🛠️ Tech Stack

- Frontend: HTML, CSS, JavaScript
- Backend: Python (Flask)
- Datenbank: SQLite (via SQLAlchemy)
- Echtzeitkommunikation: WebSockets
- Deployment: Render.com

## ⚠️ Hinweise

Dieses Projekt ist rein zu Testzwecken und zur Demonstration konzipiert. Es darf **ausschließlich** im Rahmen rechtlich zulässiger und ethischer Szenarien verwendet werden.

## 📦 Installation (lokal)

```bash
git clone https://github.com/dein-nutzername/rescueradar.git
cd rescueradar
pip install -r requirements.txt
python main.py
