# Haus ohne Hüter — interaktiver Figurenatlas

Figuren und Beziehungen in Heinrich Bölls Roman **Haus ohne Hüter** (1954) erkunden: Knoten verschieben, in das Netzwerk hineinzoomen und Beziehungen einzeln betrachten.

Der Viewer läuft vollständig **lokal und offline im Browser**. Kein Server, kein Neo4j, kein Benutzerkonto und keine Installation von JavaScript-Paketen erforderlich.

## Lokal starten

1. Dieses Repository mit GitHub Desktop oder Git klonen. Alternativ auf GitHub **Code → Download ZIP** wählen und die ZIP-Datei entpacken.
2. Die Datei **[haus-ohne-hueter-interaktiv.html](haus-ohne-hueter-interaktiv.html)** im heruntergeladenen Ordner per Doppelklick mit einem aktuellen Browser wie Chrome, Edge oder Firefox öffnen.
3. Fertig. Alle Daten und Funktionen sind in dieser Datei enthalten.

Mit Git:

```sh
git clone https://github.com/mmumba/haus-ohne-huter.git
cd haus-ohne-huter
```

Anschließend `haus-ohne-hueter-interaktiv.html` im Dateimanager öffnen. Eine Vorschau der HTML-Datei auf GitHub führt die Anwendung nicht aus; die Datei muss lokal geöffnet werden.

## Bedienung

- **Knoten ziehen:** Figuren auseinanderziehen und die Anordnung selbst gestalten.
- **Hintergrund ziehen:** den sichtbaren Ausschnitt verschieben.
- **Mausrad oder +/−:** hinein- und herauszoomen.
- **Figur auswählen:** direkte Beziehungen hervorheben und andere Bereiche ausblenden lassen. Eigenschaften und vollständige Beziehungstexte erscheinen rechts.
- **Kante auswählen:** Details zur Beziehung ansehen.
- **Suche:** eine Figur finden und zentrieren.
- **Ansicht:** zwischen Figuren, Figuren mit Familien und dem gesamten Romanmodell wechseln.
- **Alle Kantentexte:** sämtliche Bezeichnungen einblenden; bei dichten Netzen hilft die Auswahl einer einzelnen Figur.
- **Tastatur:** Knoten per Tab fokussieren, Enter für Details, Pfeiltasten zum Verschieben.

## Anordnung speichern und teilen

**Interaktive Kopie speichern** lädt eine neue HTML-Datei mit der aktuellen Anordnung und Ansicht herunter. Diese Datei lässt sich später wieder öffnen oder weitergeben. Ohne diesen Schritt gehen Änderungen an der Anordnung beim Schließen verloren.

Die Datei **haus-ohne-hueter-teilen.zip** enthält den mitgelieferten Viewer zum Weitergeben. Empfänger entpacken sie und öffnen die HTML-Datei. Einige E-Mail-Dienste blockieren HTML-Anhänge; dann die ZIP-Datei über eine Dateiablage weitergeben.

**SVG exportieren** erzeugt ein skalierbares, statisches Bild der gesamten ausgewählten Ansicht mit Kantentexten. Die interaktive HTML-Version erlaubt zusätzlich das Verschieben von Knoten. Es wird kein öffentlicher Server betrieben.

## Daten und Quellenstatus

Der enthaltene Datenstand umfasst **45 Knoten und 141 Beziehungen**: 21 Figuren, zwei Familien, sieben Orte, fünf Ereignisse, neun Themen und das Werk. Die Standardansicht zeigt die 23 Figuren-/Familienknoten mit 71 Beziehungen.

Die Angaben beruhen auf der [Modellierungsvorgabe](docs/graph-specification.md) und wurden **nicht unabhängig am Primärtext geprüft**. `kanonisch` bezeichnet die Einordnung in dieser Vorgabe; es ist kein zusätzlicher Textnachweis. Interpretationen und Figurenwahrnehmungen sind separat markiert. Das Modell bezieht sich auf den Roman, nicht auf dessen Verfilmung.

