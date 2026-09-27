# Codex Instructions: Build and Maintain the *Haus ohne Hüter* Neo4j Knowledge Graph

## Objective

Work directly against the user's local Neo4j database and iteratively build a **German-language knowledge graph for Heinrich Böll's novel _Haus ohne Hüter_**.

The graph must model the **novel only**. Do **not** mix in facts, scenes, emphases, or reinterpretations from the 1975 film adaptation unless the user explicitly asks for a separate film graph later.

The preferred workflow is to connect directly to Neo4j over Bolt, inspect the existing database state, safely isolate the literature graph from unrelated pre-existing data, load the corrected graph, validate it, and then iterate with the user.

---

# 1. Local Neo4j connection

Use the local Neo4j instance:

- Browser: `http://localhost:7474/browser/`
- Bolt: `bolt://localhost:7687`
- Database: `neo4j`
- Username observed in Neo4j Browser: `neo4j`

Do **not** hard-code the password in source files.

Prefer one of these access methods:

## Preferred: Python Neo4j driver

```bash
pip install neo4j
```

Example connection:

```python
import os
from neo4j import GraphDatabase

uri = "bolt://localhost:7687"
user = "neo4j"
password = os.environ["NEO4J_PASSWORD"]

driver = GraphDatabase.driver(uri, auth=(user, password))

with driver.session(database="neo4j") as session:
    print(session.run("RETURN 1 AS ok").single()["ok"])
```

If needed, ask the user to set:

```bash
export NEO4J_PASSWORD='...'
```

or the equivalent environment variable on Windows.

## Alternative: `cypher-shell`

If installed:

```bash
cypher-shell -a bolt://localhost:7687 -u neo4j -p "$NEO4J_PASSWORD"
```

---

# 2. Critical safety rule

The `neo4j` database already contains an unrelated pre-existing graph with labels such as:

- `DataModel`
- `Feature`
- `Tool`
- `SoftwareEdition`
- `GraphDoc`
- `GraphDocMetadata`
- `CypherBuilder`
- `NodeLabel`
- `RelationshipType`
- etc.

**Never delete or modify that graph.**

All nodes created for this literature project must carry the label:

```text
:HOH
```

Example:

```cypher
(:HOH:Figur)
(:HOH:Familie)
(:HOH:Ort)
(:HOH:Ereignis)
(:HOH:Werk)
```

This makes the project logically isolated inside the shared Neo4j database.

All destructive operations must target `:HOH` only.

Safe reset:

```cypher
MATCH (n:HOH)
DETACH DELETE n;
```

Never run:

```cypher
MATCH (n)
DETACH DELETE n;
```

---

# 3. Modeling principles

Use German node labels, German relationship types, and German semantic properties wherever practical.

Recommended labels:

```text
:Werk
:Figur
:Familie
:Ort
:Ereignis
:Thema
```

Every project node also gets:

```text
:HOH
```

Recommended common properties:

```text
name
rolle
beruf
status
bemerkung
quelle
sicherheit
```

Use:

```text
quelle: "Roman"
```

for relationships and facts.

Where a relationship is interpretive rather than purely factual, add for example:

```text
sicherheit: "interpretativ"
```

Where it is directly supported by the text:

```text
sicherheit: "kanonisch"
```

---

# 4. Important Cypher implementation rule

Do **not** create nodes in one statement and then reuse variable names in later statements without matching them again.

This was the cause of the earlier malformed graph.

Wrong pattern:

```cypher
MERGE (nella:Figur {name:'Nella Bach'});
MERGE (martin:Figur {name:'Martin Bach'});
MERGE (nella)-[:IST_MUTTER_VON]->(martin);
```

Variables do not survive statement boundaries.

Correct pattern:

```cypher
MERGE (:HOH:Figur {name:'Nella Bach'});
MERGE (:HOH:Figur {name:'Martin Bach'});

MATCH
  (nella:HOH:Figur {name:'Nella Bach'}),
  (martin:HOH:Figur {name:'Martin Bach'})
MERGE (nella)-[:IST_MUTTER_VON {
  quelle:'Roman',
  sicherheit:'kanonisch'
}]->(martin);
```

