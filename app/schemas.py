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
    pass

class Item(ItemBase):
    """
    objet
    """
    id: int
    trainer_id: int

    class Config:
        """
        configuration objet
        """
        orm_mode = True

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
    pass

class Pokemon(PokemonBase):
    """
    pokemon
    """
    id: int
    name: str
    trainer_id: int

    class Config:
        """
        configuration pokemon
        """
        orm_mode = True
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
    pass

class Trainer(TrainerBase):
    """
    entraineur
    """
    id: int
    inventory: List[Item] = []
    pokemons: List[Pokemon] = []

    class Config:
        """
        configuration entraineur
        """
        orm_mode = True
