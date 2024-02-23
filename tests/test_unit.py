# """
# _summary
# """
# from fastapi.testclient import TestClient
# # import pytest
# from ..main import app

# client = TestClient(app)

# def test_trainers_endpoint():
#     """
#     Vérifie l'existence d'un entraineur
#     """
#     response = client.get("/trainers")
#     assert response.status_code == 200
#     data = response.json()
#     assert len(data) > 0
#     assert all(isinstance(item, dict) for item in data)

# def test_items_endpoint():
#     """
#     Vérifie l'existence d'un objet
#     """
#     response = client.get("/items")
#     assert response.status_code == 200
#     data = response.json()
#     assert len(data) > 0
#     assert all(isinstance(item, dict) for item in data)

# def test_pokemons_endpoint():
#     """
#     Vérifie l'existence d'un pokemon
#     """
#     response = client.get("/pokemons")
#     assert response.status_code == 200
#     data = response.json()
#     assert len(data) > 0
#     assert all(isinstance(item, dict) for item in data)
