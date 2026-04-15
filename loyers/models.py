from django.db import models


class Appartement(models.Model):
    """Paramètres des loyers (écrire une seule fois)."""

    code = models.CharField(max_length=100, unique=True, verbose_name="Appartement (code)")
    appellation = models.CharField(max_length=100, verbose_name="Appellation")
    loyer_mensuel_attendu = models.DecimalField(
        max_digits=12, decimal_places=0, verbose_name="Loyer mensuel attendu"
    )
    devise = models.CharField(max_length=20, default="FCFA", verbose_name="Devise / unité")
    note = models.TextField(blank=True, verbose_name="Note")

    class Meta:
        verbose_name = "Appartement"
        verbose_name_plural = "Appartements"
        ordering = ["code"]

    def __str__(self):
        return f"{self.code} – {self.loyer_mensuel_attendu} {self.devise}/mois"


class DepenseFixeMensuelle(models.Model):
    """Dépenses fixes mensuelles."""

    nom = models.CharField(max_length=200, verbose_name="Désignation")
    montant = models.DecimalField(max_digits=12, decimal_places=0, verbose_name="Montant")
    devise = models.CharField(max_length=20, default="FCFA", verbose_name="Devise")
    note = models.TextField(blank=True, verbose_name="Note")

    class Meta:
        verbose_name = "Dépense fixe mensuelle"
        verbose_name_plural = "Dépenses fixes mensuelles"
        ordering = ["nom"]

    def __str__(self):
        return f"{self.nom} – {self.montant} {self.devise}"
