## Development notes


During the early stages of development I used management commands to experiment eith API calls and saving to my models. 
Eg: To call the pokemon utils without saving:

```bash
$ ./manage.py fetch_pokemon_data --name="bulbasaur" --dry-run
```

To call the pokemon utils, saving one new object:

```bash
$ ./manage.py fetch_pokemon_data --name="bulbasaur"
```

### Pokémon name or slug ? 
The Pokémon API uses names and slugs interchangably. 
There does not seem to be a 'verbose name' field in the API results. 
I would like to allow editing of names so that we dont rely on slugs that could be ugly.


### Pokémon external ID ? 
Not sure what this is used for, but the each pokemon can be called using this ID, so let's store it.
