# Changelog

## [v1.2.1] – 2025-05-01

### 🗃️ Datenbankmigration

- 🔁 Datenbank von **db4free.net zu Railway** migriert
- 🚀 Neue `DATABASE_URL` mit stabilem Cloud-Host
- 🔐 Verbindung mit `pymysql` + SQLAlchemy optimiert
- 🧪 Fehlerhafte Verbindungsabbrüche (OperationalError) gehören der Vergangenheit an

### 🛠️ Verbesserungen

- Render `.env`-Management dokumentiert
- Lokale Tests vs. Cloud-Verhalten klar abgegrenzt
- Vorbereitung für Deployment-Doku und künftige Mobil-Integration

## [v1.2.0] – 2025-05-01

### 📡 Adaptives Tracking für Endnutzer

- 🚶‍♂️ Standort wird **alle 2 Sekunden** gesendet, wenn Bewegung erkannt wird (>5 m)
- 🕒 Bei Stillstand erfolgt Standortupdate **alle 10 Sekunden**
- ⛽ Reduziert Serverlast und unnötige Requests ohne Einbußen bei der Sicherheit
- 🧠 `getDistance()` nutzt Haversine-Formel für präzise Messung

### 🔊 Verbesserte Benutzerführung

- 🚨 **Warnmeldung blendet sich automatisch aus**, wenn nach 10 Sekunden keine Einsatzfahrzeuge mehr erkannt werden
- ⚠️ Keine Flackereffekte – intelligenter Timeout-Reset bei neuer Erkennung

---

Diese Version verbessert die Reaktionszeit und spart gleichzeitig Systemressourcen – ideal für mobile Nutzer.

## [v1.1.0] - 2025-05-01

### ✅ Verbesserte Datenintegrität & Session-Handling

- 🚑 **Einsatzdaten werden zuverlässig gelöscht**, auch wenn Nutzer den Einsatz nicht manuell beenden
- 🧠 **Race-Condition verhindert**, bei der Standortdaten nach dem Löschen erneut gespeichert wurden
- 🧹 `dashboard.html`: `toggleTracking()`-Funktion überarbeitet – Löschung wird abgewartet, bevor Tracking deaktiviert wird
- 🔄 `stop_mission`: JSON-Fallback für `navigator.sendBeacon()` implementiert → saubere Löschung auch bei Tab-Schließung
- 🧼 **Endnutzerdaten-Fallback** auf 5 Minuten reduziert → weniger Datenmüll

### 🔒 Stabilität & Sicherheit

- 🚨 Keine falsch-positiven Warnmeldungen mehr durch verwaiste Einsatzdaten
- 💡 Standortübertragung von Behördenfahrzeugen wird blockiert, wenn `vehicle_id` ungültig ist
- ✅ `clearInterval()` + `sendBeacon()` greifen zuverlässig ineinander

---

Diese Version macht RescueRadar deutlich robuster im Live-Betrieb.

## [1.0.3-rollback] - 2025-04-30
### Geändert
- WebSocket-Integration vollständig entfernt
- Rückkehr zur stabilen REST-basierten Standortübertragung
- Datenbankbereinigung bei Einsatzende erneut zuverlässig

## [v1.0.2] - 2025-04-30

- 🚦 **Session-ID-Erzeugung** für Endnutzer nur noch bei aktiver Standortübertragung
- ❌ **Alte Sessions** werden nach "Beenden" vollständig entfernt
- 📡 **WebSocket-Verbindung** wird dynamisch aufgebaut und sauber beendet
- 🔊 **Warnmeldung verschwindet automatisch** nach 10 Sekunden, wenn kein Fahrzeug mehr erkannt wird
- 🛠️ Diverse kleinere UI-Verbesserungen und Konsolenlogs für Debugging

Diese Version verbessert die Effizienz und Benutzerfreundlichkeit im Live-Betrieb erheblich.
## [1.0.3-rollback] - 2025-04-30
### Geändert
- WebSocket-Integration vollständig entfernt
- Rückkehr zur stabilen REST-basierten Standortübertragung
- Datenbankbereinigung bei Einsatzende erneut zuverlässig

## [v1.0.1]

### 🚀 Neue Funktionen
- Umstellung auf **WebSocket-Kommunikation** für Standortübertragung (statt REST)
- Echtzeitübermittlung von Fahrzeug- und Nutzerpositionen via `socket.io`
- **Session-basierte Zuordnung**: Behördenfahrzeuge mit Login, Endnutzer mit temporärer `session-ID`
- **Live-Radiusabgleich** mit 100 m Umkreis für Einsatzfahrzeuge

