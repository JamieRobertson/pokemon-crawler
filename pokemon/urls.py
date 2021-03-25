from django.conf.urls import url
from pokemon.views import PokemonDetailView, PokemonListView

app_name = 'pokemon'

urlpatterns = [
    url(r'^$', PokemonListView.as_view(), name='list'),
    url(r'^(?P<slug>[-_\w]+)$', PokemonDetailView.as_view(), name='detail'),
]