# Changelog

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
