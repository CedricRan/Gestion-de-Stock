from fastapi import APIRouter
from database.elastic import es
router = APIRouter()
@router.get("/consommation")
def get_consommation_stats():
    try:
        # 1. On récupère tous les produits existants
        res = es.search(index="stock", body={"query": {"match_all": {}}, "size": 500})
        products = [hit["_source"] for hit in res["hits"]["hits"]]
        
        stats = []
        for p in products:
            name = p["nom_produit"]
            
            # 2. On appelle ta méthode pour avoir la MJc (vitesse de consommation)
            try:
                from services.prediction import prediction_service
                mj_c = prediction_service.get_vitesse_consommation(name)
            except Exception:
                mj_c = 0.0 # Valeur de secours si le service ne répond pas
            
            stats.append({
                "nom_produit": name,
                "vitesse_consommation": round(mj_c, 2),
                "unite": "unités / jour"
            })
            
        return stats
    except Exception as e:
        print(f"❌ Erreur route consommation: {e}")
        return []
