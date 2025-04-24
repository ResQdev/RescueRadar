# RescueRadar 🚨

**RescueRadar** ist ein Proof-of-Concept für eine Web-Anwendung zur Erhöhung der Sicherheit im Straßenverkehr bei Einsatzfahrten. Ziel ist es, Verkehrsteilnehmer frühzeitig zu warnen, wenn sich ein Einsatzfahrzeug nähert.

## 🔍 Funktionen

- Behörden-Login mit vordefinierten Zugangsdaten
- Einsatz-Dashboard mit Start/Stopp-Button für die Standortübertragung
- Speicherung der Fahrzeugpositionen alle 2 Sekunden
- Endbenutzeransicht mit automatischer Standorterkennung im Browser
- **Live-Abgleich** zwischen Einsatzfahrzeugen und Endnutzern (Radius: 100 Meter)
- **Session-ID-Tracking** für Endnutzer ohne Login
- **Automatische Entfernung** der Endnutzerstandorte nach 10 Minuten
- Warnhinweis auf der Startseite bei Annäherung eines Einsatzfahrzeugs
- Automatische Löschung der Einsatzstandorte nach Logout

## 🛠️ Tech Stack

- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Python (Flask)
- **Datenbank:** MySQL (über db4free.net, via SQLAlchemy)
- **Echtzeit:** Geolocation + Intervallabfragen (AJAX)
- **Deployment:** Render.com

## ⚠️ Hinweise

Dieses Projekt ist rein zu Testzwecken und zur Demonstration konzipiert. Es darf **ausschließlich** im Rahmen rechtlich zulässiger und ethischer Szenarien verwendet werden.

## 📦 Installation (lokal)

```bash
git clone https://github.com/dein-nutzername/rescueradar.git
cd rescueradar
pip install -r requirements.txt
python main.py