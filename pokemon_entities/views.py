import folium
import json

from django.core.exceptions import ObjectDoesNotExist 

from django.http import HttpResponseNotFound
from django.shortcuts import render

from pokemon_entities.models import Pokemon, PokemonEntity

MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = "https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832&fill=transparent"


def add_pokemon(folium_map, lat, lon, name, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        tooltip=name,
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    for pokemon_entity in PokemonEntity.objects.all():
        pokemon = pokemon_entity.pokemon
        img_url = request.build_absolute_uri(pokemon.image.url) if pokemon.image else DEFAULT_IMAGE_URL
        add_pokemon(
            folium_map, pokemon_entity.lat, pokemon_entity.lon,
            pokemon.title_ru, img_url)

    pokemons_on_page = []
    for pokemon in Pokemon.objects.all():
        img_url = request.build_absolute_uri(pokemon.image.url) if pokemon.image else DEFAULT_IMAGE_URL
        pokemons_on_page.append({
            'pokemon_id': pokemon.pk,
            'img_url': img_url,
            'title_ru': pokemon.title_ru,
        })

    return render(request, "mainpage.html", context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    try:
        pokemon = Pokemon.objects.get(id=pokemon_id)
    except ObjectDoesNotExist:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')

    pokemon.img_url = request.build_absolute_uri(pokemon.image.url)

    pokemon_on_page = {
        'pokemon_id': pokemon_id,
        'img_url': pokemon.img_url,
        'title_ru': pokemon.title_ru,
        'title_en': pokemon.title_en,
        'title_jp': pokemon.title_jp,
        'description': pokemon.description,
        'title': pokemon.title,
    }

    next_evolution = pokemon.next.first()
    previous_evolution = pokemon.previous_evolution

    if previous_evolution:
        pokemon_on_page['previous_evolution'] = {
            'pokemon_id': previous_evolution.id,
            'img_url': request.build_absolute_uri(previous_evolution.image.url),
            'title_ru': previous_evolution.title_ru
        }

    if next_evolution:
        pokemon_on_page['next_evolution'] = {
            'pokemon_id': pokemon.next.first().id,
            'img_url': request.build_absolute_uri(pokemon.next.first().image.url),
            'title_ru': pokemon.next.first().title_ru
        }

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    pokemon_entities = pokemon.entities.all()
    for pokemon_entity in pokemon_entities:
        add_pokemon(
            folium_map, pokemon_entity.lat, pokemon_entity.lon,
            pokemon.title_ru, pokemon.img_url)

    return render(request, "pokemon.html", context={'map': folium_map._repr_html_(),
                                                    'pokemon': pokemon_on_page})
