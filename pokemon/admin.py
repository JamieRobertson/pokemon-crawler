from django.contrib import admin
from pokemon.models import Pokemon


# class PokemonAdmin(admin.ModelAdmin):


admin.site.register(Pokemon)
