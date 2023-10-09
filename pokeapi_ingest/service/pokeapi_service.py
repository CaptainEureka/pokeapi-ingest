import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Dict, List, Optional, Protocol

import requests
from requests.adapters import HTTPAdapter

from pokeapi_ingest.service.models import Pokemon, PokemonData, PokemonId
from pokeapi_ingest.stockpile.observers import IProgressObserver

logger = logging.getLogger()


class IPokeApiService(Protocol):
    def get_pokemon_by_id(self, id: PokemonId) -> PokemonData:
        ...

    def get_all(self, batch_size: int) -> PokemonData:
        ...

    def register_observer(self, observer: IProgressObserver):
        ...

    def notify_start(self, total_count: int):
        ...

    def notify_update(self, increment: int):
        ...

    def notify_complete(self):
        ...


class PokeApiService(IPokeApiService):
    def __init__(self, url: str):
        self.url = url
        self.session: requests.Session = requests.session()
        self.observers: List[IProgressObserver] = []
        self._configure_retry()

    def _configure_retry(self) -> None:
        adapter = HTTPAdapter(max_retries=3, pool_connections=100, pool_maxsize=100)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

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

    def _fetch_data(self, url: str) -> Optional[Dict[str, Any]]:
        try:
            response = self.session.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"An error occurred while fetching data: {e}")
            raise

    def get_pokemon_by_id(self, id: PokemonId) -> PokemonData:
        logger.info(f"Fetching Pokemon by ID: {id}")
        data = self._fetch_data(f"{self.url}/{id}/")
        return PokemonData(data=[Pokemon.model_validate(data)])

    def _fetch_batch(self, url: str, offset: int, limit: int) -> List[Pokemon]:
        logger.debug(f"Fetching Batch {offset}:{offset+limit}")

        formatted_url = f"{url}/?offset={offset}&limit={limit}"
        logger.debug(f"{formatted_url=}")

        data = self._fetch_data(formatted_url)
        if data is None:
            return []

        results = data.get("results", [])

        parsed_results = [
            Pokemon.model_validate(self._fetch_data(url))
            for result in results
            if (url := result.get("url"))
        ]
        return parsed_results

    def get_all_parallel(self, batch_size: int = 20) -> PokemonData:
        initial_data = self._fetch_data(self.url)

        if initial_data is None:
            return PokemonData()

        total_count = initial_data.get("count", 0)
        self.notify_start(total_count)

        # Divide the task into smaller tasks
        offsets = list(range(0, total_count, batch_size))

        all_results = []
        with ThreadPoolExecutor() as executor:
            future_to_batch = {
                executor.submit(self._fetch_batch, self.url, offset, batch_size): offset
                for offset in offsets
            }

            for future in as_completed(future_to_batch):
                offset = future_to_batch[future]
                try:
                    data = future.result()
                except Exception as exc:
                    logger.error(
                        f"Batch at offset {offset} generated an exception: {exc}"
                    )
                else:
                    if data:
                        self.notify_update(len(data))
                        all_results.extend(data)

        logger.debug("Data fetched!")
        self.notify_complete()

        # Futures doesn't guarantee order, needs to be sorted
        return PokemonData(data=sorted(all_results, key=lambda p: p.id))

    def get_all(self, batch_size: int = 20) -> PokemonData:
        data = self._fetch_data(f"{self.url}/?limit={batch_size}")

        if data is None:
            return PokemonData()

        all_results = [
            Pokemon.model_validate(self._fetch_data(result.get("url")))
            for result in data.get("results", [])
            if result.get("url")
        ]
        next_url = data.get("next")

        while next_url:
            data = self._fetch_data(next_url)

            if data is None:
                break

            next_url = data.get("next")
            all_results.extend(
                [
                    Pokemon.model_validate(self._fetch_data(result.get("url")))
                    for result in data.get("results", [])
                    if result.get("url")
                ]
            )

        return PokemonData(data=all_results)
