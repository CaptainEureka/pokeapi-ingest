from pokeapi_ingest.service.models import Pokemon, PokemonData, PokemonId


class FakePokeApiService:
    def __init__(self, url: str | None = None) -> None:
        pass

    def get_all(self, batch_size: int) -> PokemonData:
        return PokemonData(
            data=[
                Pokemon.model_validate(
                    {
                        "id": 1,
                        "name": "bulbasaur",
                        "types": [
                            {
                                "slot": 1,
                                "type": {
                                    "name": "grass",
                                    "url": "https://my-dummy-url/",
                                },
                            }
                        ],
                        "height": 1,
                        "weight": 10,
                        "base_experience": 120,
                        "abilities": [
                            {
                                "slot": 1,
                                "is_hidden": False,
                                "ability": {
                                    "name": "overgrowth",
                                    "url": "https://my-dummy-url/",
                                },
                            }
                        ],
                    }
                )
            ]
            * batch_size
        )

    def get_pokemon_by_id(self, id: PokemonId) -> PokemonData:
        return PokemonData(
            data=[
                Pokemon.model_validate(
                    {
                        "id": 1,
                        "name": "bulbasaur",
                        "types": [
                            {
                                "slot": 1,
                                "type": {
                                    "name": "grass",
                                    "url": "https://my-dummy-url/",
                                },
                            }
                        ],
                        "height": 1,
                        "weight": 10,
                        "base_experience": 120,
                        "abilities": [
                            {
                                "slot": 1,
                                "is_hidden": False,
                                "ability": {
                                    "name": "overgrowth",
                                    "url": "https://my-dummy-url/",
                                },
                            }
                        ],
                    }
                )
            ]
        )
