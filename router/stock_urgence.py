from fastapi import APIRouter
from database.elastic import es
from services.prediction import prediction_service

router = APIRouter()

@router.get("/stocks/by-urgency")
def get_stocks_by_urgency():
    try:
        # 1. Récupérer TOUS les produits depuis ton index stock
        # (On met une size large pour être sûr de tout avoir)
        response = es.search(index="stock", body={"query": {"match_all": {}}, "size": 1000})
        produits = [hit["_source"] for hit in response["hits"]["hits"]]
        
        liste_triee = []
        
        for p in produits:
            name = p["nom_produit"]
            stock_actuel = p["quantite"]
            
            # 2. On demande au service de prédiction la consommation moyenne (MJc)
            # On va réutiliser la logique mais en demandant juste le chiffre
            mj_c = prediction_service.get_vitesse_consommation(name)
            
            # 3. Calcul de l'urgence
            if mj_c > 0:
                jours_restants = stock_actuel / mj_c
            else:
                # Si aucune consommation (MJc = 0), le produit n'est pas urgent du tout
                jours_restants = 9999  
            
            liste_triee.append({
                "nom_produit": name,
                "stock_actuel": stock_actuel,
                "consommation_moyenne": round(mj_c, 2),
                "jours_restants": round(jours_restants, 1) if jours_restants != 9999 else "Infini",
                "score_urgence": jours_restants # Plus ce chiffre est bas, plus c'est urgent
            })
        
        # 4. Le Tri Magique : On classe du plus petit nombre de jours au plus grand
        liste_triee.sort(key=lambda x: x["score_urgence"])
        
        return liste_triee

    except Exception as e:
        print(f"❌ Erreur lors du calcul de l'urgence des stocks : {e}")
        return []
