from typing import Iterator, List, NewType, Sequence

from pydantic import BaseModel, Field, HttpUrl

PokemonId = NewType("PokemonId", int)


class Type(BaseModel):
    name: str
    url: HttpUrl


class PokemonType(BaseModel):
    slot: int
    _type: Type


class Ability(BaseModel):
    name: str
    url: HttpUrl


class PokemonAbility(BaseModel):
    is_hidden: bool
    slot: int
    ability: Ability


class Pokemon(BaseModel):
    id: int = Field(..., alias="id")
    name: str
    types: Sequence[PokemonType]
    height: int
    weight: int
    base_experience: int | None
    abilities: Sequence[PokemonAbility]


class PokemonData(BaseModel):
    data: List[Pokemon] = []

    def to_iter(self) -> Iterator[Pokemon]:
        for pokemon in self.data:
            yield pokemon
