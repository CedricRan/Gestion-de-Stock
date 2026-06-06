from fastapi import APIRouter
from database.elastic import es
router = APIRouter()
@router.get("/anomalies")
def get_all_anomalies():
    try:
        response = es.search(
            index="anomalies",
            body={
                "query": {"match_all": {}},
                "sort": [{"date": {"order": "desc"}}],
                "size": 20
            }
        )
        hits = response["hits"]["hits"]
        anomalies = [hit["_source"] for hit in hits]
        return anomalies

    except Exception as e:
        return []
