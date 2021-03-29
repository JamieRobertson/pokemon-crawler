## Getting started : How to seed DB

```bash
./manage.py fetch_pokemon_data 
```
Running this will fetch and save the first 90 Pokémon to our DB


```bash
./manage.py fetch_pokemon_data --no-limit
```
Running this will attempt to save all the Pokémon - might take some time



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
Not sure what this is used for, but each pokemon can be called using this ID, so let's store it.


### Future steps :
- We could use celery to keep data relevant 
- The `description` field for our objects is intentionally blank, this could be filled 
- Start prefetching related fields before 
- Much of the content links back to the API. Do something with this
- Cache results


### What I would have done differently:
- Admin area needs as more attention. I might have gotten carried away with the front-end
- Is a M2M field with `through` fields really the best way to handle stats ? 

