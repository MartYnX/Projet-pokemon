"""
Schema
"""
from datetime import date
from typing import  List, Optional, Union
from pydantic import BaseModel

#
#  ITEM
#
class ItemBase(BaseModel):
    """
    objet
    """
    name: str
    description: Union[str, None] = None

class ItemCreate(ItemBase):
    """
    objet
    """

class Item(ItemBase):
    """
    objet
    """
    id: int
    trainer_id: int

    class Config:
        from_attributes = True

#
#  POKEMON
#
class PokemonBase(BaseModel):
    """
    pokemon
    """
    api_id: int
    custom_name: Optional[str] = None

class PokemonCreate(PokemonBase):
    """
    pokemon
    """

class Pokemon(PokemonBase):
    """
    pokemon
    """
    id: int
    name: str
    trainer_id: int

    class Config:
        from_attributes = True
#
#  TRAINER
#
class TrainerBase(BaseModel):
    """
    entraineur
    """
    name: str
    birthdate: date

class TrainerCreate(TrainerBase):
    """
    entraineur
    """

class Trainer(TrainerBase):
    """
    entraineur
    """
    id: int
    inventory: List[Item] = []
    pokemons: List[Pokemon] = []

    class Config:
        from_attributes = True
