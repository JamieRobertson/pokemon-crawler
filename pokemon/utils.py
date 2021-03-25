import logging
import requests
from django.db import IntegrityError, transaction

from pokemon.models import (
    Pokemon,
    Move,
    PokemonMove,
    Sprite,
    Stat,
    PokemonStat,
)


logger = logging.getLogger(__name__)
API_BASE = 'https://pokeapi.co/api/v2'


def save_pokemon(data):
    pokemon, created = Pokemon.objects.update_or_create(
        name=data['name'],
        defaults={
            'external_id': data['id']
        }
    )
    if pokemon:
        if data.get('moves', None):
            for move in data['moves']:
                try:
                    with transaction.atomic():
                        move_obj, _ = Move.objects.get_or_create(
                            name=move['move']['name'],
                            url=move['move']['url'],
                        )
                        _, _ = PokemonMove.objects.update_or_create(
                            pokemon=pokemon,
                            move=move_obj,
                        )
                except IntegrityError:
                    pass

        if data.get('stats', None):
            for stat in data['stats']:
                try:
                    with transaction.atomic():
                        stat_obj, _ = Stat.objects.get_or_create(
                            name=stat['stat']['name'],
                            url=stat['stat']['url'],
                        )
                        _, _ = PokemonStat.objects.update_or_create(
                            pokemon=pokemon,
                            stat=stat_obj,
                            base_stat=stat.get('base_stat', None),
                            effort=stat.get('effort', None),
                        )
                except IntegrityError:
                    pass

        if data.get('sprites', None):
            # Save featured image
            try:
                official_artwork = data['sprites']['other']['official-artwork']['front_default']
                with transaction.atomic():
                    sprite, _ = Sprite.objects.update_or_create(
                        name='official_artwork',
                        url=official_artwork,
                        pokemon=pokemon,
                    )

            except KeyError as exc:
                # No official artwork :(
                # TODO: handle other types of artworks
                print(exc)
                pass
            except IntegrityError as exc_2:
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
        logger.error(f"Error fetching Pokémon <{name}>. Status code: <{r.status_code}>")
        print(f"Error fetching Pokémon <{name}>. Status code: <{r.status_code}>")
        raise

    logger.debug(r.json())

    if save:
        save_pokemon(r.json())


def fetch_pokemon(offset=0, limit=30, endpoint=None, save=True, limit_results=90, loop_index=1):
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
            if limit_results and (limit_results <= loop_index * limit):
                return

            fetch_pokemon(endpoint=data['next'], loop_index=loop_index+1)


