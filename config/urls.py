import json
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta

import requests
from django.conf import settings
from django.contrib import admin
from django.http import HttpResponse
from django.urls import path
from django.views.decorators.csrf import csrf_exempt


def filtred_by_keys(source: dict, keys: list[str]) -> dict:
    """
    Filters the given dictionary source based on the provided list of keys
    and returns the filtered dictionary.
    """
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
        """
        Creates a Pokemon object from raw data dictionary.
        """
        filtred_data = filtred_by_keys(
            raw_data,
            cls.__dataclass_fields__.keys(),
        )
        return cls(**filtred_data)


TTL = timedelta(seconds=5)
POKEMONS: dict[{str}, list[Pokemon, datetime]] = {}


def get_pokemon_from_api(name: str) -> Pokemon:
    """
    Retrieves Pokemon data from the API for the specified name
    and returns a Pokemon object.
    """
    url = settings.POKEAPI_BASE_URL + f"/{name}"
    responce = requests.get(url)
    raw_data = responce.json()
    return Pokemon.from_raw_data(raw_data)


def _get_pokemon(name: str) -> Pokemon:
    """
    Take pokemon from the cache or
    fetch it from the API and then save it to the cache.
    """
    try:
        pokemon, created_at = POKEMONS[name]

        if datetime.now() > created_at + TTL:
            del POKEMONS[name]
            return _get_pokemon(name)
    except KeyError:
        pokemon: Pokemon = get_pokemon_from_api(name)
        POKEMONS[name] = [pokemon, datetime.now()]

    return pokemon


@csrf_exempt
def manage_pokemon(request, name: str) -> HttpResponse:
    """
    Handles the GET and DELETE requests for retrieving or deleting a Pokemon.
    """
    try:
        if request.method == "GET":
            pokemon: Pokemon = _get_pokemon(name)
            return HttpResponse(
                content_type="application/json",
                content=json.dumps(asdict(pokemon)),
            )
        elif request.method == "DELETE":
            return delete_pokemon(name)
    except ValueError:
        return HttpResponse(f"<p>Pokemon named {name} do not exist.</p>")


@csrf_exempt
def manage_pokemon_for_mobile(request, name: str) -> HttpResponse:
    """
    Handles the GET and DELETE requests
    for retrieving or deleting a Pokemon for mobile applications.
    """
    try:
        if request.method == "GET":
            pokemon: Pokemon = _get_pokemon(name)
            result = filtred_by_keys(
                asdict(pokemon),
                ["id", "name", "base_experience"],
            )
            return HttpResponse(
                content_type="application/json",
                content=json.dumps(result),
            )
        elif request.method == "DELETE":
            return delete_pokemon(name)
    except ValueError:
        return HttpResponse(f"<p>Pokemon named {name} do not exist.</p>")


def delete_pokemon(name: str) -> HttpResponse:
    """
    Removes the pokemon from the cache.
    """
    try:
        del POKEMONS[name]
        return HttpResponse(f"<p>You have deleted {name} from the cache.</p>")
    except KeyError:
        return HttpResponse(
            f"<p>There is no Pokemon named " f"{name} in the cache.</p>"
        )


def get_all_from_cache(request) -> HttpResponse:
    """
    Returns all pokemons that are available in the cache variable.
    """
    pokemon_cache = {}

    for name, pokemon_info in POKEMONS.items():
        pokemon_cache[name] = asdict(pokemon_info[0])

    return HttpResponse(
        content_type="application/json",
        content=json.dumps(pokemon_cache),
    )


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/pokemons/<str:name>/", manage_pokemon),
    path("api/pokemons/mobile/<str:name>/", manage_pokemon_for_mobile),
    path("api/pokemons/", get_all_from_cache),
]
