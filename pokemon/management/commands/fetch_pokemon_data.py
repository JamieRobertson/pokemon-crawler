import logging
from pokemon.utils import fetch_pokemon, fetch_pokemon_by_name
from django.core.management.base import BaseCommand, CommandError


logger = logging.getLogger('pokemon.models')


class Command(BaseCommand):
    help = 'Fetch Pokemon data from id'

    def add_arguments(self, parser):
        parser.add_argument(
            '--name',
            type=str,
            dest='name',
            default=False,
        )

        parser.add_argument(
            '--dry-run',
            action='store_true',
            dest='dry_run',
            default=False
        )

    def handle(self, *args, **options):
        name = options.get('name', False)
        dry_run = options.get('dry_run', False)

        if name is not False:
            fetch_pokemon_by_name(
                name,
                save=not dry_run
            )
        else:
            fetch_pokemon(
                save=not dry_run
            )

