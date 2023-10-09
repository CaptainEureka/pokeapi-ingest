from typing import List

from pokeapi_ingest.service.models import Pokemon, PokemonData, PokemonId
from pokeapi_ingest.stockpile.observers import IProgressObserver


class FakePokeApiService:
    def __init__(self, url: str | None = None) -> None:
        self.url = url
        self.observers: List[IProgressObserver] = []

    def get_all_parallel(self, batch_size: int) -> PokemonData:
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

    def register_observer(self, observer: IProgressObserver):
        self.observers.append(observer)

    def notify_start(self, total_count: int):
        for observer in self.observers:
            observer.start(total_count)

    def notify_update(self, increment: int):
        for observer in self.observers:
            observer.update(increment)

    def notify_complete(self):
        for observer in self.observers:
            observer.complete()
