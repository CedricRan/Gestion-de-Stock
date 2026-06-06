from fastapi import APIRouter
from database.elastic import es
router = APIRouter()
@router.get("/alerts")
def get_all_alerts():
    """Renvoie les alertes de provisionnement triées par urgence (jours restants croissants)"""
    try:
        response = es.search(
            index="alerts",
            body={
                "query": {"match_all": {}},
                "sort": [{"jours_restants": {"order": "asc"}}],
                "size": 20
            }
        )
        return [hit["_source"] for hit in response["hits"]["hits"]]
    except Exception:
        return []
