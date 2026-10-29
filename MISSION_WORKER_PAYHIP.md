# MISSION — Worker workflows Payhip sur l'iMac (auto-hébergé)

## Contexte
Ce dépôt contient le code des automatisations Mistral Workflows des Éditions du Discernement.
Le worker doit tourner EN PERMANENCE sur l'iMac (option B : auto-hébergement, 0 €).
Tu es l'agent local Vibe Code CLI installé sur cet iMac. Exécute cette mission de bout en bout.

## Étapes

1. **Préparer le projet**
   - Clone le dépôt : `git clone https://github.com/ericattar5-cloud/editions-workflows.git ~/editions-workflows`
   - Vérifie Python 3.12+ (`python3 --version`). Si absent : `brew install python@3.12` (Homebrew).
   - Installe les dépendances : `pip3 install --user "mistralai-workflows>=3.10" httpx`

2. **Créer le fichier de clés `.env` à la racine de ~/editions-workflows`
   - `MISTRAL_API_KEY=<clé API Mistral que tu demanderas à Éric de coller>`
   - `PAYHIP_API_KEY=<clé Payhip que tu demanderas à Éric de coller>`
   - ATTENTION : ce fichier ne doit JAMAIS être commité, jamais affiché en clair dans le journal,
     jamais envoyé dans le chat. Crée aussi un `.gitignore` contenant `.env`.
   - Éric a les deux clés dans ses notes Mac. Demande-les UNE PAR UNE, il les collera.

3. **Lancer le worker en permanence**
   - Crée un service LaunchAgent (~/Library/LaunchAgents/com.editions.workflows.plist) qui exécute :
     `cd ~/editions-workflows && PYTHONPATH=src MISTRAL_API_KEY=... PAYHIP_API_KEY=... python3 src/entrypoints/worker.py`
     (lis les valeurs depuis .env via un petit script wrapper start_worker.sh, chmod +x).
   - Charge-le : `launchctl load ~/Library/LaunchAgents/com.editions.workflows.plist`
   - Programme le redémarrage au boot (RunAtLoad + KeepAlive à true dans le plist).
   - Le worker inscrit automatiquement les workflows `payhip-list-coupons` et
     `payhip-create-lot-coupons` auprès du workspace Mistral de la clé fournie.

4. **Vérifier**
   - Attends ~30 s, vérifie que le process tourne (logs dans ~/editions-workflows/worker.log).
   - Ajoute une entrée datée dans /iCloud Drive/SAGA_NOVALIS/JOURNAL_AGENT.md :
     installation, démarrage du worker, workflows enregistrés, problèmes rencontrés.

## Interdits
- Aucune dépense, aucun achat, aucun abonnement.
- Ne jamais afficher ni commiter les clés.
- Ne pas toucher au reste du dossier SAGA_NOVALIS.

## Signalement
À la fin, rends compte à Éric en 5 lignes max : ce qui est installé, si le worker tourne,
quels workflows sont enregistrés, ce qui bloque éventuellement.
