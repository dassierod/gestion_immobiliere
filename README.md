# Gestion Immobilière

Application web Flask pour la gestion locative. Elle remplace le fichier Excel de suivi des loyers et dépenses par une interface web complète.

## Fonctionnalités

- **Tableau de bord** mensuel (identique au tableau Excel) : statut de paiement par chambre, totaux, dépenses, dépôts
- **Chambres** : ajout / modification / suppression des chambres avec loyer mensuel
- **Paiements** : saisie et suivi des paiements par chambre et par mois
- **Dépenses** : suivi des charges (hygiène, caissier) et du dépôt réel
- **Paramètres** : valeurs par défaut (loyers, frais caissier, etc.)
- **Export Excel** : génère un fichier `.xlsx` formaté identique au tableau de bord

## Installation

```bash
pip install -r requirements.txt
```

## Lancement

```bash
python run.py
```

Puis ouvrir [http://localhost:5000](http://localhost:5000). Créer un compte via la page **S'inscrire**.

## Structure

```
app/
  __init__.py       # Factory Flask
  models.py         # Modèles SQLAlchemy (User, Room, Payment, Expense, Parameter)
  forms.py          # Formulaires WTForms
  routes/
    auth.py         # Inscription / connexion / déconnexion
    dashboard.py    # Tableau de bord principal
    rooms.py        # Gestion des chambres
    payments.py     # Gestion des paiements
    expenses.py     # Gestion des dépenses
    parameters.py   # Paramètres de l'application
    export.py       # Export Excel (openpyxl)
  templates/        # Templates Jinja2 (Bootstrap 5)
run.py              # Point d'entrée
requirements.txt
```
