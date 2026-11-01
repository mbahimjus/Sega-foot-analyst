# SEGA FOOT ANALYST — MVP technique

Ce dépôt est un squelette de démarrage, pas un bot déployé ni connecté à 1xBet.

## État
- Base SQLite et tables essentielles : incluses.
- Recherche historique dans l'ordre exact domicile–extérieur : incluse.
- Point d'entrée Telegram : inclus, à configurer avec un jeton Telegram.
- Connecteur 1xBet : non activé tant qu'une API ou un flux autorisé n'est pas confirmé.
- Tableau de bord web : phase suivante.
- Archive : aucune ligne historique n'est encore importée dans cette base.

## Installation
Python 3.11+ recommandé.
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```
Ajoute le jeton de ton bot Telegram dans `.env`, puis lance :
```bash
python -m app.bot
```

Le prototype ne fabrique aucune donnée : tant que le connecteur de matchs n'est pas configuré, il confirme simplement la réception du numéro.

Ne partage jamais ton mot de passe 1xBet. L'accès automatisé devra respecter les conditions du fournisseur.
