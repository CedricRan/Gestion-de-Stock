from fastapi import APIRouter
from database.elastic import es
router = APIRouter()
@router.get("/movements")
def get_all_movements():
    query = {
        "query": {
            "match_all": {}
        },
        "sort": [
            # 📅 On trie par date décroissante pour afficher les derniers mouvements en haut
            {"date_mouvement": {"order": "desc"}}
        ],
        "size": 100  # Récupère les 100 derniers mouvements
    }
    
    try:
        response = es.search(index="movements", body=query)
        # On extrait la source de chaque hit trouvé
        movements = []
        for hit in response["hits"]["hits"]:
            source = hit["_source"]
            # Optionnel : On rend la date plus jolie si elle existe
            if "date_mouvement" in source:
                # Transforme "2026-06-06T10:48:30" en quelque chose de plus lisible si tu veux
                source["date_mouvement"] = source["date_mouvement"].replace("T", " ")[:19]
            movements.append(source)
            
        return movements
    except Exception as e:
        print(f"❌ Erreur lors de la récupération de l'historique : {e}")
        # Si l'index n'existe pas encore (aucun mouvement fait), on renvoie une liste vide
        return []
