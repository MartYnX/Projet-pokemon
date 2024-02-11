"""
pokeapi
"""
import random
import requests

BASE_URL = "https://pokeapi.co/api/v2"


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
    return requests.get(f"{BASE_URL}/pokemon/{api_id}", timeout=10).json()


def battle_pokemon(first_api_id, second_api_id):
    """
        Do battle between 2 pokemons
    """
    first_pokemon_name = get_pokemon_name(first_api_id)
    second_pokemon_name = get_pokemon_name(second_api_id)
    premier_pokemon = get_pokemon_stats(first_api_id)
    second_pokemon = get_pokemon_stats(second_api_id)
    
    battle_result = battle_compare_stats(premier_pokemon, second_pokemon)
    if battle_result == 'first':
        return {"response": "le pokemon "+ first_pokemon_name + " a gagné le combat son id est le " + str(first_api_id) +". "}
    if battle_result == 'second':
        return {"response": "le pokemon "+ second_pokemon_name + " a gagné le combat son id est le " + str(second_api_id) +". "}
    if battle_result == 'equal':
        return {"response": "il y' a eu égalité"}
    
    return {"response":" pas de resultat"}
        
        


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
            if pokemon_first['base_stat'] < pokemon_second['base_stat']:
                second_result += 1
    
    if first_result > second_result:
        return 'first'
    if first_result < second_result:
        return 'second'
    
    return 'equal'
        
    

def get_three_pokemon():
    random_numbers = [random.randint(0, 100) for _ in range(3)]
    data = []
    for identifier in random_numbers:
       name = get_pokemon_name(identifier)
       stats = get_pokemon_stats(identifier)
       
       data.append({name: name, stats: stats})
       
    return data
        
