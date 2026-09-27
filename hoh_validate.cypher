// Summary, isolation and provenance checks (read-only).
CALL { MATCH (n:HOH) RETURN count(n) AS knoten }
CALL { MATCH (:HOH)-[r]->(:HOH) RETURN count(r) AS kanten }
CALL { MATCH (n) WHERE NOT n:HOH RETURN count(n) AS fremde_knoten }
CALL { MATCH (a)-[r]->(b) WHERE NOT a:HOH AND NOT b:HOH RETURN count(r) AS fremde_kanten }
CALL { MATCH (n) WHERE size(labels(n))=0 RETURN count(n) AS unbeschriftete_knoten }
CALL { MATCH (n:HOH) WHERE NOT (n)--() RETURN collect(n.name) AS isolierte_knoten }
CALL { MATCH (a:HOH)-[r]-(b) WHERE NOT b:HOH RETURN count(r) AS namespace_uebertritte }
CALL { MATCH (n:HOH) WITH n.name AS name, count(*) AS anzahl WHERE anzahl>1 RETURN collect({name:name, anzahl:anzahl}) AS doppelte_namen }
CALL { MATCH (:HOH)-[r]->(:HOH) WHERE r.quelle IS NULL OR r.quelle <> 'Roman' OR r.sicherheit IS NULL RETURN count(r) AS kanten_ohne_quelle_oder_sicherheit }
CALL { MATCH (:HOH:Figur {name:'Martin Bach'})-[r:IST_FREUND_VON]-(:HOH:Figur {name:'Heinrich Brielach'}) RETURN count(r) AS freundschaftsbruecken }
CALL { MATCH p=(:HOH:Figur {name:'Nella Bach'})-[*1..6]-(:HOH:Figur {name:'Wilma Brielach'}) WHERE all(n IN nodes(p) WHERE n:HOH:Figur) WITH p LIMIT 1 RETURN count(p) AS familien_ueber_figuren_verbunden }
RETURN *;

// Complete graph.
MATCH p=(a:HOH)-[r]->(b:HOH) RETURN p;

// Figures only: preserves the visual family communities without the work hub.
MATCH p=(a:HOH:Figur)-[r]->(b:HOH:Figur) RETURN p;

// Friendship bridge.
MATCH p=(:HOH:Figur {name:'Martin Bach'})-[:IST_FREUND_VON]-(:HOH:Figur {name:'Heinrich Brielach'}) RETURN p;

// Family connectivity confined to project nodes.
MATCH p=(:HOH:Figur {name:'Nella Bach'})-[*1..6]-(:HOH:Figur {name:'Wilma Brielach'})
WHERE all(n IN nodes(p) WHERE n:HOH:Figur) RETURN p LIMIT 20;

// Figure relationships, each stored direction once.
MATCH (a:HOH:Figur)-[r]->(b:HOH:Figur)
RETURN a.name AS Von, type(r) AS Beziehung, b.name AS Zu, properties(r) AS Eigenschaften
ORDER BY Von, Beziehung, Zu;

// Existing unlabeled nodes must never be deleted on assumptions of ownership.
MATCH (n) WHERE size(labels(n))=0 RETURN elementId(n), properties(n);

MATCH (n:HOH) WHERE NOT (n)--() RETURN labels(n), n.name;
