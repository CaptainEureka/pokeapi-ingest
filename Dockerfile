ARG PYTHON_VERSION=3.12
ARG POETRY_VERSION=1.6.1
FROM python:$PYTHON_VERSION AS build
ARG PYTHON_VERSION
ARG POETRY_VERSION

RUN pip install poetry==$POETRY_VERSION

# Prepare working directory
WORKDIR /app

COPY pyproject.toml poetry.lock /app/

# Install dependencies
RUN poetry install --no-ansi --no-interaction --all-extras \
	--without=dev,tools

COPY . /app

# Build the CLI
RUN poetry build -n -vv --format=wheel

FROM python:$PYTHON_VERSION-slim-bullseye AS run

# Copy the package from the build stage
COPY --from=build /app/dist/*.whl /app/

# Install your package using pipx
RUN pip install --user /app/pokeapi_ingest-0.1.0-py3-none-any.whl

# Update PATH to include pip binaries
ENV PATH="/root/.local/bin:$PATH"

ENTRYPOINT ["stockpile"]