---

# 5. Core graph topology

The graph should visually form two main communities:

```text
Familie Bach  <---- Martin Bach ---- IST_FREUND_VON ---- Heinrich Brielach ----> Familie Brielach
```

The friendship between **Martin Bach** and **Heinrich Brielach** is the most important bridge between the two family subgraphs.

Albert forms additional social bridges.

---

# 6. Nodes to create

## Werk

```cypher
(:HOH:Werk {
  name:'Haus ohne Hüter',
  autor:'Heinrich Böll',
  erscheinungsjahr:1954
})
```

## Familie Bach / Umfeld

Create these `:HOH:Figur` nodes:

```text
Nella Bach
Raimund Bach
Martin Bach
Martins Großmutter
Albert Muchow
Will
Glumbich Cholokusteban
Bolda
Pater Willibrord
Schurbigel
Gäseler
```

Recommended properties:

### Nella Bach
```text
rolle: "Mutter von Martin; Witwe von Raimund"
```

### Raimund Bach
```text
rolle: "Dichter / Schriftsteller"
status: "im Zweiten Weltkrieg gefallen"
```

### Martin Bach
```text
rolle: "Kind; Hauptfigur / Perspektivfigur"
```

### Martins Großmutter
```text
rolle: "Mutter von Nella; Großmutter von Martin"
bemerkung: "wohlhabende Fabrikantenfamilie / Marmeladenfabrik"
```

### Albert Muchow
```text
rolle: "enge Bezugsperson der Familie Bach"
beruf: "Witzzeichner / Zeichner"
bemerkung: "arbeitete früher mit Raimund als Zeichner in der Marmeladenfabrik"
```

### Will
```text
rolle: "Onkel von Martin; ältere stabile Bezugsperson"
```

### Glumbich Cholokusteban
```text
alias: "Glum"
rolle: "männlicher Hausgenosse / Freund des Bach-Umfelds"
bemerkung: "angelt; ehemaliger Lagerinsasse"
```

### Bolda
```text
rolle: "alte Freundin von Martins Großmutter"
```

### Pater Willibrord
```text
beruf: "katholischer Geistlicher"
```

### Schurbigel
```text
rolle: "Redner / Kulturintellektueller / Literaturbetrieb"
bemerkung: "veröffentlichte 1935 ein Gedicht Raimund Bachs; Dissertation 1934: 'Unser Führer in der modernen Lyrik'"
```

### Gäseler
```text
rolle: "ehemaliger Leutnant; später im Literaturbetrieb"
bemerkung: "Raimunds militärischer Vorgesetzter"
```

## Familie Brielach / Umfeld

Create:

```text
Wilma Brielach
Heinrich Brielach
Wilma Brielach (Tochter)
Vater Brielach
Leo
Der Bäcker
Erich
Gert
Karl
Frau Borussiak
```

Recommended properties:

### Wilma Brielach
This is Frau Brielach, Heinrich's mother.

```text
rolle: "Mutter von Heinrich und Wilma"
bemerkung: "Vorname im Roman ausdrücklich als Wilma belegt"
```

### Heinrich Brielach
```text
rolle: "Kind; Hauptfigur / Perspektivfigur"
```

### Wilma Brielach (Tochter)
```text
rolle: "kleine Halbschwester von Heinrich"
```

### Vater Brielach
```text
beruf: "Autoschlosser"
status: "im Krieg gefallen / verschollen; Todesumstände unsicher"
```

### Leo
```text
beruf: "Straßenbahnschaffner"
rolle: "Partner von Wilma Brielach; Vater der kleinen Wilma"
```

### Der Bäcker
```text
beruf: "Bäcker"
rolle: "Arbeitgeber und Verehrer von Wilma Brielach"
```

### Erich / Gert / Karl
```text
rolle: "frühere Partner / 'Onkel' im Umfeld von Heinrichs Mutter"
```

### Frau Borussiak
```text
rolle: "Bekannte / Betreuungsperson im Umfeld der Brielachs"
```

---

