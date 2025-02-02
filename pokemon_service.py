# pokemon_service.py
import requests

class PokemonService:
    BASE_URL = "https://pokeapi.co/api/v2/pokemon"

    def get_pokemon_info(self, pokemon_name):
        url = f"{self.BASE_URL}/{pokemon_name}"
        response = requests.get(url)

        if response.status_code == 200:
            return response.json()
        else:
            return None
