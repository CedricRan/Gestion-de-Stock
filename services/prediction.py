from datetime import datetime, timedelta
from database.elastic import es

class PredictionService:
    def __init__(self):
        self.index_alerts = "alerts"

    # 🛠️ CORRECTION : Passage en fonction standard (sans async)
    async def calculate_stock_runout(self, name: str, current_stock: int):
        """
        Calcule la vitesse de consommation et prédit le nombre de jours
        avant la rupture de stock. Génère ou nettoie les alertes.
        """
        il_y_a_30_jours = (datetime.utcnow() - timedelta(days=30)).isoformat()

        # 🛠️ CORRECTION : Utilisation directe des champs du mapping (sans .keyword)
        query = {
            "query": {
                "bool": {
                    "must": [
                        {"term": {"nom_produit": name}},      # Mapping exact keyword
                        {"term": {"type_mouvement": "OUT"}},  # Mapping exact keyword
                        {"range": {"date_mouvement": {"gte": il_y_a_30_jours}}}
                    ]
                }
            },
            "aggs": {
                "total_sorties": {
                    "sum": {"field": "quantite"}
                }
            },
            "size": 0
        }

        try:
            response = es.search(index="movements", body=query)
            
            # 🎯 PRINTS DE DÉBOGAGE POUR TON TERMINAL
            nb_mouvements = response['hits']['total']['value']
            print(f"🔍 [DEBUG PREDICTION] {name} -> Mouvements 'OUT' trouvés sur 30j : {nb_mouvements}")
            
            total_consomme = response["aggregations"]["total_sorties"]["value"] or 0
            print(f"🔍 [DEBUG PREDICTION] {name} -> Total quantité consommée : {total_consomme}")
        except Exception as e:
            print(f"❌ Erreur lors de l'agrégation de prédiction : {e}")
            total_consomme = 0

        mj_c = total_consomme / 30

        if mj_c == 0:
            self._delete_alert_if_exists(name)
            return

        jours_restants = current_stock / mj_c
        print(f"🔍 [DEBUG PREDICTION] {name} -> Jours restants calculés : {round(jours_restants, 1)} jours")

        if jours_restants <= 7:
            if jours_restants <= 3:
                niveau = "CRITICAL"
                raison = f"Urgence critique : rupture prévue dans moins de 3 jours."
            else:
                niveau = "WARNING"
                raison = f"Approvisionnement requis : stock en baisse constante."

            alert_doc = {
                "nom_produit": name,
                "type": niveau,
                "jours_restants": round(jours_restants, 1),
                "consommation_moyenne": round(mj_c, 2),
                "stock_actuel": current_stock,
                "raison": raison,
                "date": datetime.utcnow().isoformat()
            }

            es.index(index=self.index_alerts, id=name, document=alert_doc)
            print(f"⚠️ [ALERTE PROVISIONNEMENT] {name} classé en {niveau} ({round(jours_restants, 1)}j restants)")
        
        else:
            self._delete_alert_if_exists(name)

    # 🛠️ CORRECTION : Passage en fonction standard (sans async)
    def _delete_alert_if_exists(self, name: str):
        """Supprime proprement une alerte de l'index si elle existe."""
        try:
            es.delete(index=self.index_alerts, id=name)
            print(f"✨ [DEBUG PREDICTION] Ancienne alerte nettoyée pour {name}")
        except Exception:
            pass 
    # À ajouter à la fin de PredictionService dans services/prediction.py

    def get_vitesse_consommation(self, name: str) -> float:
        """Calcule uniquement la MJc d'un produit sur les 30 derniers jours."""
        from datetime import datetime, timedelta
        il_y_a_30_jours = (datetime.utcnow() - timedelta(days=30)).isoformat()

        query = {
            "query": {
                "bool": {
                    "must": [
                        {"term": {"nom_produit": name}},
                        {"term": {"type_mouvement": "OUT"}},
                        {"range": {"date_mouvement": {"gte": il_y_a_30_jours}}}
                    ]
                }
            },
            "aggs": {
                "total_sorties": {"sum": {"field": "quantite"}}
            },
            "size": 0
        }
        try:
            response = es.search(index="movements", body=query)
            total_consomme = response["aggregations"]["total_sorties"]["value"] or 0
            return total_consomme / 30
        except Exception:
            return 0.0
prediction_service = PredictionService()