# 7. Places and institutions

Create these `:HOH:Ort` nodes:

```text
Bambergers Nudelfabrik
Marmeladenfabrik
Bäckerei
Bietenhahn
Odessa
Russland / Ostfront
nicht näher bezeichnete Stadt am Rhein
```

Suggested properties:

### Bietenhahn
```text
typ: "fiktiver Ort"
bemerkung: "Schutz- und Gegenraum für die Kinder"
```

### Odessa
```text
bemerkung: "Militärgefängnis-Kontext während des Krieges"
```

---

# 8. Key event nodes

Create `:HOH:Ereignis` nodes for events where direct person-to-person edges would oversimplify causality.

Recommended:

```text
Raimunds letzter Patrouillengang
Tod Raimunds
Albert schlägt Gäseler
Alberts Haft in Odessa
Aufenthalt der Kinder in Bietenhahn
```

---

# 9. Canonical relationship set

All relationship names below must remain in German.

## Family Bach

```cypher
(Nella Bach)-[:IST_MUTTER_VON]->(Martin Bach)

(Raimund Bach)-[:IST_VATER_VON]->(Martin Bach)

(Nella Bach)-[:WAR_VERHEIRATET_MIT]->(Raimund Bach)

(Martins Großmutter)-[:IST_MUTTER_VON]->(Nella Bach)

(Martins Großmutter)-[:IST_GROSSMUTTER_VON]->(Martin Bach)

(Will)-[:IST_ONKEL_VON]->(Martin Bach)

(Bolda)-[:IST_FREUNDIN_VON]->(Martins Großmutter)

(Glumbich Cholokusteban)-[:GEHOERT_ZUM_UMFELD_VON]->(Familie Bach)

(Albert Muchow)-[:GEHOERT_ZUM_UMFELD_VON]->(Familie Bach)

(Pater Willibrord)-[:GEHOERT_ZUM_UMFELD_VON]->(Familie Bach)

(Schurbigel)-[:GEHOERT_ZUM_UMFELD_VON]->(Familie Bach)

(Gäseler)-[:GEHOERT_ZUM_UMFELD_VON]->(Familie Bach)
```

## Main bridge between the two family communities

```cypher
(Martin Bach)-[:IST_FREUND_VON]->(Heinrich Brielach)
```

Treat this as conceptually symmetric even if stored as a single directed edge.

## Albert relationships

```cypher
(Albert Muchow)-[:IST_FREUND_VON]->(Raimund Bach)

(Albert Muchow)-[:DIENTE_MIT]->(Raimund Bach)

(Albert Muchow)-[:IST_VATERFIGUR_FUER]->(Martin Bach)

(Albert Muchow)-[:IST_VERTRAUENSPERSON_FUER]->(Heinrich Brielach)

(Albert Muchow)-[:UEBERNIMMT_FUERSORGE_FUER]->(Wilma Brielach (Tochter))

(Albert Muchow)-[:LIEBT]->(Nella Bach)

(Albert Muchow)-[:MOECHTE_HEIRATEN]->(Nella Bach)

(Nella Bach)-[:LEHNT_HEIRAT_MIT_AB]->(Albert Muchow)
```

## Raimund / Gäseler / war

Prefer an event model:

```cypher
(Gäseler)-[:WAR_VORGESETZTER_VON]->(Raimund Bach)

(Gäseler)-[:ORDNET_AN]->(Raimunds letzter Patrouillengang)

(Raimund Bach)-[:NIMMT_TEIL_AN]->(Raimunds letzter Patrouillengang)

(Raimunds letzter Patrouillengang)-[:FUEHRT_ZU]->(Tod Raimunds)

(Tod Raimunds)-[:BETRIFFT]->(Raimund Bach)
```

Add:
```text
motiv: "eitler Eigensinn / verletzte Autorität"
```

Do not model:
```text
Gäseler -[:IST_MOERDER_VON]-> Raimund
```

## Albert / Gäseler

```cypher
(Albert Muchow)-[:SCHLAEGT_INS_GESICHT]->(Gäseler)

(Albert Muchow)-[:WIRD_INHAFTIERT_IN]->(Odessa)
```

