import json
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta

import requests
from django.conf import settings
from django.contrib import admin
from django.http import HttpResponse
from django.urls import path


def filtred_by_keys(source: dict, keys: list[str]) -> dict:
    filtred_data = {}

    for key, value in source.items():
        if key in keys:
            filtred_data[key] = value

    return filtred_data


@dataclass
class Pokemon:
    id: int
    name: str
    height: int
    weight: int
    base_experience: int

    @classmethod
    def from_raw_data(cls, raw_data: dict) -> "Pokemon":
        filtred_data = filtred_by_keys(
            raw_data,
            cls.__dataclass_fields__.keys(),
        )
        return cls(**filtred_data)


TTL = timedelta(seconds=500)
POKEMONS: dict[{str}, list[Pokemon, datetime]] = {}


def get_pokemon_from_api(name: str) -> Pokemon:
    url = settings.POKEAPI_BASE_URL + f"/{name}"
    responce = requests.get(url)
    raw_data = responce.json()

    return Pokemon.from_raw_data(raw_data)


def _get_pokemon(name: str) -> Pokemon:
    """
    Take pokemon from the cache or
    fetch it from the API and then save it to the cache.
    """
    if name in POKEMONS:
        pokemon, created_at = POKEMONS[name]

        if datetime.now() > created_at + TTL:
            del POKEMONS[name]
            return _get_pokemon(name)
    else:
        pokemon: Pokemon = get_pokemon_from_api(name)
        POKEMONS[name] = [pokemon, datetime.now()]

    return pokemon


def get_pokemon(request, name: str):
    pokemon: Pokemon = _get_pokemon(name)
    return HttpResponse(
        content_type="application/json",
        content=json.dumps(asdict(pokemon)),
    )


def get_pokemon_for_mobile(request, name: str):
    pokemon: Pokemon = _get_pokemon(name)
    result = filtred_by_keys(
        asdict(pokemon),
        ["id", "name", "base_experience"],
    )
    return HttpResponse(
        content_type="application/json",
        content=json.dumps(result),
    )


def get_all_from_cache(request) -> dict:
    pokemon_cache = {}

    for name, pokemon_info in POKEMONS.items():
        pokemon_cache[name] = asdict(pokemon_info[0])

    return HttpResponse(
        content_type="application/json",
        content=json.dumps(pokemon_cache),
    )


def delete_pokemon(request, name: str) -> str:
    if name in POKEMONS:
        del POKEMONS[name]

    return HttpResponse(f"<p>You have deleted {name}</p>")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/pokemons/<str:name>/", get_pokemon),
    path("api/pokemons/mobile/<str:name>/", get_pokemon_for_mobile),
    path("api/pokemons/", get_all_from_cache),
    path("api/pokemons/delete/<str:name>/", delete_pokemon),
]
