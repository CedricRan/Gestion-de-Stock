from datetime import datetime, timedelta
from database.elastic import es

class AnomalyService:
    def __init__(self):
        self.index_name = "anomalies"

    async def analyze_movement(self, name: str, qte: int, state: str):
        if state != "OUT":
            return

        # 1. Récupérer l'historique des sorties du produit (30 derniers jours)
        il_y_a_30_jours = (datetime.utcnow() - timedelta(days=30)).isoformat()
        
        query = {
            "query": {
                "bool": {
                    "must": [
                        {"term": {"nom_produit": name}},
                        {"term": {"type_mouvement.keyword": "OUT"}},
                        {"range": {"date_mouvement": {"gte": il_y_a_30_jours}}}
                    ]
                }
            },
            "aggs": {
                "stats_sorties": {
                    "extended_stats": {"field": "quantite"} # Calcule moyenne, écart-type, max, etc.
                }
            },
            "size": 0
        }

        try:
            response = es.search(index="movements", body=query)
            stats = response["aggregations"]["stats_sorties"]
            
            moyenne = stats["avg"] or 0
            ecart_type = stats["std_deviation"] or 0
            historique_count = stats["count"] or 0
        except Exception:
            return # Si l'index est vide ou inaccessible, on ignore

        # 2. Algorithme de détection intelligent
        is_anomaly = False
        score = 0.0
        raison = ""

        # Cas A : C'est un produit fréquemment utilisé (on a assez de recul historique)
        if historique_count >= 5 and ecart_type > 0:
            # Calcul du Z-Score (combien d'écarts-types séparent cette quantité de la moyenne)
            z_score = (qte - moyenne) / ecart_type
            
            # Un Z-Score > 3 signifie que l'événement a moins de 1% de chance d'arriver normalement
            if z_score > 2.5:
                is_anomaly = True
                # On normalise le score entre 0 et 1
                score = round(min(z_score / 5, 1.0), 2)
                raison = f"Volume suspect (Z-Score: {round(z_score, 1)}). Moyenne habituelle: {round(moyenne, 1)}"

        # Cas B : Historique faible ou pas d'écart-type, on applique un seuil d'alerte absolu
        else:
            if qte > 100:
                is_anomaly = True
                score = round(min(qte / 300, 1.0), 2)
                raison = f"Pic de consommation brut sans historique solide (> 100 unités)"

        # 3. Enregistrer l'anomalie si elle est validée
        if is_anomaly:
            anomaly_doc = {
                "nom_produit": name,
                "type": "Consommation excessive",
                "quantite": qte,
                "z_score": score,
                "raison": raison,
                "date": datetime.utcnow().isoformat()
            }

            es.index(index=self.index_name, document=anomaly_doc)
            print(f"🚨 [ANOMALIE CONVAINCANTE] {name} - Score: {score} | Raison: {raison}")

anomaly_service = AnomalyService()

"""
from datetime import datetime
from database.elastic import es

class AnomalyService:
    def __init__(self):
        self.index_name = "anomalies"

    async def analyze_movement(self, name: str, qte: int, state: str):
        if state != "OUT":
            return
        SEUIL_ANOMALIE = 100

        if qte > SEUIL_ANOMALIE:
            score = round(min(qte / 500, 1.0), 2)
            anomaly_doc = {
                "nom_produit": name,
                "type": "Consommation excessive",
                "quantite": qte,
                "score": score,
                "date": datetime.utcnow().isoformat()
            }

            es.index(index=self.index_name, document=anomaly_doc)
            print(f"[ANOMALIE DÉTECTÉE] {name} - Quantité: {qte} - Score: {score}")

# Instanciation du service
anomaly_service = AnomalyService()
"""