Recommended properties:
```text
dauer: "sechs Monate"
grund: "Ohrfeige / Schlag gegen Gäseler"
```

## Nella / Gäseler

```cypher
(Gäseler)-[:VERSUCHT_ZU_EROBERN]->(Nella Bach)

(Nella Bach)-[:HASST]->(Gäseler)

(Nella Bach)-[:HEGT_RACHEFANTASIEN_GEGEN]->(Gäseler)
```

Do not model this as a murder plan.

## Gäseler / Raimund's work

```cypher
(Gäseler)-[:INTERESSIERT_SICH_FUER_WERK_VON]->(Raimund Bach)
```

## Schurbigel / Raimund / Nella

```cypher
(Schurbigel)-[:VEROEFFENTLICHTE_GEDICHT_VON]->(Raimund Bach)

(Schurbigel)-[:BEZEICHNET_SICH_ALS_ENTDECKER_VON]->(Raimund Bach)

(Schurbigel)-[:BESUCHT_REGELMAESSIG]->(Nella Bach)

(Nella Bach)-[:HASST]->(Schurbigel)
```

Recommended edge property:
```text
jahr: 1935
```

## Pater Willibrord

```cypher
(Pater Willibrord)-[:KENNT]->(Nella Bach)

(Pater Willibrord)-[:KENNT]->(Schurbigel)

(Pater Willibrord)-[:STELLT_VOR]->(Gäseler)
```

For the introduction to Nella, a cleaner event-oriented model is:

```cypher
(Pater Willibrord)-[:STELLT_VOR]->(Gäseler)
(Gäseler)-[:WIRD_VORGESTELLT_BEI]->(Nella Bach)
```

---

# 10. Family Brielach relationships

## Core family

```cypher
(Wilma Brielach)-[:IST_MUTTER_VON]->(Heinrich Brielach)

(Vater Brielach)-[:IST_VATER_VON]->(Heinrich Brielach)

(Wilma Brielach)-[:IST_MUTTER_VON]->(Wilma Brielach (Tochter))

(Leo)-[:IST_VATER_VON]->(Wilma Brielach (Tochter))

(Heinrich Brielach)-[:IST_HALBBRUDER_VON]->(Wilma Brielach (Tochter))
```

## Wilma Brielach / Leo

```cypher
(Wilma Brielach)-[:LEBT_MIT]->(Leo)

(Leo)-[:BESCHAEMT]->(Wilma Brielach)
```

Mark the second as:
```text
sicherheit: "interpretativ"
```

## Earlier "Onkel" partners

```cypher
(Erich)-[:HATTE_BEZIEHUNG_MIT]->(Wilma Brielach)

(Gert)-[:HATTE_BEZIEHUNG_MIT]->(Wilma Brielach)

(Karl)-[:HATTE_BEZIEHUNG_MIT]->(Wilma Brielach)
```

Optional character-perception relationships:

```cypher
(Heinrich Brielach)-[:SIEHT_ALS_VEREINIGUNGSONKEL]->(Erich)
(Heinrich Brielach)-[:SIEHT_ALS_VEREINIGUNGSONKEL]->(Gert)
(Heinrich Brielach)-[:SIEHT_ALS_VEREINIGUNGSONKEL]->(Karl)
(Heinrich Brielach)-[:SIEHT_ALS_VEREINIGUNGSONKEL]->(Leo)
```

## Will as contrast category

```cypher
(Heinrich Brielach)-[:SIEHT_ALS_RICHTIGEN_ONKEL]->(Will)
```

---

# 11. Wilma Brielach / work / Bäcker

```cypher
(Wilma Brielach)-[:ARBEITETE_IN]->(Bambergers Nudelfabrik)

(Wilma Brielach)-[:ARBEITET_BEI]->(Der Bäcker)

(Der Bäcker)-[:ARBEITET_IN]->(Bäckerei)

(Der Bäcker)-[:BEGEHRT]->(Wilma Brielach)

(Der Bäcker)-[:WIRBT_UM]->(Wilma Brielach)

(Wilma Brielach)-[:ERWAEGT_BEZIEHUNG_MIT]->(Der Bäcker)

(Wilma Brielach)-[:ERWAEGT_TRENNUNG_VON]->(Leo)
```

