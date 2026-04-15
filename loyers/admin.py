from django.contrib import admin

from .models import Appartement, DepenseFixeMensuelle


@admin.register(Appartement)
class AppartementAdmin(admin.ModelAdmin):
    list_display = ("code", "appellation", "loyer_mensuel_attendu", "devise", "note")
    search_fields = ("code", "appellation")
    list_editable = ("loyer_mensuel_attendu", "devise")


@admin.register(DepenseFixeMensuelle)
class DepenseFixeMensuelleAdmin(admin.ModelAdmin):
    list_display = ("nom", "montant", "devise", "note")
    search_fields = ("nom",)
    list_editable = ("montant", "devise")
