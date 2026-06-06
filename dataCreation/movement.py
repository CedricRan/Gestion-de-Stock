from elasticsearch import helpers
from database.elastic import es

index_name = "movements"

docs = [
    {
        "id_mouvement": "M001",
        "movement_id": "MOV-001",
        "nom_produit": "Riz",
        "operator_id": "OP-01",
        "product_id": "PR-001",
        "quantite": 20,
        "quantity": 20,
        "reference": "REF-001",
        "date_mouvement": "2026-06-01",
        "timestamp": "2026-06-01T10:00:00",
        "type": "entrée",
        "type_mouvement": "IN"
    },
    {
        "id_mouvement": "M002",
        "movement_id": "MOV-002",
        "nom_produit": "Sucre",
        "operator_id": "OP-02",
        "product_id": "PR-002",
        "quantite": 10,
        "quantity": 10,
        "reference": "REF-002",
        "date_mouvement": "2026-06-02",
        "timestamp": "2026-06-02T11:00:00",
        "type": "entrée",
        "type_mouvement": "IN"
    },
    {
        "id_mouvement": "M003",
        "movement_id": "MOV-003",
        "nom_produit": "Huile",
        "operator_id": "OP-03",
        "product_id": "PR-003",
        "quantite": 5,
        "quantity": 5,
        "reference": "REF-003",
        "date_mouvement": "2026-06-03",
        "timestamp": "2026-06-03T09:30:00",
        "type": "sortie",
        "type_mouvement": "OUT"
    },
    {
        "id_mouvement": "M004",
        "movement_id": "MOV-004",
        "nom_produit": "Pâtes",
        "operator_id": "OP-01",
        "product_id": "PR-004",
        "quantite": 15,
        "quantity": 15,
        "reference": "REF-004",
        "date_mouvement": "2026-06-04",
        "timestamp": "2026-06-04T14:20:00",
        "type": "entrée",
        "type_mouvement": "IN"
    },
    {
        "id_mouvement": "M005",
        "movement_id": "MOV-005",
        "nom_produit": "Sel",
        "operator_id": "OP-04",
        "product_id": "PR-005",
        "quantite": 8,
        "quantity": 8,
        "reference": "REF-005",
        "date_mouvement": "2026-06-05",
        "timestamp": "2026-06-05T08:10:00",
        "type": "sortie",
        "type_mouvement": "OUT"
    },

    {
        "id_mouvement": "M006",
        "movement_id": "MOV-006",
        "nom_produit": "Savon",
        "operator_id": "OP-02",
        "product_id": "PR-006",
        "quantite": 12,
        "quantity": 12,
        "reference": "REF-006",
        "date_mouvement": "2026-06-06",
        "timestamp": "2026-06-06T12:00:00",
        "type": "entrée",
        "type_mouvement": "IN"
    },
    {
        "id_mouvement": "M007",
        "movement_id": "MOV-007",
        "nom_produit": "Shampooing",
        "operator_id": "OP-03",
        "product_id": "PR-007",
        "quantite": 6,
        "quantity": 6,
        "reference": "REF-007",
        "date_mouvement": "2026-06-07",
        "timestamp": "2026-06-07T13:45:00",
        "type": "sortie",
        "type_mouvement": "OUT"
    },
    {
        "id_mouvement": "M008",
        "movement_id": "MOV-008",
        "nom_produit": "Dentifrice",
        "operator_id": "OP-01",
        "product_id": "PR-008",
        "quantite": 4,
        "quantity": 4,
        "reference": "REF-008",
        "date_mouvement": "2026-06-08",
        "timestamp": "2026-06-08T09:00:00",
        "type": "entrée",
        "type_mouvement": "IN"
    },
    {
        "id_mouvement": "M009",
        "movement_id": "MOV-009",
        "nom_produit": "Eau minérale",
        "operator_id": "OP-05",
        "product_id": "PR-009",
        "quantite": 50,
        "quantity": 50,
        "reference": "REF-009",
        "date_mouvement": "2026-06-09",
        "timestamp": "2026-06-09T10:15:00",
        "type": "entrée",
        "type_mouvement": "IN"
    },
    {
        "id_mouvement": "M010",
        "movement_id": "MOV-010",
        "nom_produit": "Café",
        "operator_id": "OP-05",
        "product_id": "PR-010",
        "quantite": 7,
        "quantity": 7,
        "reference": "REF-010",
        "date_mouvement": "2026-06-10",
        "timestamp": "2026-06-10T11:30:00",
        "type": "sortie",
        "type_mouvement": "OUT"
    }
]

# Bulk actions
actions = [
    {
        "_index": index_name,
        "_id": doc["id_mouvement"],
        "_source": doc
    }
    for doc in docs
]

# Execution bulk
response = helpers.bulk(es, actions)

print("✔ Bulk mouvements terminé")
print(response)