For the last two:
```text
sicherheit: "interpretativ / gedanklich erwogen"
```

---

# 12. Work history involving Raimund and Albert

```cypher
(Raimund Bach)-[:ARBEITETE_IN]->(Marmeladenfabrik)

(Albert Muchow)-[:ARBEITETE_IN]->(Marmeladenfabrik)

(Albert Muchow)-[:ARBEITETE_MIT]->(Raimund Bach)
```

---

# 13. Bietenhahn

Create:

```cypher
(:HOH:Ort {name:'Bietenhahn'})
(:HOH:Ereignis {name:'Aufenthalt der Kinder in Bietenhahn'})
```

Relationships:

```cypher
(Albert Muchow)-[:INITIIERT_AUFENTHALT]->(Aufenthalt der Kinder in Bietenhahn)

(Martin Bach)-[:NIMMT_TEIL_AN]->(Aufenthalt der Kinder in Bietenhahn)

(Heinrich Brielach)-[:NIMMT_TEIL_AN]->(Aufenthalt der Kinder in Bietenhahn)

(Wilma Brielach (Tochter))-[:NIMMT_TEIL_AN]->(Aufenthalt der Kinder in Bietenhahn)

(Aufenthalt der Kinder in Bietenhahn)-[:FINDET_STATT_IN]->(Bietenhahn)
```

---

# 14. Optional themes

Possible `:HOH:Thema` nodes:

```text
Vaterlosigkeit
Trauer
Nachkriegsarmut
Verdrängung
soziale Ungleichheit
Ersatzväter
Verantwortung
Vergangenheitsaufarbeitung
Auflösung traditioneller Familienstrukturen
```

Possible relationships:

```cypher
(Martin Bach)-[:BETROFFEN_VON]->(Vaterlosigkeit)

(Heinrich Brielach)-[:BETROFFEN_VON]->(Vaterlosigkeit)

(Wilma Brielach)-[:BETROFFEN_VON]->(Nachkriegsarmut)

(Heinrich Brielach)-[:BETROFFEN_VON]->(Nachkriegsarmut)

(Nella Bach)-[:BETROFFEN_VON]->(Trauer)

(Gäseler)-[:STEHT_FUER]->(Verdrängung)

(Albert Muchow)-[:STEHT_FUER]->(Verantwortung)
```

Mark symbolic interpretation edges:
```text
sicherheit: "interpretativ"
```

---

# 15. Do not include film-only assertions

Do not create a film node and do not encode any relationship solely because of the 1975 adaptation.

The graph is currently:

```text
Roman only
```

If the user later wants film comparison, create a separate namespace such as:

```text
:HOH_FILM
```

Do not mix it with `:HOH`.

---

# 16. Suggested initialization strategy

## Step A: inspect current state

```cypher
MATCH (n:HOH)
RETURN labels(n), n.name, properties(n);
```

## Step B: reset only this project if needed

```cypher
MATCH (n:HOH)
DETACH DELETE n;
```

## Step C: load all nodes

Use `MERGE` and apply both semantic and project labels:

```cypher
MERGE (:HOH:Figur {name:'Martin Bach'})
SET ...
```

## Step D: create relationships using explicit `MATCH`

Never rely on variable scope across statements.

## Step E: validate counts and topology

---

# 17. Validation queries

## Show the complete HOH graph

```cypher
MATCH p=(a:HOH)-[r]-(b:HOH)
RETURN p;
```

## Show only figure-to-figure graph

```cypher
MATCH p=(a:HOH:Figur)-[r]-(b:HOH:Figur)
RETURN p;
```

## Verify Martin-Heinrich bridge

```cypher
MATCH p=
  (:HOH:Figur {name:'Martin Bach'})
  -[:IST_FREUND_VON]-
  (:HOH:Figur {name:'Heinrich Brielach'})
RETURN p;
```

