import os
from datetime import datetime
from pathlib import Path
from types import NoneType
from typing import Generator, Tuple
from zoneinfo import ZoneInfo

from rich import print
from rich.progress import BarColumn, Progress, TextColumn, TimeElapsedColumn

from pokeapi_ingest.service.models import PokemonData, PokemonId
from pokeapi_ingest.service.pokeapi_service import PokeApiService
from pokeapi_ingest.stockpile.observers import RichProgressObserver

progress = Progress(
    TextColumn(
        "[bold green]{task.fields[filename]}",
        justify="right",
    ),
    BarColumn(),
    "[progress.percentage]{task.percentage:>3.1f}%",
    TimeElapsedColumn(),
)

DEFAULT_FILE_STEM = "pokemon_data"


def generate_json_and_status(
    pokemon_data: PokemonData,
) -> Generator[Tuple[str, int], None, None]:
    """Generate serialized JSON strings and current progress."""
    total_items = len(pokemon_data.data)
    for idx, pokemon in enumerate(pokemon_data.to_iter()):
        yield (pokemon.model_dump_json(indent=2), int((idx / total_items) * 100))


def save_to_json_file(pokemon_data: PokemonData, output_dir: Path) -> None:
    """Save to JSON file while showing a progress bar."""
    timestamp = datetime.now(tz=ZoneInfo("UTC")).strftime("%Y%m%d%H%M%S")
    run_folder = output_dir / f"run_{timestamp}"
    run_folder.mkdir(parents=True, exist_ok=True)
    file_path = run_folder / f"{DEFAULT_FILE_STEM}.json"

    with file_path.open("w") as f, progress as p:
        task = p.add_task(
            "Writing...",
            filename=file_path.name,
            total=99,
        )

        f.write("[")  # Start of JSON array

        for idx, (json_str, progress_percentage) in enumerate(
            generate_json_and_status(pokemon_data)
        ):
            if idx > 0:
                f.write(", ")  # Separator between items
            f.write(json_str)
            p.update(task, completed=progress_percentage, advance=1)

        f.write("]")

    print(f"\n📁 [cyan]Saved to[/] `{file_path.as_posix()}`")


def fetch_pokemon_data(
    pokemon_id: int | None, api_url: str, parallelize: bool
) -> PokemonData:
    # Create a progress observer
    progress_observer = RichProgressObserver(description="Ingesting...")

    # Create a service instance
    pokeapi = PokeApiService(url=api_url)

    # Register the observer
    pokeapi.register_observer(progress_observer)

    match pokemon_id:
        case NoneType():
            # Run the service method within the context of the progress observer
            with progress_observer:
                if parallelize:
                    return pokeapi.get_all_parallel(batch_size=20)
                else:
                    return pokeapi.get_all(batch_size=600)
        case int():
            return pokeapi.get_pokemon_by_id(PokemonId(pokemon_id))


def main(
    pokemon_id: int | None = None,
    output_dir: Path | None = None,
    parallelize: bool = True,
) -> None:
    pokemon_data = fetch_pokemon_data(
        pokemon_id,
        api_url=os.environ["POKEAPI_V2_POKEMON_URL"],
        parallelize=parallelize,
    )

    print("\n[bold]🎉 Data ingested[/]\n")

    save_to = Path("output") if output_dir is None else output_dir
    save_to_json_file(pokemon_data, output_dir=save_to)
