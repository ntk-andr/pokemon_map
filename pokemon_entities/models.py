from django.db import models


class Pokemon(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название')
    title_ru = models.CharField(max_length=200, verbose_name='Название ru', blank=True)
    title_en = models.CharField(max_length=200, verbose_name='Название en', blank=True)
    title_jp = models.CharField(max_length=200, verbose_name='Название jp', blank=True)
    description = models.TextField(verbose_name='Описание', blank=True)
    image = models.ImageField(null=True, blank=True, verbose_name='Изображение')

    previous_evolution = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='next',
        verbose_name='Из кого эволюционирует'
    )

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey('Pokemon', on_delete=models.CASCADE, related_name='entities', verbose_name='Покемон')
    lat = models.FloatField(verbose_name='Широта')
    lon = models.FloatField(verbose_name='Долгота')
    appeared_at = models.DateTimeField(verbose_name='Время появления')
    disappeared_at = models.DateTimeField(verbose_name='Время исчезновения')

    level = models.IntegerField(verbose_name='Уровень')
    health = models.IntegerField(verbose_name='Здоровье')
    strength = models.IntegerField(verbose_name='Атака')
    defence = models.IntegerField(verbose_name='Защита')
    stamina = models.IntegerField(verbose_name='Выносливость')

    def __str__(self):
        return self.pokemon.title
