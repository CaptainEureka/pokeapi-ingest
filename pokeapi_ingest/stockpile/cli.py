import os
from pathlib import Path
from typing import Annotated, Optional

import typer
from dotenv import load_dotenv

from pokeapi_ingest.stockpile.logging import configure_logging
from pokeapi_ingest.stockpile.main import main

app = typer.Typer()

logger = configure_logging()

load_dotenv()


@app.command(help="Ingest Data from PokeAPI")
def ingest(
    pokemon_id: Annotated[
        Optional[int],
        typer.Option(
            help=(
                "The ID of the specific Pokemon to ingest. "
                "If omitted, data for all Pokemon will be ingested."
            )
        ),
    ] = None,
    output_path: Annotated[
        Optional[Path],
        typer.Option(
            help=(
                "The file path where the ingested data will be saved. "
                "Defaults to 'pokemon_data.json' in a timestamped run folder."
            )
        ),
    ] = None,
    parallel: bool = typer.Option(
        default=True, help="Parallelize the download. Defaults to `True`"
    ),
):
    main(pokemon_id, output_path, parallelize=parallel)


@app.command(help="Open PokeAPI docs")
def docs():
    typer.launch(os.environ["POKEAPI_DOCS_URL"])
