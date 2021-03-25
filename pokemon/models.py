from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class AbstractAttribute(models.Model):
    """ Many objects returned from the PK API consist of values for these keys. """
    name = models.CharField(max_length=75)
    url = models.URLField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class Move(AbstractAttribute):
    pass


class PokemonMove(models.Model):
    """ TODO: There is more info about moves (eg: `version_group_details`). Skipping for now. """
    move = models.ForeignKey("Move", on_delete=models.CASCADE)
    pokemon = models.ForeignKey("Pokemon", on_delete=models.CASCADE)

    class Meta:
        unique_together = (("pokemon", "move"),)


# class Stat(AbstractAttribute):
#     pass


# class PokemonStat(models.Model):
#     stat = models.ForeignKey("Stat", on_delete=models.CASCADE)
#     pokemon = models.ForeignKey(Pokemon, related_name='stats', on_delete=models.CASCADE)
#     base_stat = models.IntegerField()
#     effort = models.IntegerField()
#     class Meta:
#         unique_together = (("pokemon", "stat"),)


class Pokemon(models.Model):
    external_id = models.IntegerField()  # returned from API data
    name = models.CharField(max_length=75)
    slug = models.SlugField(null=False, unique=True)
    description = models.TextField(blank=True)
    moves = models.ManyToManyField(Move, through=PokemonMove)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('pokemon:detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Pokémon'
        verbose_name_plural = 'Pokémon'


# class Thumbnail(AbstractAttribute):
#     # Called 'sprites' in API
#     pokemon = models.ForeignKey(Pokemon, related_name='thumbnails', on_delete=models.CASCADE)





# class Ability(models.Model):
    # is_hidden
    # slot

