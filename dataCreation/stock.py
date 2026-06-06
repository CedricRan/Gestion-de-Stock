from elasticsearch import Elasticsearch, helpers
from database.elastic import es


index_name = "stock"

# Données exemple compatibles avec ton mapping
docs = [
    {"id": "1", "category": "alimentaire", "nom_produit": "Riz", "quantite": 50},
    {"id": "2", "category": "alimentaire", "nom_produit": "Sucre", "quantite": 30},
    {"id": "3", "category": "alimentaire", "nom_produit": "Huile", "quantite": 20},
    {"id": "4", "category": "alimentaire", "nom_produit": "Pâtes", "quantite": 80},
    {"id": "5", "category": "alimentaire", "nom_produit": "Sel", "quantite": 15},

    {"id": "6", "category": "hygiène", "nom_produit": "Savon", "quantite": 25},
    {"id": "7", "category": "hygiène", "nom_produit": "Shampooing", "quantite": 12},
    {"id": "8", "category": "hygiène", "nom_produit": "Dentifrice", "quantite": 18},
    {"id": "9", "category": "hygiène", "nom_produit": "Papier toilette", "quantite": 40},
    {"id": "10", "category": "hygiène", "nom_produit": "Déodorant", "quantite": 14},

    {"id": "11", "category": "boisson", "nom_produit": "Eau minérale", "quantite": 100},
    {"id": "12", "category": "boisson", "nom_produit": "Café", "quantite": 22},
    {"id": "13", "category": "boisson", "nom_produit": "Thé", "quantite": 18},
    {"id": "14", "category": "boisson", "nom_produit": "Jus", "quantite": 35},
    {"id": "15", "category": "boisson", "nom_produit": "Soda", "quantite": 10},

    {"id": "16", "category": "alimentaire", "nom_produit": "Farine", "quantite": 60},
    {"id": "17", "category": "alimentaire", "nom_produit": "Levure", "quantite": 5},
    {"id": "18", "category": "alimentaire", "nom_produit": "Lait", "quantite": 24},
    {"id": "19", "category": "alimentaire", "nom_produit": "Fromage", "quantite": 9},
    {"id": "20", "category": "alimentaire", "nom_produit": "Beurre", "quantite": 11},

    {"id": "21", "category": "equipement", "nom_produit": "Ampoules", "quantite": 15},
    {"id": "22", "category": "equipement", "nom_produit": "Batteries", "quantite": 20},
    {"id": "23", "category": "equipement", "nom_produit": "Câbles", "quantite": 12},
    {"id": "24", "category": "equipement", "nom_produit": "Clés USB", "quantite": 18},
    {"id": "25", "category": "equipement", "nom_produit": "Chargeurs", "quantite": 14},

    {"id": "26", "category": "alimentaire", "nom_produit": "Tomates", "quantite": 22},
    {"id": "27", "category": "alimentaire", "nom_produit": "Oignons", "quantite": 19},
    {"id": "28", "category": "alimentaire", "nom_produit": "Pommes de terre", "quantite": 45},
    {"id": "29", "category": "alimentaire", "nom_produit": "Carottes", "quantite": 16},
    {"id": "30", "category": "alimentaire", "nom_produit": "Poulet", "quantite": 28},

    {"id": "31", "category": "pharmacie", "nom_produit": "Médicament A", "quantite": 9},
    {"id": "32", "category": "pharmacie", "nom_produit": "Médicament B", "quantite": 7},
    {"id": "33", "category": "pharmacie", "nom_produit": "Vitamine C", "quantite": 20},
    {"id": "34", "category": "pharmacie", "nom_produit": "Paracétamol", "quantite": 30},
    {"id": "35", "category": "pharmacie", "nom_produit": "Antiseptique", "quantite": 13},

    {"id": "36", "category": "alimentaire", "nom_produit": "Riz parfumé", "quantite": 40},
    {"id": "37", "category": "alimentaire", "nom_produit": "Haricots", "quantite": 55},
    {"id": "38", "category": "boisson", "nom_produit": "Limonade", "quantite": 18},
    {"id": "39", "category": "hygiène", "nom_produit": "Gel douche", "quantite": 21},
    {"id": "40", "category": "equipement", "nom_produit": "Powerbank", "quantite": 17},
]

# Bulk format
actions = [
    {
        "_index": index_name,
        "_id": doc["id"],   # important car champ id existe dans mapping
        "_source": doc
    }
    for doc in docs
]

# Exécution bulk
response = helpers.bulk(es, actions)

print("✔ Bulk terminé")
print(response)
