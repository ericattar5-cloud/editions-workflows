# editions-workflows

Workflows Mistral — automatisations des Éditions du Discernement (Payhip, coupons, audit).

- `payhip-list-coupons` : liste les coupons Payhip (valide la clé API).
- `payhip-create-lot-coupons` : crée les coupons LOT3 (-15 % dès 2,97 €) et LOT10 (-40 % dès 9,90 €)
  sur la collection « récits courts » (tome I exclu).

**Aucun secret dans ce dépôt.** Les clés viennent du coffre (déploiement géré) ou d'un fichier .env local (auto-hébergé).

## Lancement local (iMac)
```
pip3 install "mistralai-workflows>=3.10" httpx
PYTHONPATH=src python3 src/entrypoints/worker.py   # .env chargé par start_worker.sh
```
