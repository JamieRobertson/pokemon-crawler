from django.contrib import admin
from pokemon.models import Pokemon


class PokemonAdmin(admin.ModelAdmin):
    readonly_fields = ('external_id',)


admin.site.register(Pokemon, PokemonAdmin)
