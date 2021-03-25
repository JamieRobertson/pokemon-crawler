from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from pokemon.models import Pokemon


class PokemonListView(ListView):
    """"""
    model = Pokemon
    template_name = 'pokemon_list.html'
    paginate_by = 30


class PokemonDetailView(DetailView):
    """"""
    model = Pokemon
    template_name = 'pokemon_detail.html'
