"""
fichier principale
"""

from fastapi import FastAPI
from app.routers import trainers, pokemons, items
from app.utils.pokeapi import get_pokemon_stats


app = FastAPI()


app.include_router(trainers.router,
                   prefix="/trainers")
app.include_router(items.router,
                   prefix="/items")
app.include_router(pokemons.router,
                   prefix="/pokemons")
