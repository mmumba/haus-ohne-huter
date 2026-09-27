# Interaktiven Figurenatlas teilen

Öffne `haus-ohne-hueter-interaktiv.html` per Doppelklick in Chrome, Edge oder Firefox. Kein Server, Internet, React-Setup oder Neo4j erforderlich. Alle 45 Knoten und 141 Beziehungen des hier erstellten Datenstands sind enthalten. Die Dateien enthalten keine Datenbank-Zugangsdaten.

Zum Versenden: `haus-ohne-hueter-teilen.zip` weitergeben. Empfänger entpacken die ZIP-Datei und öffnen die HTML-Datei im Browser. Manche Mailprogramme blockieren HTML-Anhänge; dann eine Dateiablage verwenden. Die lokale Vorschauadresse ist kein öffentlicher Link.

- Knoten mit der Maus verschieben; Hintergrund ziehen; mit dem Mausrad oder +/− zoomen.
- Figur anklicken oder suchen: verbundene Kanten werden hervorgehoben, die Seitenleiste zeigt vollständige Namen, Beziehungen und Eigenschaften.
- Mit „Gesamter Roman“ auch Orte, Themen, Ereignisse und Werk anzeigen.
- „Interaktive Kopie speichern“ erstellt eine neue HTML-Datei mit der aktuellen Knoten-Anordnung und Ansicht. Diese Datei weitergeben oder später wieder öffnen. Ungespeicherte Änderungen gehen beim Schließen verloren.
- „SVG exportieren“ exportiert die gesamte gewählte Ansicht einschließlich aller Kantentexte als skalierbares statisches Bild. Für frei verschiebbare Knoten die HTML-Datei verwenden.
- Per Tab einen Knoten fokussieren; Enter zeigt Details, Pfeiltasten verschieben ihn.

Dies ist eine offline lesbare Momentaufnahme aus `hoh_graph.json`, keine Live-Verbindung zur Datenbank. Anordnung ändern verändert keine Neo4j-Daten. Der Viewer enthält keinen Editor für Romanfakten. Spätere Datenbankänderungen erfordern einen neuen Datenexport und das erneute Ausführen von `package_viewer.py`.

## Workbench-Verbindung

Der Screenshot zeigt eine gespeicherte Verbindung mit `http://localhost:7474`. Das ist der HTTP-Port, nicht die Bolt-Verbindung. In der vorhandenen Verbindung „EDIT“ wählen:

- Connection URL: `bolt://localhost:7687`
- Database Name: `neo4j`
- Username: `neo4j`
- Password: das bereits in Neo4j Browser erfolgreich verwendete Datenbankpasswort
- Encrypted und Proxy: aus für diese lokale Verbindung

Speichern und „TEST“ klicken. Der Fehler „Unknown scheme: null“ betrifft die gespeicherte URL und ist kein Nachweis eines falschen Passworts.

Workbench verwendet zusätzlich ein eigenes Anwendungskonto. Das ist vom Neo4j-Datenbankkonto getrennt. Ein importiertes Workbench-Schemadiagramm ist kein Editor für die konkreten Figuren und Beziehungen dieser Momentaufnahme.
