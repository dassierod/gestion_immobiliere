# Gestion Immobilière

Application web de gestion immobilière développée avec Flask (Python). Elle permet de gérer votre parc immobilier : biens, locataires, contrats de location, et suivi des paiements, avec import/export Excel.

## Fonctionnalités

- **Tableau de bord** : vue d'ensemble (biens loués/disponibles, revenus du mois, paiements récents, contrats expirant bientôt)
- **Biens immobiliers** : gestion complète (appartements, maisons, bureaux, etc.) avec recherche et filtres
- **Locataires** : fiche locataire avec historique des contrats
- **Contrats de location** : suivi des baux (date début/fin, loyer, charges, caution)
- **Paiements** : suivi des loyers et paiements (Payé / En attente / Retard)
- **Propriétaires** : gestion des propriétaires de biens
- **Export Excel** : export de toutes les données (biens, locataires, contrats, paiements) en fichier `.xlsx`
- **Import Excel** : import de biens et locataires depuis un fichier Excel

## Installation

```bash
# Cloner le dépôt
git clone https://github.com/dassierod/gestion_immobiliere.git
cd gestion_immobiliere

# Créer un environnement virtuel
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

# Installer les dépendances
pip install -r requirements.txt

# Lancer l'application
python app.py
```

L'application sera disponible à l'adresse : http://localhost:5000

## Première utilisation

Cliquez sur le bouton **Démo** (en haut à droite) pour charger des données d'exemple et explorer l'application.

## Format d'import Excel

Le fichier Excel doit contenir les feuilles suivantes :

**Feuille `Biens`** — colonnes :
`Référence | Type | Adresse | Ville | Code Postal | Surface (m²) | Nb Pièces | Loyer (€) | Charges (€) | Statut | Description`

**Feuille `Locataires`** — colonnes :
`Nom | Prénom | Email | Téléphone | Adresse | Date de naissance (JJ/MM/AAAA) | Profession | Revenu mensuel (€)`

> Téléchargez le modèle depuis **Données → Exporter Excel**, puis remplissez-le et réimportez-le.

## Technologies

- **Backend** : Python 3, Flask, SQLAlchemy (SQLite)
- **Frontend** : Bootstrap 5.3, Bootstrap Icons (servis localement)
- **Excel** : openpyxl, pandas
