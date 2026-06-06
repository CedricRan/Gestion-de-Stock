from elasticsearch import helpers
from database.elastic import es

index_name = "anomalies"

docs = [
    {
        "date": "2026-06-01",
        "nom_produit": "Riz",
        "quantite": 50,
        "raison": "consommation élevée",
        "score": 0.85,
        "type": "alimentaire"
    },
    {
        "date": "2026-06-02",
        "nom_produit": "Sucre",
        "quantite": 30,
        "raison": "usage quotidien",
        "score": 0.70,
        "type": "alimentaire"
    },
    {
        "date": "2026-06-03",
        "nom_produit": "Huile",
        "quantite": 20,
        "raison": "cuisine",
        "score": 0.65,
        "type": "alimentaire"
    },
    {
        "date": "2026-06-04",
        "nom_produit": "Pâtes",
        "quantite": 80,
        "raison": "forte demande",
        "score": 0.90,
        "type": "alimentaire"
    },
    {
        "date": "2026-06-05",
        "nom_produit": "Sel",
        "quantite": 15,
        "raison": "usage modéré",
        "score": 0.40,
        "type": "alimentaire"
    },

    {
        "date": "2026-06-06",
        "nom_produit": "Savon",
        "quantite": 25,
        "raison": "hygiène quotidienne",
        "score": 0.75,
        "type": "hygiène"
    },
    {
        "date": "2026-06-07",
        "nom_produit": "Shampooing",
        "quantite": 12,
        "raison": "usage personnel",
        "score": 0.60,
        "type": "hygiène"
    },
    {
        "date": "2026-06-08",
        "nom_produit": "Dentifrice",
        "quantite": 18,
        "raison": "santé dentaire",
        "score": 0.55,
        "type": "hygiène"
    },
    {
        "date": "2026-06-09",
        "nom_produit": "Papier toilette",
        "quantite": 40,
        "raison": "consommation stable",
        "score": 0.80,
        "type": "hygiène"
    },
    {
        "date": "2026-06-10",
        "nom_produit": "Déodorant",
        "quantite": 14,
        "raison": "usage quotidien",
        "score": 0.50,
        "type": "hygiène"
    },

    {
        "date": "2026-06-11",
        "nom_produit": "Eau minérale",
        "quantite": 100,
        "raison": "forte consommation",
        "score": 0.95,
        "type": "boisson"
    },
    {
        "date": "2026-06-12",
        "nom_produit": "Café",
        "quantite": 22,
        "raison": "habitude quotidienne",
        "score": 0.88,
        "type": "boisson"
    },
    {
        "date": "2026-06-13",
        "nom_produit": "Thé",
        "quantite": 18,
        "raison": "consommation régulière",
        "score": 0.60,
        "type": "boisson"
    },
    {
        "date": "2026-06-14",
        "nom_produit": "Jus",
        "quantite": 35,
        "raison": "consommation familiale",
        "score": 0.72,
        "type": "boisson"
    },
    {
        "date": "2026-06-15",
        "nom_produit": "Soda",
        "quantite": 10,
        "raison": "occasionnel",
        "score": 0.30,
        "type": "boisson"
    },

    {
        "date": "2026-06-16",
        "nom_produit": "Farine",
        "quantite": 60,
        "raison": "boulangerie",
        "score": 0.78,
        "type": "alimentaire"
    },
    {
        "date": "2026-06-17",
        "nom_produit": "Levure",
        "quantite": 5,
        "raison": "cuisson",
        "score": 0.45,
        "type": "alimentaire"
    },
    {
        "date": "2026-06-18",
        "nom_produit": "Lait",
        "quantite": 24,
        "raison": "consommation quotidienne",
        "score": 0.82,
        "type": "alimentaire"
    },
    {
        "date": "2026-06-19",
        "nom_produit": "Fromage",
        "quantite": 9,
        "raison": "repas",
        "score": 0.68,
        "type": "alimentaire"
    },
    {
        "date": "2026-06-20",
        "nom_produit": "Beurre",
        "quantite": 11,
        "raison": "petit-déjeuner",
        "score": 0.70,
        "type": "alimentaire"
    }
]

# BULK actions
actions = [
    {
        "_index": index_name,
        "_source": doc
    }
    for doc in docs
]

response = helpers.bulk(es, actions)

print("✔ Bulk analyse terminé")
print(response)
