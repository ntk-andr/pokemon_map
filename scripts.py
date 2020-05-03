import os

import json
import random
import django

from datetime import timedelta

from django.conf import settings
from django.core.files import File
from django.utils.timezone import now

os.environ['DJANGO_SETTINGS_MODULE'] = 'pogomap.settings'

django.setup()

from pokemon_entities.models import Pokemon, PokemonEntity


def get_pokemons():
    """Получаем тестовые данные о покемонах из файла."""
    with open("pokemon_entities/pokemons.json", encoding="utf-8") as database:
        return json.load(database)['pokemons']


def delete_db():
    """Удаляем файл БД и миграции."""
    os.system('rm -r media/*')
    os.system('rm -r pokemon_entities/migrations/0*.py')
    os.system('rm -r db.sqlite3')


def create_superuser():
    """Создаем суперюзера."""
    os.system('python manage.py migrate')
    print('createsuperuser')
    os.system('python manage.py createsuperuser --email ""')


def create_migraions():
    """Накатываем миграции."""
    os.system('python manage.py makemigrations')
    os.system('python manage.py migrate')


def create_img_for_pokemons():
    """Создание изображения для покемонов."""
    for pokemon in pokemons:
        try:
            pokemon_id = pokemon['pokemon_id']
            pokemon = Pokemon.objects.get(id=pokemon_id)
            filepath = f'images/{pokemon_id}.png'
            with open(filepath, 'rb') as file:
                data = File(file)
                filename = f'pokemon_{pokemon_id}.png'
                pokemon.image.save(filename, data, False)
            pokemon.save()
        except Exception as e:
            print(e)


def create_pokemons():
    """Создание видов покемонов."""
    for pokemon in pokemons:
        Pokemon.objects.create(
            title=pokemon['title_ru'],
            title_ru=pokemon['title_ru'],
            title_en=pokemon['title_en'],
            title_jp=pokemon['title_jp'],
            description=pokemon['description']
        )


def create_evolutions():
    """Создание эволюций покемонов."""
    for pokemon in pokemons:
        pokemon_id = pokemon['pokemon_id']
        pokemon_item = Pokemon.objects.get(id=pokemon_id)
        if 'previous_evolution' in pokemon:
            pokemon_item.previous_evolution_id = pokemon['previous_evolution']['pokemon_id']
            pokemon_item.save()


def create_pokemons_entities():
    """Создание покемонов."""
    for pokemon in pokemons:
        for pokemon_entity in pokemon['entities']:
            level = pokemon_entity['level']
            PokemonEntity.objects.create(
                pokemon_id=pokemon['pokemon_id'],
                lat=pokemon_entity['lat'],
                lon=pokemon_entity['lon'],
                appeared_at=now(),
                disappeared_at=now() + timedelta(days=random.randint(1, 30)),
                level=level,
                health=level + random.randint(1, 30),
                strength=level + random.randint(1, 30),
                defence=level + random.randint(1, 30),
                stamina=level + random.randint(1, 30),

            )


if __name__ == "__main__":
    pokemons = get_pokemons()
    delete_db()
    create_superuser()
    create_migraions()
    create_pokemons()
    create_evolutions()
    create_img_for_pokemons()
    create_pokemons_entities()
