"""
pokeapi
"""
import requests

base_url = "https://pokeapi.co/api/v2"


def get_pokemon_name(api_id):
    """
        Get a pokemon name from the API pokeapi
    """
    return get_pokemon_data(api_id)['name']

def get_pokemon_stats(api_id):
    """
        Get pokemon stats from the API pokeapi
    """
    return get_pokemon_data(api_id)['stats']

def get_pokemon_data(api_id):
    """
        Get data of pokemon name from the API pokeapi
    """
    return requests.get(f"{base_url}/pokemon/{api_id}", timeout=10).json()


def battle_pokemon(first_api_id, second_api_id):
    """
        Do battle between 2 pokemons
    """
    premierPokemon = get_pokemon_data(first_api_id)
    secondPokemon = get_pokemon_data(second_api_id)
    battle_result = 0
    return premierPokemon if battle_result > 0 else secondPokemon if battle_result < 0 else {'winner': 'draw'}


def battle_compare_stats(first_pokemon_stats, second_pokemon_stats):
    """
        Compare given stat between two pokemons
    """
    first_result = 0
    second_result = 0
    
    for pokemon_first in first_pokemon_stats:
        for pokemon_second in second_pokemon_stats:
            if pokemon_first['base_stat'] > pokemon_second['base_stat']:
                first_result += 1
            elif pokemon_first['base_stat'] < pokemon_second['base_stat']:
                second_result += 1
    
    if first_result > second_result:
        return 'first'
    elif first_result < second_result:
        return 'second'
    else:
        return 'equal'
        
    
