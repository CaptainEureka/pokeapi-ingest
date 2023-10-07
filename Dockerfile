FROM python:3.12 AS build

# RUN apt update -y && apt upgrade -y

RUN pip install poetry

# Prepare working directory
WORKDIR /app

COPY pyproject.toml poetry.lock /app/

# Install dependencies
RUN poetry install --no-ansi --no-interaction --all-extras

COPY . /app

# Build the CLI
RUN poetry build -n -vv --format=wheel

FROM python:3.12 AS run

# Copy the package from the build stage
COPY --from=build /app/dist/*.whl /app/

# Install your package using pipx
RUN pip install --user /app/pokeapi_ingest-0.1.0-py3-none-any.whl

# Update PATH to include pipx binaries
ENV PATH="/root/.local/bin:$PATH"

ENTRYPOINT ["stockpile"]
