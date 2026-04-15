# Gestion Immobilière

Application Django de gestion de biens immobiliers.

## Fonctionnalités

- **Paramètres des loyers** : enregistrez une seule fois le code, l'appellation et le loyer mensuel attendu (en FCFA) pour chaque bien (appartement, studio, chambre…).
- **Dépenses fixes mensuelles** : suivez les charges récurrentes (ex. rodrigue, dépôt direct…).
- Interface d'administration Django prête à l'emploi.

## Installation

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py loaddata initial_data   # charge les données de la feuille de paramètres
python manage.py createsuperuser
python manage.py runserver
```

Accédez ensuite à http://127.0.0.1:8000/admin/ pour gérer les biens et les dépenses.

## Structure du projet

```
config/          # configuration Django (settings, urls, wsgi)
loyers/          # application principale
  models.py      # Appartement, DepenseFixeMensuelle
  admin.py       # interface d'administration
  fixtures/      # données initiales (initial_data.json)
  migrations/    # migrations de base de données
manage.py
requirements.txt
```
