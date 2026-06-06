from fastapi import APIRouter
from database.elastic import es
from datetime import datetime, timedelta  # 🛠️ CORRECTION : Import de timedelta ajouté

router = APIRouter()

@router.get("/dashboard/stats")
def get_dashboard_stats():
    try:
        # 1️⃣ VRAI COMPTEUR : Références en Stock
        try:
            res_produits = es.count(index="stocks")
            total_p = res_produits.get("count", 0)
        except Exception:
            total_p = 0

        # 2️⃣ VRAI COMPTEUR : Urgences Rupture (≤ 2 jours)
        try:
            query_critique = {
                "query": {
                    "range": {
                        "jours_restants": {
                            "lte": 2
                        }
                    }
                }
            }
            res_critiques = es.count(index="stocks", body=query_critique)
            prod_c = res_critiques.get("count", 0)
        except Exception:
            prod_c = 0

        # 3️⃣ VRAI COMPTEUR : Anomalies Détectées
        try:
            res_anomalies = es.count(index="anomalies")
            total_a = res_anomalies.get("count", 0)
        except Exception:
            total_a = 0

        # 4️⃣ VRAI COMPTEUR : Flux du Jour (Mouvements d'aujourd'hui)
        try:
            aujourd_hui = datetime.utcnow().strftime("%Y-%m-%d")
            query_flux_jour = {
                "query": {
                    "range": {
                        "date_mouvement": {
                            "gte": f"{aujourd_hui}T00:00:00",
                            "lte": f"{aujourd_hui}T23:59:59"
                        }
                    }
                }
            }
            res_flux = es.count(index="movements", body=query_flux_jour)
            mov_j = res_flux.get("count", 0)
        except Exception:
            mov_j = 0

        # 📊 5️⃣ DONNÉES DU GRAPHIQUE (7 derniers jours)
        labels = []
        data_in = []
        data_out = []
        
        maintenant = datetime.utcnow()
        
        # On boucle sur les 7 derniers jours pour récupérer les volumes IN/OUT
        for i in range(6, -1, -1):
            jour = maintenant - timedelta(days=i)
            date_str = jour.strftime("%Y-%m-%d")
            labels.append(jour.strftime("%d/%m"))
            
            query_jour = {
                "query": {
                    "bool": {
                        "must": [
                            {"range": {"date_mouvement": {"gte": f"{date_str}T00:00:00", "lte": f"{date_str}T23:59:59"}}}
                        ]
                    }
                }
            }
            
            try:
                res_j = es.search(index="movements", body={"query": query_jour["query"], "size": 1000})
                mouvements = [hit["_source"] for hit in res_j["hits"]["hits"]]
                
                # Somme des quantités pour le jour en question
                somme_in = sum((m.get("quantite") or m.get("qte") or 0) for m in mouvements if m.get("type_mouvement") == "IN")
                somme_out = sum((m.get("quantite") or m.get("qte") or 0) for m in mouvements if m.get("type_mouvement") == "OUT")
                
                data_in.append(somme_in)
                data_out.append(somme_out)
            except Exception:
                data_in.append(0)
                data_out.append(0)

        # 🛠️ Renvoyer la réponse finale propre (SANS DUPLICATION)
        return {
            "total_references": total_p,
            "urgences_rupture": prod_c,
            "anomalies_detectees": total_a,
            "flux_du_jour": mov_j,
            "graphique": {
                "labels": labels,
                "entrees": data_in,
                "sorties": data_out
            }
        }

    except Exception as e:
        print(f"🚨 Erreur globale dashboard: {e}")
        return {
            "total_references": 0,
            "urgences_rupture": 0,
            "anomalies_detectees": 0,
            "flux_du_jour": 0,
            "graphique": {"labels": [], "entrees": [], "sorties": []}
        }
"""
from fastapi import APIRouter
from database.elastic import es
from datetime import datetime, timedelta

router = APIRouter()

@router.get("/dashboard/stats")
def get_dashboard_stats():
    try:
        # --- 1. COMPTEURS GLOBAUX (Récupération de tes variables) ---
        # Remplace ces simulations par tes vrais appels Elasticsearch ou services existants
        total_p = 1245  # Ta variable réelle pour total_produits
        prod_c = 14     # Ta variable réelle pour produits_critiques
        mov_j = 425     # Ta variable réelle pour mouvements_jour

        # Pour le compteur d'anomalies, on compte combien de documents existent dans l'index "anomalies"
        try:
            res_anomalies = es.count(index="anomalies")
            total_a = res_anomalies.get("count", 0)
        except Exception:
            total_a = 0

        # --- 2. PRÉPARATION DU GRAPHIQUE (7 derniers jours) ---
        labels = []
        data_in = []
        data_out = []
        
        maintenant = datetime.utcnow()
        
        for i in range(6, -1, -1):
            jour = maintenant - timedelta(days=i)
            date_str = jour.strftime("%Y-%m-%d")
            labels.append(jour.strftime("%a %d/%m")) # Format "Lun 06/06" pour Chart.js
            
            # Requête Elastic pour filtrer la journée précise
            query_jour = {
                "query": {
                    "bool": {
                        "must": [
                            {"range": {"date_mouvement": {"gte": f"{date_str}T00:00:00", "lte": f"{date_str}T23:59:59"}}}
                        ]
                    }
                }
            }
            
            try:
                res_j = es.search(index="movements", body={"query": query_jour["query"], "size": 1000})
                mouvements = [hit["_source"] for hit in res_j["hits"]["hits"]]
                
                # 🛠️ CORRECTION SYNTAXE : Extraction propre des quantités sans appeler "m(...)"
                somme_in = sum((m.get("quantite") or m.get("qte") or 0) for m in mouvements if m.get("type_mouvement") == "IN")
                somme_out = sum((m.get("quantite") or m.get("qte") or 0) for m in mouvements if m.get("type_mouvement") == "OUT")
                
                data_in.append(somme_in)
                data_out.append(somme_out)
            except Exception:
                data_in.append(0)
                data_out.append(0)

        # 🛠️ CORRECTION DICTIONNAIRE : On renvoie exactement la structure attendue par le JS
        return {
            "total_references": total_p,
            "urgences_rupture": prod_c,
            "anomalies_detectees": total_a,  # S'aligne avec data.anomalies_detectees
            "flux_du_jour": mov_j,
            "graphique": {                    # S'aligne avec data.graphique
                "labels": labels,
                "entrees": data_in,
                "sorties": data_out
            }
        }

    except Exception as e:
        # En cas de crash global, renvoyer une structure par défaut propre pour ne pas bloquer le JS
        return {
            "total_references": 0,
            "urgences_rupture": 0,
            "anomalies_detectees": 0,
            "flux_du_jour": 0,
            "graphique": {"labels": [], "entrees": [], "sorties": []}
        }
        """
