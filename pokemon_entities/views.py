import folium
from django.http import HttpResponseNotFound
from django.shortcuts import get_object_or_404, render
from pokemon_entities.models import Pokemon, PokemonEntity
from django.utils.timezone import localtime


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):

    local_time = localtime()
    pokemon_entities = PokemonEntity.objects.filter(appeared_at__lte=local_time, disappeared_at__gte=local_time)
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    for pokemon_entity in pokemon_entities:
        add_pokemon(
            folium_map, pokemon_entity.lat,
            pokemon_entity.lon,
            request.build_absolute_uri(pokemon_entity.pokemon.image.url)
        )

    pokemons = Pokemon.objects.all()
    pokemons_on_page = []
    for pokemon in pokemons:
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': request.build_absolute_uri(pokemon.image.url),
            'title_ru': pokemon.title,
            'description': pokemon.description,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):

    local_time = localtime()
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    pokemon = get_object_or_404(Pokemon, id=pokemon_id)
    pokemon_entities = PokemonEntity.objects.filter(pokemon=pokemon, appeared_at__lte=local_time, disappeared_at__gte=local_time)
    for pokemon_entity in pokemon_entities:
        add_pokemon(
            folium_map, pokemon_entity.lat,
            pokemon_entity.lon,
            request.build_absolute_uri(pokemon_entity.pokemon.image.url)
        )

    chosen_pokemon = {
        'title_ru': pokemon.title,
        'title_en': pokemon.title_en,
        'title_jp': pokemon.title_jp,
        'img_url': request.build_absolute_uri(pokemon.image.url),
        'description': pokemon.description,
    }



    if pokemon.previous_evolution is not None:
        chosen_pokemon['previous_evolution'] = {
                                            "pokemon_id": pokemon.previous_evolution.id,
                                            "title_ru": pokemon.previous_evolution.title,
                                            "img_url": request.build_absolute_uri(pokemon.previous_evolution.image.url),
                                            }
  
    next_evolution = pokemon.next_evolutions.first()
    if next_evolution is not None:
        chosen_pokemon['next_evolution'] = {
                                            "pokemon_id": next_evolution.id,
                                            "title_ru": next_evolution.title,
                                            "img_url": request.build_absolute_uri(next_evolution.image.url),
                                            }

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': chosen_pokemon
    })
