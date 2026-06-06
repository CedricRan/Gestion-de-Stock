from database.elastic import es
"""
def stockAdd(doc, id):
    es.update(
            index="stock",
            id=id,
            script={
                "source": "ctx._source.quantite += params.qte",
                "params": {"qte": doc["quantite"]}
                },
            upsert=doc
            )
"""
def stockAdd(payload, doc_id=None):
    """
    Gère l'ajout de stock.
    - Si doc_id est None : Le produit n'existe pas, on le CRÉE (Indexation).
    - Sinon : Le produit existe, on incrémente sa quantité (Mise à jour).
    """
    if doc_id is None:
        res = es.index(
            index="stock",
            document=payload # payload contient déjà {"nom_produit": name, "quantite": qte}
        )
        print(f"📦 Nouveau produit créé dans le stock avec l'ID: {res['_id']}")
    
    else:
        script_update = {
            "source": "ctx._source.quantite += params.valeur",
            "params": {
                "valeur": payload["quantite"]
            }
        }
        
        es.update(
            index="stock",
            id=doc_id,
            body={"script": script_update}
        )
        print(f"🔄 Stock mis à jour pour le produit ID: {doc_id}")

def stockRemove(doc, id):
    es.update(
            index="stock",
            id=id,
            script={
                "source": "ctx._source.quantite -= params.qte",
                "params": {"qte": doc["quantite"]}
                }
            )

def checkout(name:str):
    response = es.search(
            index="stock",
            query={
                "match": {
                    "nom_produit": name
                    }
                }
            )
    print(response)
    return response

def count_stock(name:str):
    result = es.search(
            index="stock",
            query={
                "filter":{
                    "nom_produit":name
                    }
                }
            )
    print(result)


