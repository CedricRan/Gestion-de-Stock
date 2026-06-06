from elasticsearch import helpers
from database.elastic import es
# Connexion à Elasticsearch


index_name = "alerts"

# Tes 40 documents
docs = [
    {"consommation_moyenne": 2.5, "date": "2026-06-01", "jours_restants": 12, "nom_produit": "Riz", "raison": "usage quotidien", "stock_actuel": 30, "type": "alimentaire"},
    {"consommation_moyenne": 1.2, "date": "2026-06-02", "jours_restants": 20, "nom_produit": "Sucre", "raison": "consommation régulière", "stock_actuel": 25, "type": "alimentaire"},
    {"consommation_moyenne": 0.8, "date": "2026-06-03", "jours_restants": 15, "nom_produit": "Huile", "raison": "cuisine", "stock_actuel": 10, "type": "alimentaire"},
    {"consommation_moyenne": 3.0, "date": "2026-06-04", "jours_restants": 10, "nom_produit": "Pâtes", "raison": "repas fréquents", "stock_actuel": 40, "type": "alimentaire"},
    {"consommation_moyenne": 0.5, "date": "2026-06-05", "jours_restants": 30, "nom_produit": "Sel", "raison": "usage modéré", "stock_actuel": 15, "type": "alimentaire"},

    {"consommation_moyenne": 1.1, "date": "2026-06-06", "jours_restants": 18, "nom_produit": "Savon", "raison": "hygiène", "stock_actuel": 20, "type": "hygiène"},
    {"consommation_moyenne": 0.7, "date": "2026-06-07", "jours_restants": 25, "nom_produit": "Shampooing", "raison": "usage personnel", "stock_actuel": 12, "type": "hygiène"},
    {"consommation_moyenne": 0.3, "date": "2026-06-08", "jours_restants": 40, "nom_produit": "Dentifrice", "raison": "hygiène dentaire", "stock_actuel": 8, "type": "hygiène"},
    {"consommation_moyenne": 2.2, "date": "2026-06-09", "jours_restants": 14, "nom_produit": "Papier toilette", "raison": "usage quotidien", "stock_actuel": 50, "type": "hygiène"},
    {"consommation_moyenne": 0.9, "date": "2026-06-10", "jours_restants": 22, "nom_produit": "Déodorant", "raison": "hygiène corporelle", "stock_actuel": 14, "type": "hygiène"},

    {"consommation_moyenne": 5.0, "date": "2026-06-11", "jours_restants": 8, "nom_produit": "Eau minérale", "raison": "consommation élevée", "stock_actuel": 100, "type": "boisson"},
    {"consommation_moyenne": 1.5, "date": "2026-06-12", "jours_restants": 16, "nom_produit": "Café", "raison": "consommation quotidienne", "stock_actuel": 18, "type": "boisson"},
    {"consommation_moyenne": 1.0, "date": "2026-06-13", "jours_restants": 19, "nom_produit": "Thé", "raison": "boisson chaude", "stock_actuel": 22, "type": "boisson"},
    {"consommation_moyenne": 2.8, "date": "2026-06-14", "jours_restants": 11, "nom_produit": "Jus", "raison": "consommation familiale", "stock_actuel": 30, "type": "boisson"},
    {"consommation_moyenne": 0.6, "date": "2026-06-15", "jours_restants": 28, "nom_produit": "Soda", "raison": "occasionnel", "stock_actuel": 10, "type": "boisson"},

    {"consommation_moyenne": 1.3, "date": "2026-06-16", "jours_restants": 17, "nom_produit": "Farine", "raison": "boulangerie", "stock_actuel": 35, "type": "alimentaire"},
    {"consommation_moyenne": 0.4, "date": "2026-06-17", "jours_restants": 35, "nom_produit": "Levure", "raison": "cuisson", "stock_actuel": 6, "type": "alimentaire"},
    {"consommation_moyenne": 2.0, "date": "2026-06-18", "jours_restants": 13, "nom_produit": "Lait", "raison": "consommation quotidienne", "stock_actuel": 24, "type": "alimentaire"},
    {"consommation_moyenne": 1.7, "date": "2026-06-19", "jours_restants": 15, "nom_produit": "Fromage", "raison": "repas", "stock_actuel": 9, "type": "alimentaire"},
    {"consommation_moyenne": 0.9, "date": "2026-06-20", "jours_restants": 21, "nom_produit": "Beurre", "raison": "petit-déjeuner", "stock_actuel": 11, "type": "alimentaire"},

    {"consommation_moyenne": 0.2, "date": "2026-06-21", "jours_restants": 50, "nom_produit": "Ampoules", "raison": "maintenance", "stock_actuel": 15, "type": "équipement"},
    {"consommation_moyenne": 1.4, "date": "2026-06-22", "jours_restants": 14, "nom_produit": "Batteries", "raison": "usage appareils", "stock_actuel": 20, "type": "équipement"},
    {"consommation_moyenne": 0.5, "date": "2026-06-23", "jours_restants": 32, "nom_produit": "Câbles", "raison": "informatique", "stock_actuel": 12, "type": "équipement"},
    {"consommation_moyenne": 0.3, "date": "2026-06-24", "jours_restants": 45, "nom_produit": "Clés USB", "raison": "stock IT", "stock_actuel": 18, "type": "équipement"},
    {"consommation_moyenne": 0.6, "date": "2026-06-25", "jours_restants": 27, "nom_produit": "Chargeurs", "raison": "remplacement", "stock_actuel": 14, "type": "équipement"},

    {"consommation_moyenne": 1.8, "date": "2026-06-26", "jours_restants": 12, "nom_produit": "Tomates", "raison": "cuisine", "stock_actuel": 22, "type": "alimentaire"},
    {"consommation_moyenne": 1.6, "date": "2026-06-27", "jours_restants": 13, "nom_produit": "Oignons", "raison": "cuisine", "stock_actuel": 19, "type": "alimentaire"},
    {"consommation_moyenne": 2.3, "date": "2026-06-28", "jours_restants": 10, "nom_produit": "Pommes de terre", "raison": "repas", "stock_actuel": 45, "type": "alimentaire"},
    {"consommation_moyenne": 0.7, "date": "2026-06-29", "jours_restants": 24, "nom_produit": "Carottes", "raison": "cuisine", "stock_actuel": 16, "type": "alimentaire"},
    {"consommation_moyenne": 1.9, "date": "2026-06-30", "jours_restants": 11, "nom_produit": "Poulet", "raison": "repas", "stock_actuel": 28, "type": "alimentaire"},

    {"consommation_moyenne": 0.4, "date": "2026-07-01", "jours_restants": 33, "nom_produit": "Médicament A", "raison": "traitement", "stock_actuel": 9, "type": "pharmacie"},
    {"consommation_moyenne": 0.2, "date": "2026-07-02", "jours_restants": 60, "nom_produit": "Médicament B", "raison": "prévention", "stock_actuel": 7, "type": "pharmacie"},
    {"consommation_moyenne": 0.3, "date": "2026-07-03", "jours_restants": 48, "nom_produit": "Vitamine C", "raison": "santé", "stock_actuel": 20, "type": "pharmacie"},
    {"consommation_moyenne": 0.5, "date": "2026-07-04", "jours_restants": 29, "nom_produit": "Paracétamol", "raison": "douleur", "stock_actuel": 30, "type": "pharmacie"},
    {"consommation_moyenne": 0.6, "date": "2026-07-05", "jours_restants": 26, "nom_produit": "Antiseptique", "raison": "soins", "stock_actuel": 13, "type": "pharmacie"},
]

# Bulk actions
actions = [
    {
        "_index": index_name,
        "_source": doc
    }
    for doc in docs
]

# Envoi bulk
response = helpers.bulk(es, actions)

print("Bulk terminé !")
print(response)
