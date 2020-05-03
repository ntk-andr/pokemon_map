from django.db import models


class Pokemon(models.Model):
    title = models.CharField(max_length=200)
    title_ru = models.CharField(max_length=200)
    title_en = models.CharField(max_length=200)
    title_jp = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    image = models.ImageField(null=True, blank=True)

    # previous_evolution = models.ForeignKey(
    #     'self',
    #     on_delete=models.SET_NULL,
    #     null=True, blank=True,
    #     related_name='next_evolution'
    # )

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey('Pokemon', on_delete=models.CASCADE)
    lat = models.FloatField()
    lon = models.FloatField()
    appeared_at = models.DateTimeField()
    disappeared_at = models.DateTimeField()

    level = models.IntegerField()
    health = models.IntegerField()
    strength = models.IntegerField()
    defence = models.IntegerField()
    stamina = models.IntegerField()

    def __str__(self):
        return self.pokemon.title
