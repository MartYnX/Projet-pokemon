"""
Fichier des informations des pokemons
"""
from typing import List
from sqlalchemy.orm import Session
from fastapi import APIRouter,  Depends
from app import actions, schemas
from app.utils.pokeapi import battle_pokemon, get_three_pokemon
from app.utils.utils import get_db

router = APIRouter()


@router.get("/{first_id}/{second_id}")
async def pokemon_fight(first_id: int,second_id: int):
    results = battle_pokemon(first_id,second_id)
    return results
    
@router.get("/", response_model=List[schemas.Pokemon])
def get_pokemons(skip: int = 0, limit: int = 100, database: Session = Depends(get_db)):
    """
        Return all pokemons
        Default limit is 100
    """
    pokemons = actions.get_pokemons(database, skip=skip, limit=limit)
    return pokemons

@router.get("/aleatoire")
def get_aleatoire():
    data = get_three_pokemon()
    return data