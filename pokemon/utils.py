import logging
import requests
from django.db import IntegrityError, transaction

from pokemon.models import Move, Pokemon, PokemonMove


logger = logging.getLogger(__name__)
API_BASE = 'https://pokeapi.co/api/v2'


def save_pokemon(data):
    pokemon, created = Pokemon.objects.update_or_create(
        external_id=data['id'],
        name=data['name'],
    )
    if pokemon:
        if data.get('moves', None):
            for move in data['moves']:
                print(move)
                try:
                    with transaction.atomic():
                        move, _ = Move.objects.get_or_create(
                            name=move['move']['name'],
                            url=move['move']['url'],
                        )
                        PokemonMove.objects.create(
                            pokemon=pokemon,
                            move=move,
                        )
                        # pokemon.pokemonmove_set.add(
                        #     PokemonMove.objects.create(
                        #         pokemon=pokemon,
                        #         move=move,
                        #     )
                        # )
                except IntegrityError:
                    pass

    if created:
        logger.info(f"New Pokémon <{pokemon.name}> added")
    else:
        logger.info(f"Pokémon <{pokemon.name}> has been updated")


def fetch_pokemon_by_name(name, save=True):
    if not type(name) is str:
        raise TypeError("name must be an string")

    endpoint = f"{API_BASE}/pokemon/{name}"
    try:
        r = requests.get(url=endpoint)
    except Exception as e:
        logger.error("Error fetching Pokémon", exception=e)
        raise

    if not r.ok:
        logger.error(f"Error fetching Pokémon. Status code: <{r.status_code}>")
        raise

    logger.debug(r.json())
    # print(r.json())

    if save:
        save_pokemon(r.json())


def fetch_pokemon(offset=0, limit=60, endpoint=None, save=True):
    if not endpoint:
        endpoint = f"{API_BASE}/pokemon/?offset={offset}&limit={limit}"

    try:
        r = requests.get(url=endpoint)
    except Exception as e:
        logger.error("Error fetching Pokémon", exception=e)
        raise
    else:
        if not r.ok:
            logger.error(f"Error fetching Pokémon. Status code: <{r.status_code}>")
            raise

        data = r.json()
        if data.get('results', None):
            for result in data['results']:
                fetch_pokemon_by_name(result['name'], save=save)

        # Call this function recursively if there are more Pokémon
        if data.get('next', None):
            fetch_pokemon(endpoint=data['next'])


