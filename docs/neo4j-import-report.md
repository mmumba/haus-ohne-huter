# Haus ohne Hüter – Neo4j-Wissensgraph

Stand: 27. September 2026. Import in die lokale Datenbank `neo4j` erfolgreich über die authentifizierte Neo4j-Browser-Sitzung (Bolt-Verbindung). Keine Zugangsdaten in Dateien gespeichert.

## Ergebnis

- 45 neue Knoten: 21 Figuren, 2 Familien, 7 Orte, 5 Ereignisse, 9 Themen, 1 Werk.
- 141 neue gerichtete Beziehungen, darunter 44 Werkzuordnungen.
- Alle Projektknoten tragen `HOH`; alle Beziehungen besitzen `quelle: Roman` und `sicherheit`.
- Keine isolierten Knoten, doppelten Knotennamen, unbeschrifteten Knoten oder Verbindungen zu fremden Knoten.
- Martin–Heinrich-Freundschaft: genau eine gespeicherte, konzeptionell symmetrische Beziehung.
- Nella und Wilma sind innerhalb von höchstens sechs Beziehungen ausschließlich über Figuren verbunden.
- Fremdbestand vor und nach Import: 52 Knoten, 140 Beziehungen. Alle Schreiboperationen waren auf `HOH` beschränkt. Kein Reset und keine Löschung durchgeführt.
- Vollständige Graphansicht: 45 Knoten, 141 Beziehungen. Figurentabelle: 51 Beziehungen.

## Quellenstatus und Prüfpunkte

Die literarischen Angaben wurden aus `haus_ohne_hueter_codex_instructions.md` übernommen, nicht unabhängig am Roman geprüft. `kanonisch` bezeichnet die Einordnung laut dieser Vorgabe, keinen neu erbrachten Primärtextnachweis. Das zusätzliche Feld `belegstatus` hält diese Einschränkung auf jedem Knoten und jeder Beziehung fest. Es wurden keine Filmquellen ergänzt.

Als interpretativ markiert sind insbesondere Alberts Vaterrolle, Leos Beschämung Wilmas, Heinrichs Onkel-Kategorien, Wilmas Erwägungen zum Bäcker und zur Trennung sowie die thematischen Deutungen. Gäselers Motiv trägt separat `motiv_sicherheit: interpretativ`. Die unklaren Todesumstände von Vater Brielach bleiben ausdrücklich unsicher. Seiten- und Kapitelbelege können beim Weiterlesen ergänzt werden.

Zusätzliche Strukturbeziehungen ordnen Figuren ihren Familien bzw. deren Umfeld zu, verbinden die vorgegebenen Ereignisknoten und ordnen alle Elemente dem Werk zu. Die Werkzuordnungen verhindern technisch isolierte Knoten, ersetzen aber keine konkreten Szenenbelege. Russland/Ostfront und die unbenannte Rheinstadt haben bislang nur diese Werkzuordnung. Vier optionale Themen haben ebenfalls noch keine konkreten Figurenbeziehungen.

## Ansichten

Vollständiger Graph:

```cypher
MATCH p=(a:HOH)-[r]->(b:HOH) RETURN p;
```

Familien und Figuren, ohne den zentralen Werk-Knoten:

```cypher
MATCH p=(a:HOH)-[r]->(b:HOH)
WHERE (a:Figur OR a:Familie) AND (b:Figur OR b:Familie)
RETURN p;
```

Nur direkte Figurenbeziehungen:

```cypher
MATCH p=(a:HOH:Figur)-[r]->(b:HOH:Figur) RETURN p;
```

## Dateien und Wiederverwendung

- `hoh_graph.json`: vollständige Knoten- und Beziehungsliste mit Eigenschaften.
- `hoh_import.cypher`: atomare, wiederholbare MERGE-Abfrage. Keine Löschungen; keine Veränderung von Nicht-HOH-Knoten. Vor Wiederverwendung bestehende HOH-Daten auf Namensduplikate und manuelle Änderungen prüfen. Gleiche Eigenschaften werden durch den Import aktualisiert; zusätzliche bestehende Daten bleiben erhalten.
- `hoh_validate.cypher`: Validierungs- und Anzeigeabfragen, einzeln ausführen.
- `hoh_browser_queries.csv`: Browser-kompatible gespeicherte Import- und Validierungsabfragen; über „Upload“ im Queries-Bereich laden.
- `build_graph.py`: erzeugt JSON und Cypher erneut aus der ursprünglichen Anweisungsdatei und den expliziten Modellierungsregeln. Die CSV ist der gespeicherte Stand des erfolgreichen Imports.

Die Browser-Abfragen „HOH – Roman importieren“ und „HOH – Validierung“ wurden gespeichert.
