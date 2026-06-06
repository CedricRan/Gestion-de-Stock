from router.add import router as add_router 
from router.anomaly import router as anomaly_router
from router.alert import router as alert_router
from router.stock_urgence import router as urgence_router
from router.consommation import router as consommation_router
from router.historique import router as historique_router
from router.dashbord import router as dashbord_router
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
app = FastAPI()

app.include_router(add_router)
app.include_router(anomaly_router)
app.include_router(urgence_router)
app.include_router(consommation_router)
app.include_router(alert_router)
app.include_router(historique_router)
app.include_router(dashbord_router)
@app.get("/")
def home():
    return FileResponse("index.html")
