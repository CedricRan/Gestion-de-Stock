from pydantic import BaseModel, Field
from typing import Literal
class MovementInput(BaseModel):
    name: str = Field(..., example="Produit A")
    state: Literal["IN", "OUT"] = Field(..., example="OUT")
    qte: int = Field(..., gt=0, example=10) # Quantité strictement supérieure à 0
