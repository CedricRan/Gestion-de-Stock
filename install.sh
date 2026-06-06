#!/bin/bash
set -e

echo "Installation des dépendances..."

python3 -m venv elastic-venv

elastic-venv/bin/python3 -m pip install --upgrade pip
elastic-venv/bin/python3 -m pip install -r requirements.txt

echo "Fin installation"
echo "========================"
echo "Initialisation"

elastic-venv/bin/python3 -m dataCreation.alert
elastic-venv/bin/python3 -m dataCreation.anomaly
elastic-venv/bin/python3 -m dataCreation.movement
elastic-venv/bin/python3 -m dataCreation.stock

echo " "
echo "Lancement de l'API..."

elastic-venv/bin/python3 -m uvicorn main:app 

echo "========================"
