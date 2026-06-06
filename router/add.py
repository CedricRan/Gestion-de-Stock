from fastapi import APIRouter, HTTPException, status, BackgroundTasks
from services.prediction import prediction_service
from services.anomaly import anomaly_service
from utils.stock import checkout, stockRemove, stockAdd
from models.movementInput import MovementInput
from datetime import datetime
from database.elastic import es

router = APIRouter()

@router.post("/movement", status_code=status.HTTP_201_CREATED)
def create_movement(movement_data: MovementInput, background_tasks: BackgroundTasks):
    name = movement_data.name
    state = movement_data.state
    qte = movement_data.qte
    

    search_result = checkout(name)

    try:
        hits = search_result["hits"]["hits"]
        doc_id = hits[0]["_id"] if hits else None
        current_stock = hits[0]["_source"]["quantite"] if hits else 0
    except (KeyError, IndexError):
        doc_id = None
        current_stock = 0


    stock_payload = {
        "nom_produit": name,
        "quantite": qte
    }


    if state == "OUT":
        if doc_id is None or current_stock < qte:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Stock insuffisant ou produit inexistant. Stock actuel: {current_stock}"
            )

        stockRemove(stock_payload, doc_id)


    movement_document = {
        "nom_produit": name,
        "type_mouvement": state,
        "quantite": qte,
        "date_mouvement": datetime.utcnow().isoformat(),  
        "reference": "REF123", 
    }

    es.index(index="movements", document=movement_document, refresh=True)


    if state == "IN":
        stockAdd(stock_payload, doc_id)


    stock_apres_mouvement = current_stock + qte if state == "IN" else current_stock - qte


    background_tasks.add_task(
        anomaly_service.analyze_movement, 
        name=name, 
        qte=qte, 
        state=state
    )
    
    background_tasks.add_task(
        prediction_service.calculate_stock_runout, 
        name=name, 
        current_stock=stock_apres_mouvement 
    )

    return {
        "status": "success",
        "message": f"Mouvement {state} enregistré avec succès",
        "produit": name,
        "quantite_transferee": qte
    }