### 🔔 Verbesserte Warnlogik
- Warnmeldung (Text + Audio) bei Annäherung eines Einsatzfahrzeugs
- Visuelle und akustische Rückmeldung auf Endnutzerseite
- Automatische Entwarnung nach 10 Sekunden ohne neue Warnung

### 🧹 Automatisches Daten-Handling
- Automatische **Löschung von Endnutzer-Sessions** nach 10 Minuten
- **Fahrzeug-Trackingdaten** werden nach Klick auf „Einsatz beenden“ gelöscht

### 🐛 Bugfixes
- Deadlocks bei `DELETE`-Statements vermieden (kein Bulk-Delete mehr)
- Session-Zuweisung über `join_room()` bei WebSocket-Verbindung
- Verbesserte iOS-Kompatibilität durch Benutzerinteraktion vor Audiowiedergabe

## [v1.0.0] - 2025-04-30
### Neue Features
- Echtzeit-Standortübertragung via WebSocket
- Admin-Portal mit Benutzerverwaltung
- Öffentliche Warnung und Audioausgabe bei Annäherung von Einsatzfahrzeugen

### Removed
- Veraltete REST-Route /update_location_public
- REST-Route /update_location für Behördenfahrzeuge ersetzt durch WebSocket

### Changed
- Frontend (index.html & dashboard.html) vollständig WebSocket-basiert

## [v0.3.0] - 2025-04-28

### ✨ Neue Features
- Neuer **Tracking-Button** auf der Startseite: Endnutzer können nun das Standort-Tracking **manuell starten und beenden**.
- **Button-Status**: Wechsel zwischen „Starten“ (grün) und „Beenden“ (rot) mit fetter Beschriftung.
- Verbesserung der Benutzerkontrolle und Kompatibilität speziell für iOS-Geräte (Audio-Freigabe bei User-Interaktion).
- neue Warntöne in /static hinzugefügt, die aktuell über die index.html geändert werden können.

### 🔧 Verbesserungen
- Backend-Zeitmanagement wurde modernisiert:
  - Nutzung von **timezone-aware** Timestamps (`datetime.now(timezone.utc)`).
  - `timestamp`-Spalte der `location`-Tabelle auf `TIMESTAMP` Typ in MySQL umgestellt.
  - `models.py` aktualisiert: `timestamp = db.Column(db.DateTime(timezone=True))`.

### 🐛 Bugfixes
- Entfernung von `DeprecationWarning` bei Verwendung von `datetime.utcnow()`.

### 🧹 Cleanup
- Kleinere Code-Aufräumarbeiten und Vereinheitlichung der Zeit- und Tracking-Logik.

---

## Hinweise:
- Diese Version ist kompatibel mit zukünftigen Python-Versionen.
- Datenbankänderung erforderlich (`ALTER TABLE location MODIFY COLUMN timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP;`).

## [v0.2.2] - 2025-04-25

### ✨ Verbesserungen
- Dashboard für mobile Nutzung optimiert:
  - Überschrift "Dashboard" fixiert und hervorgehoben.
  - Fahrzeug-ID mittig (horizontal & vertikal) angezeigt.
  - Start/Stop-Button und Logout-Button fixiert am unteren Bildschirmrand, mit gleichmäßiger Breite und Touch-Optimierung.

## [v0.2.1] - 2025-04-24

### ✨ Verbesserungen
- Session-ID wird nun korrekt überschrieben, wenn ein Endgerät als Einsatzfahrzeug eingeloggt ist.
- Standortdaten von Endnutzern werden zuverlässiger als temporäre Sitzungseinträge behandelt.

### 🔊 Neue Features
- Warnsound bei Annäherung eines Einsatzfahrzeugs (MP3-Datei wird bei Aktivierung abgespielt)

### 🐛 Bugfixes
- Warnmeldungen wurden zuvor fälschlicherweise ausgelöst, auch wenn kein Einsatzfahrzeug in der Nähe war. Dieses Verhalten wurde behoben.
- Die Session-IDs für Endnutzer und Einsatzfahrzeuge wurden vereinheitlicht, um Konflikte zu vermeiden.

### 🧹 Cleanup
- Alte Standortdaten von Endnutzern werden nach 10 Minuten automatisch entfernt.


## [0.2.0] - 2025-04-24

### Added
- Standorttracking für Endnutzer implementiert (mit Session-ID)
- Abgleich mit Einsatzfahrzeugen im Radius von 100m
- Entfernung von Standortdaten nach 10 Minuten (public user)
- Neue API-Route `/update_location_public`

### Fixed
- Vereinheitlichung der Datenbankverbindung
- Importfehler in main.py bereinigt

### Changed
- `main.py` modularisiert
- Performance-Optimierungen durch gezieltes Löschen alter Daten