Der Viewer ist eine **Momentaufnahme**, keine Live-Verbindung zu Neo4j. Das Verschieben von Knoten ändert nur die Darstellung. Ein Editor zum Hinzufügen oder Ändern literarischer Fakten ist bisher nicht enthalten.

## Weiterentwickeln

Die Anwendung verwendet natives JavaScript, CSS und SVG, ohne React, externe Bibliotheken oder CDN-Abhängigkeiten.

| Datei | Zweck |
| --- | --- |
| `graph-viewer.template.html` | Editierbarer Quellcode für Oberfläche und Interaktion |
| `hoh_graph.json` | Knoten, Beziehungen und Eigenschaften |
| `package_viewer.py` | Bettet die Daten in die Vorlage ein und erzeugt HTML und ZIP |
| `haus-ohne-hueter-interaktiv.html` | Fertige, direkt ausführbare Anwendung |
| `build_graph.py` | Erzeugt den Ausgangsdatensatz und Cypher aus der Modellierungsvorgabe und den im Skript definierten Regeln |
| `hoh_import.cypher` | Wiederholbarer Import in eine eigene Neo4j-Datenbank |
| `hoh_validate.cypher` | Prüf- und Anzeigeabfragen für Neo4j |
| `hoh_browser_queries.csv` | Gespeicherte Neo4j-Browser-Abfragen des ursprünglichen Imports |
| `docs/neo4j-import-report.md` | Historischer Bericht des ursprünglichen lokalen Imports |
| `SHARING.md` | Weitere Hinweise zu Teilen und Workbench-Verbindungen |

### Viewer neu erzeugen

Für die Entwicklung wird **Python 3.9 oder neuer** benötigt; ausschließlich die Standardbibliothek wird verwendet. Python ist zum bloßen Öffnen des Viewers nicht notwendig.

Vorlage oder JSON bearbeiten, dann im Repository-Verzeichnis ausführen:

```sh
python package_viewer.py
```

Unter Windows funktioniert je nach Installation `py -3 package_viewer.py`, unter Linux/macOS `python3 package_viewer.py`. Danach die HTML-Datei neu öffnen oder im Browser neu laden. Quellcode und neu erzeugte HTML-/ZIP-Datei zusammen committen.

Optionaler lokaler Entwicklungsserver, falls gewünscht:

```sh
python -m http.server 8000 --bind 127.0.0.1
```

Dann `http://127.0.0.1:8000/haus-ohne-hueter-interaktiv.html` öffnen. Mit Strg+C beenden. Für den normalen Gebrauch ist dieser Server nicht erforderlich.

### Datensatz neu aufbauen

```sh
python build_graph.py
python package_viewer.py
```

**Achtung:** `build_graph.py` überschreibt `hoh_graph.json` und `hoh_import.cypher`. Direkte Änderungen am JSON vorher sichern oder in den Generator übernehmen. Die Browser-CSV ist ein historischer Export und wird von diesen Skripten nicht aktualisiert.

### Ein anderes Netzwerk darstellen

Die JSON-Struktur besteht aus `nodes` mit `name`, `label`, `properties` sowie `relationships` mit `von`, `typ`, `zu`, `properties`. Namen müssen eindeutig sein; jede Beziehung muss auf vorhandene Knoten verweisen. Für andere Projekte müssen außerdem die derzeit romanspezifischen Texte, Ansichtsfilter, Farben und Startpositionen in der Vorlage angepasst werden.

## Optional: Neo4j

Neo4j wird nur zur separaten Verwaltung des Wissensgraphen benötigt. Die Importabfrage legt alle Projektknoten unter `:HOH` an. Vor Verwendung bestehende Daten prüfen; wiederholte Imports aktualisieren übereinstimmende Eigenschaften. Keine Zugangsdaten in das Repository aufnehmen.

Für eine lokale Standardinstallation verwendet Workbench `bolt://localhost:7687`, Datenbank `neo4j`, Datenbankbenutzer `neo4j` und das eigene Datenbankpasswort. `http://localhost:7474` ist die Browser-/HTTP-Adresse und keine Bolt-Verbindungsadresse.
