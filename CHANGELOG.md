# Changelog

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
