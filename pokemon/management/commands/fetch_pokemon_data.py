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

        parser.add_argument(
            '--no-limit',
            action='store_true',
            dest='no_limit',
            default=False
        )

    def handle(self, *args, **options):
        name = options.get('name', False)
        dry_run = options.get('dry_run', False)
        no_limit = options.get('no_limit', False)

        if name is not False:
            fetch_pokemon_by_name(
                name,
                save=not dry_run
            )
        else:
            if no_limit is not False:
                fetch_pokemon(
                    limit_results=None,
                    save=not dry_run
                )
            else:
                # Fetching all Pokemon, might take some time 
                fetch_pokemon(
                    save=not dry_run
                )
