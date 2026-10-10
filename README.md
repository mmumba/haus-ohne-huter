# Haus ohne Hüter — interaktiver Figurenatlas

Figuren und Beziehungen in Heinrich Bölls Roman **Haus ohne Hüter** (1954) erkunden: Knoten verschieben, in das Netzwerk hineinzoomen und Beziehungen einzeln betrachten.

Der Viewer läuft vollständig **lokal und offline im Browser**. Kein Server, kein Neo4j, kein Benutzerkonto und keine Installation von JavaScript-Paketen erforderlich.

## Online öffnen

Der Figurenatlas wird über GitHub Pages veröffentlicht: [Figurenatlas öffnen](https://mmumba.github.io/haus-ohne-huter/).

Die Offline-Datei bleibt weiterhin verfügbar. Änderungen an der persönlichen Anordnung werden nicht für andere Besucher gespeichert.

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

**SVG exportieren** erzeugt ein skalierbares, statisches Bild der gesamten ausgewählten Ansicht mit Kantentexten. Die interaktive HTML-Version erlaubt zusätzlich das Verschieben von Knoten. Die Online-Version wird als statische Website auf GitHub Pages bereitgestellt.

## Daten und Quellenstatus

Der enthaltene Datenstand umfasst **45 Knoten und 141 Beziehungen**: 21 Figuren, zwei Familien, sieben Orte, fünf Ereignisse, neun Themen und das Werk. Die Standardansicht zeigt die 23 Figuren-/Familienknoten mit 71 Beziehungen.

Die Angaben beruhen auf einer vom Projektinitiator bereitgestellten Modellierungsvorgabe und wurden **nicht unabhängig am Primärtext geprüft**. `kanonisch` bezeichnet die Einordnung in dieser Vorgabe; es ist kein zusätzlicher Textnachweis. Interpretationen und Figurenwahrnehmungen sind separat markiert. Das Modell bezieht sich auf den Roman, nicht auf dessen Verfilmung.

Der Viewer enthält einen eingebetteten **Datenstand**, der vollständig offline funktioniert. Das Verschieben von Knoten ändert nur die Darstellung. Ein Editor zum Hinzufügen oder Ändern literarischer Fakten ist bisher nicht enthalten.

## Weiterentwickeln

Die Anwendung verwendet natives JavaScript, CSS und SVG, ohne React, externe Bibliotheken oder CDN-Abhängigkeiten.

| Datei | Zweck |
| --- | --- |
| `graph-viewer.template.html` | Editierbarer Quellcode für Oberfläche und Interaktion |
| `hoh_graph.json` | Knoten, Beziehungen und Eigenschaften |
| `package_viewer.py` | Bettet die Daten in die Vorlage ein und erzeugt HTML und ZIP |
| `haus-ohne-hueter-interaktiv.html` | Fertige, direkt ausführbare Anwendung |
| `haus-ohne-hueter-teilen.zip` | Dieselbe Anwendung als ZIP zum Weitergeben |

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

### Daten aktualisieren

`hoh_graph.json` ist die Datenquelle des Viewers. Eigenschaften und Beziehungen dort bearbeiten und anschließend `python package_viewer.py` ausführen. So werden HTML und ZIP mit dem aktualisierten Datenstand erstellt. Es ist keine Datenbank erforderlich.

### Ein anderes Netzwerk darstellen

Die JSON-Struktur besteht aus `nodes` mit `name`, `label`, `properties` sowie `relationships` mit `von`, `typ`, `zu`, `properties`. Namen müssen eindeutig sein; jede Beziehung muss auf vorhandene Knoten verweisen. Für andere Projekte müssen außerdem die derzeit romanspezifischen Texte, Ansichtsfilter, Farben und Startpositionen in der Vorlage angepasst werden.

## Feedback

Über **Feedback geben** im Viewer gelangst du zu einem [kurzen deutschen Google-Formular](https://docs.google.com/forms/d/e/1FAIpQLSfjob3Mv2FTE6_5Vf8izzlP9AREabSCRBCbGm1BkiiqZKbEsw/viewform?hl=de). Kein Google-Konto erforderlich; E-Mail-Adressen werden nicht gesammelt. Alle Fragen sind freiwillig. Bitte keine persönlichen Angaben eintragen. Antworten sind nicht öffentlich sichtbar. Das Formular wird in einem neuen Tab geöffnet; das übrige Programm funktioniert weiterhin offline.
