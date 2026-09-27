"""Build a reproducible, novel-only HOH import from the supplied specification."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / 'docs' / 'graph-specification.md'
spec = SOURCE.read_text(encoding='utf-8-sig')
nodes = {}

def node(name, label, **props):
    nodes[name] = dict(name=name, label=label, properties=dict(
        name=name, quelle='Roman', sicherheit='kanonisch',
        belegstatus='Aus Nutzervorgabe übernommen; nicht am Primärtext geprüft',
        **props))

node('Haus ohne Hüter', 'Werk', autor='Heinrich Böll', erscheinungsjahr=1954)
node('Familie Bach', 'Familie')
node('Familie Brielach', 'Familie')
figures = {
    'Nella Bach': dict(rolle='Mutter von Martin; Witwe von Raimund'),
    'Raimund Bach': dict(rolle='Dichter / Schriftsteller', status='im Zweiten Weltkrieg gefallen'),
    'Martin Bach': dict(rolle='Kind; Hauptfigur / Perspektivfigur'),
    'Martins Großmutter': dict(rolle='Mutter von Nella; Großmutter von Martin', bemerkung='wohlhabende Fabrikantenfamilie / Marmeladenfabrik'),
    'Albert Muchow': dict(rolle='enge Bezugsperson der Familie Bach', beruf='Witzzeichner / Zeichner', bemerkung='arbeitete früher mit Raimund als Zeichner in der Marmeladenfabrik'),
    'Will': dict(rolle='Onkel von Martin; ältere stabile Bezugsperson'),
    'Glumbich Cholokusteban': dict(alias='Glum', rolle='männlicher Hausgenosse / Freund des Bach-Umfelds', bemerkung='angelt; ehemaliger Lagerinsasse'),
    'Bolda': dict(rolle='alte Freundin von Martins Großmutter'),
    'Pater Willibrord': dict(beruf='katholischer Geistlicher'),
    'Schurbigel': dict(rolle='Redner / Kulturintellektueller / Literaturbetrieb', bemerkung="veröffentlichte 1935 ein Gedicht Raimund Bachs; Dissertation 1934: 'Unser Führer in der modernen Lyrik'"),
    'Gäseler': dict(rolle='ehemaliger Leutnant; später im Literaturbetrieb', bemerkung='Raimunds militärischer Vorgesetzter'),
    'Wilma Brielach': dict(rolle='Mutter von Heinrich und Wilma', bemerkung='Vorname laut Nutzervorgabe im Roman ausdrücklich als Wilma belegt'),
    'Heinrich Brielach': dict(rolle='Kind; Hauptfigur / Perspektivfigur'),
    'Wilma Brielach (Tochter)': dict(rolle='kleine Halbschwester von Heinrich'),
    'Vater Brielach': dict(beruf='Autoschlosser', status='im Krieg gefallen / verschollen; Todesumstände unsicher'),
    'Leo': dict(beruf='Straßenbahnschaffner', rolle='Partner von Wilma Brielach; Vater der kleinen Wilma'),
    'Der Bäcker': dict(beruf='Bäcker', rolle='Arbeitgeber und Verehrer von Wilma Brielach'),
    'Frau Borussiak': dict(rolle='Bekannte / Betreuungsperson im Umfeld der Brielachs'),
}
for name in ['Erich', 'Gert', 'Karl']:
    figures[name] = dict(rolle="frühere Partner / 'Onkel' im Umfeld von Heinrichs Mutter")
for name, props in figures.items():
    node(name, 'Figur', **props)
for name in ['Bambergers Nudelfabrik', 'Marmeladenfabrik', 'Bäckerei', 'Bietenhahn', 'Odessa', 'Russland / Ostfront', 'nicht näher bezeichnete Stadt am Rhein']:
    props = {}
    if name == 'Bietenhahn':
        props = dict(typ='fiktiver Ort', bemerkung='Schutz- und Gegenraum für die Kinder (Interpretation)')
    if name == 'Odessa':
        props = dict(bemerkung='Militärgefängnis-Kontext während des Krieges')
    node(name, 'Ort', **props)
for name in ['Raimunds letzter Patrouillengang', 'Tod Raimunds', 'Albert schlägt Gäseler', 'Alberts Haft in Odessa', 'Aufenthalt der Kinder in Bietenhahn']:
    node(name, 'Ereignis')
for name in ['Vaterlosigkeit', 'Trauer', 'Nachkriegsarmut', 'Verdrängung', 'soziale Ungleichheit', 'Ersatzväter', 'Verantwortung', 'Vergangenheitsaufarbeitung', 'Auflösung traditioneller Familienstrukturen']:
    node(name, 'Thema')
    nodes[name]['properties']['sicherheit'] = 'interpretativ'

edges = {}
def edge(a, rel, b, **props):
    assert a in nodes and b in nodes, (a, rel, b)
    assert re.fullmatch('[A-Z_]+', rel), rel
    p = dict(quelle='Roman', sicherheit='kanonisch',
             belegstatus='Aus Nutzervorgabe übernommen; nicht am Primärtext geprüft')
    p.update(props)
    edges[(a, rel, b)] = dict(von=a, typ=rel, zu=b, properties=p)

# Only the explicitly named relationship examples in sections 9–14.
section = spec.split('# 9. Canonical relationship set', 1)[1].split('# 15.', 1)[0]
for a, rel, b in re.findall(r'^\((.+)\)-\[:([A-Z_]+)\]->\((.+)\)\s*$', section, re.M):
    edge(a, rel, b)

for (a, rel, b), item in edges.items():
    p = item['properties']
    if rel.startswith('SIEHT_ALS_'):
        p.update(sicherheit='interpretativ', aussageart='Figurenwahrnehmung', perspektive='Heinrich Brielach')
    elif rel.startswith('ERWAEGT_'):
        p.update(sicherheit='interpretativ', aussageart='gedanklich erwogen', perspektive='Wilma Brielach')
    elif rel in {'BESCHAEMT', 'IST_VATERFIGUR_FUER', 'STEHT_FUER', 'BETROFFEN_VON'}:
        p.update(sicherheit='interpretativ', aussageart='Interpretation')
    if rel == 'IST_FREUND_VON':
        p['symmetrisch'] = True
    if rel == 'VEROEFFENTLICHTE_GEDICHT_VON':
        p['jahr'] = 1935
    if rel == 'WIRD_INHAFTIERT_IN':
        p.update(dauer='sechs Monate', grund='Ohrfeige / Schlag gegen Gäseler')
    if rel == 'ORDNET_AN':
        p.update(motiv='eitler Eigensinn / verletzte Autorität', motiv_sicherheit='interpretativ')

# Explicit family membership yields the requested two communities.
for name in ['Nella Bach', 'Raimund Bach', 'Martin Bach', 'Martins Großmutter', 'Will']:
    edge(name, 'GEHOERT_ZUR_FAMILIE', 'Familie Bach')
for name in ['Wilma Brielach', 'Heinrich Brielach', 'Wilma Brielach (Tochter)', 'Vater Brielach']:
    edge(name, 'GEHOERT_ZUR_FAMILIE', 'Familie Brielach')
for name in ['Leo', 'Der Bäcker', 'Erich', 'Gert', 'Karl', 'Frau Borussiak']:
    edge(name, 'GEHOERT_ZUM_UMFELD_VON', 'Familie Brielach')

# Connect named events without inventing additional novel facts.
edge('Albert Muchow', 'HANDELT_IN', 'Albert schlägt Gäseler')
edge('Albert schlägt Gäseler', 'BETRIFFT', 'Gäseler')
edge('Albert schlägt Gäseler', 'FUEHRT_ZU', 'Alberts Haft in Odessa')
edge('Alberts Haft in Odessa', 'BETRIFFT', 'Albert Muchow', dauer='sechs Monate')
edge('Alberts Haft in Odessa', 'FINDET_STATT_IN', 'Odessa')

# Work links are cataloguing metadata, not assertions of unverified scenes.
for name, item in nodes.items():
    if name == 'Haus ohne Hüter':
        continue
    label = item['label']
    rel = {'Figur': 'IST_FIGUR_IN', 'Familie': 'IST_FAMILIE_IN', 'Ort': 'IST_ORT_IN',
           'Ereignis': 'IST_EREIGNIS_IN', 'Thema': 'IST_THEMA_IN'}[label]
    edge(name, rel, 'Haus ohne Hüter', sicherheit='interpretativ' if label == 'Thema' else 'kanonisch', aussageart='Werkzuordnung')

data = dict(nodes=list(nodes.values()), relationships=list(edges.values()))
(ROOT / 'hoh_graph.json').write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')

def cypher(value):
    if isinstance(value, dict):
        return '{' + ', '.join('`' + k + '`: ' + cypher(v) for k, v in value.items()) + '}'
    if isinstance(value, list):
        return '[' + ', '.join(cypher(v) for v in value) + ']'
    return json.dumps(value, ensure_ascii=False)

# A single statement is atomic in Browser and never uses cross-statement variables.
clauses = []
for label in sorted({n['label'] for n in nodes.values()}):
    rows = [n['properties'] for n in nodes.values() if n['label'] == label]
    clauses.append('CALL {\n UNWIND ' + cypher(rows) + ' AS row\n MERGE (n:HOH:' + label + ' {name: row.name})\n SET n += row\n RETURN count(*) AS anzahl_' + label + '\n}')
for index, rel in enumerate(sorted({e['typ'] for e in edges.values()})):
    rows = [dict(von=e['von'], zu=e['zu'], eigenschaften=e['properties']) for e in edges.values() if e['typ'] == rel]
    clauses.append('CALL {\n UNWIND ' + cypher(rows) + ' AS row\n MATCH (a:HOH {name: row.von}), (b:HOH {name: row.zu})\n MERGE (a)-[r:' + rel + ']->(b)\n SET r += row.eigenschaften\n RETURN count(*) AS kanten_' + str(index) + '\n}')
clauses.append('RETURN ' + str(len(nodes)) + ' AS erwartete_Knoten, ' + str(len(edges)) + ' AS erwartete_Kanten;')
(ROOT / 'hoh_import.cypher').write_text('\n'.join(clauses), encoding='utf-8')
print(json.dumps(dict(nodes=len(nodes), relationships=len(edges), labels={label:sum(n['label']==label for n in nodes.values()) for label in sorted({n['label'] for n in nodes.values()})}), ensure_ascii=False))
