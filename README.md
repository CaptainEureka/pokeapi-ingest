# PokeAPI Ingest

* [🌄 Overview](#Overview)
* [🛠️ Prerequisites](#Prerequisites)
* [⚙️ Setup](#Setup)
  * [🚀 Getting started](#Gettingstarted)
    * [Clone the repository](#Clonetherepository)
    * [📦 Installation](#Installation)
    * [👟 Running the `stockpile` CLI locally](#RunningthestockpileCLIlocally)
  * [🏗️ Build and Run the container](#BuildandRunthecontainer)
* [©️ License](#License)

## <a name='Overview'></a>🌄 Overview

`pokeapi-ingest` is a containerized CLI application designed for ingesting data from the [PokeAPI](https://pokeapi.co/docs/v2).
The project is implemented in Python and makes extensive use of Poetry, Docker, Docker Compose.

The primary entrypoint of the application is the `stockpile` CLI.

## <a name='Prerequisites'></a>🛠️ Prerequisites

* Python 3.12
* Docker
* Poetry
* Docker Compose
* _Optional_: [Devenv](https://devenv.sh)

## <a name='Setup'></a>⚙️ Setup

### <a name='Gettingstarted'></a>🚀 Getting started

#### <a name='Clonetherepository'></a>Clone the repository

```bash
git clone https://github.com/CaptainEureka/pokeapi-ingest.git
cd pokeapi-ingest
```

#### <a name='Installation'></a>📦 Installation

Install the package with `poetry`:

```bash
poetry install
```

#### <a name='RunningthestockpileCLIlocally'></a>👟 Running the `stockpile` CLI locally

Once installed the `stockpile` CLI should be available in your shells's `$PATH` you can check if this is the case by running:

```bash
stockpile --help
```

The main entrypoint to `stockpile` is the `ingest` subcomman. The `ingest` subcommand has two options. If passing the `--pokemon-id` argument `stockpile` will fetch **only** the Pokemon data from PokeAPI for that Pokemon ID otherwise it will fetch _all_ pokemon.

e.g.

```bash
stockpile ingest --pokemon-id 317
```

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./assets/stockpile-ingest-pokemon-id.gif">
  <source media="(prefers-color-scheme: light)" srcset="./assets/stockpile-ingest-pokemon-id.gif">
  <img width="600" alt="Example of running `stockpile` with pokemon id." src="./assets/stockpile-ingest-pokemon-id.gif">
</picture>

or

```bash
stockpile ingest
```

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./assets/stockpile-ingest-all.gif">
  <source media="(prefers-color-scheme: light)" srcset="./assets/stockpile-ingest-all.gif">
  <img width="600" alt="Example of running `stockpile` without pokemon id." src="./assets/stockpile-ingest-all.gif">
</picture>

### <a name='BuildandRunthecontainer'></a>🏗️ Build and Run the container

Build:
```bash
docker compose build
```

Run:
```bash
docker compose run -it --rm stockpile --help
```

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./assets/docker-build-n-run-app.gif">
  <source media="(prefers-color-scheme: light)" srcset="./assets/docker-build-n-run-app.gif">
  <img width="600" alt="Example of running `stockpile` inside a Docker container." src="./assets/docker-build-n-run-app.gif">
</picture>

## <a name='License'></a>©️ License

This project is licensed under the MIT License. See the LICENSE file for more details.