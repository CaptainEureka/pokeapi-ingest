from unittest.mock import patch

import pytest
from typer.testing import CliRunner

from tests.fakes import FakePokeApiService

runner = CliRunner()

pytestmarks = pytest.mark.integ


class TestStockpileCLI:
    def test_ingest_command_without_pokemon_id_ingests_all(self):
        with patch(
            "pokeapi_ingest.service.pokeapi_service.PokeApiService",
            new=FakePokeApiService,
        ):
            from pokeapi_ingest.stockpile.cli import app

            result = runner.invoke(app=app, args=["ingest"])
            assert result.exit_code == 0

    def test_ingest_command_with_pokemon_id_ingests_one(self):
        with patch(
            "pokeapi_ingest.service.pokeapi_service.PokeApiService",
            new=FakePokeApiService,
        ):
            from pokeapi_ingest.stockpile.cli import app

            result = runner.invoke(app=app, args=["ingest", "--pokemon-id", "1"])
            assert result.exit_code == 0