## Verify Bach-to-Brielach connectivity

```cypher
MATCH p=
  (:HOH:Figur {name:'Nella Bach'})
  -[*1..6]-
  (:HOH:Figur {name:'Wilma Brielach'})
RETURN p
LIMIT 20;
```

## List all figure relationships as a table

```cypher
MATCH (a:HOH:Figur)-[r]-(b:HOH:Figur)
RETURN
  a.name AS Von,
  type(r) AS Beziehung,
  b.name AS Zu
ORDER BY Von, Beziehung, Zu;
```

## Detect unlabeled accidental nodes

```cypher
MATCH (n)
WHERE size(labels(n)) = 0
RETURN n, properties(n);
```

There should be no new unlabeled nodes created by this project.

## Detect HOH nodes without relationships

```cypher
MATCH (n:HOH)
WHERE NOT (n)--()
RETURN labels(n), n.name;
```

Review every result.

---

# 18. Iteration workflow

When the user discovers a new relationship while reading:

1. Do not blindly append it.
2. Check whether the node already exists.
3. Decide whether it is:
   - factual / canonical,
   - a character's perception,
   - or literary interpretation.
4. Use the appropriate German relationship type.
5. Add `quelle:'Roman'`.
6. Add `sicherheit:'kanonisch'` or `sicherheit:'interpretativ'`.
7. Run validation queries.
8. Show the user the exact edge(s) added or changed.

Example:

```cypher
MATCH
  (h:HOH:Figur {name:'Heinrich Brielach'}),
  (w:HOH:Figur {name:'Will'})
MERGE (h)-[r:SIEHT_ALS_RICHTIGEN_ONKEL]->(w)
SET
  r.quelle = 'Roman',
  r.sicherheit = 'interpretativ';
```

---

# 19. Style conventions

Relationship types:

```text
UPPER_SNAKE_CASE
```

German only.

Examples:

```text
IST_MUTTER_VON
IST_VATER_VON
IST_FREUND_VON
WAR_VERHEIRATET_MIT
WAR_VORGESETZTER_VON
SCHLAEGT_INS_GESICHT
HEGT_RACHEFANTASIEN_GEGEN
VEROEFFENTLICHTE_GEDICHT_VON
```

Avoid English relationship types such as:

```text
MOTHER_OF
FRIEND_OF
WORKED_AT
```

Node properties may use German lowercase names:

```text
rolle
beruf
status
bemerkung
quelle
sicherheit
```

---

# 20. Important data-quality notes

The graph is a work in progress and should evolve as the user reads.

Do not overstate uncertain details.

Examples:

- Gäseler's moral responsibility for Raimund's death is clear in the novel's character perspectives, but do not encode him as an objective legal `Mörder`.
- Frau Brielach's thoughts about the Bäcker may be modeled as `ERWAEGT_*` rather than as a completed relationship until the text clearly establishes it.
- Character perception edges should be distinguished from objective facts.
- Film adaptation details must remain excluded.

---

# 21. Desired final visual structure

When visualized, the graph should naturally form something like:

```text
                     Familie Bach
                         |
      Großmutter -- Nella -- Raimund -- Gäseler
          |          |          |
        Bolda       Martin ---- Albert
                      |
                      | IST_FREUND_VON
                      |
                   Heinrich
                      |
                 Wilma Brielach
                  /          \
                Leo        Der Bäcker
                  \
             Wilma (Tochter)
```

This is schematic only.

The actual Neo4j graph should show all verified relationships, with Martin-Heinrich as the central bridge between the two major family communities.

---

# 22. First action for the Codex agent

Start by:

1. Connecting via Bolt.
2. Running:
   ```cypher
   MATCH (n:HOH) RETURN count(n);
   ```
3. If any stale HOH nodes exist, inspect them.
4. If the graph is malformed, safely reset only `:HOH`.
5. Load the corrected graph.
6. Run all validation queries.
7. Return a concise report:
   - nodes created
   - relationships created
   - isolated nodes
   - any uncertain relationships requiring user review
   - exact visualization query to run in Neo4j Browser

Do not touch unrelated database content.
