# test_actions.py
import datetime
from unittest.mock import patch
import pytest
from sqlalchemy.orm import Session
from app.actions import get_trainer, get_trainer_by_name, get_trainers, create_trainer, add_trainer_item, add_trainer_pokemon, get_items, get_pokemon, get_pokemons
from app.models import Trainer, Item, Pokemon
from app.sqlite import Base, engine, SessionLocal
from app.schemas import PokemonCreate, TrainerCreate, ItemCreate, TrainerCreate

@pytest.fixture(scope="module")
def databases():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    yield db
    db.close()
def test_clear_trainers(database: Session):
    # Supprime toutes les données de la table trainers
    database.query(Trainer).delete()
    database.query(Pokemon).delete()
    database.query(Item).delete()
    database.commit()

    # Vérifiez que la table est vide
    assert database.query(Trainer).count() == 0
    assert database.query(Pokemon).count() == 0
    assert database.query(Item).count() == 0
def test_get_pokemons(database: Session):
    # Créer quelques Pokémon fictifs dans la base de données
    pokemons = [
        Pokemon(name="Pikachu", trainer_id=1),
        Pokemon(name="Charmander", trainer_id=2),
        Pokemon(name="Squirtle", trainer_id=3)
    ]
    database.add_all(pokemons)
    database.commit()

    try:
        # Appeler la fonction pour récupérer tous les pokémons
        retrieved_pokemons = get_pokemons(database)

        # Vérifier si les pokémons ont été récupérés avec succès
        assert len(retrieved_pokemons) == len(pokemons)
        assert all(pokemon.name in [p.name for p in retrieved_pokemons] for pokemon in pokemons)
    finally:
        # Supprimer les données ajoutées de la base de données
        for pokemon in pokemons:
            database.delete(pokemon)
        database.commit()

def test_get_pokemon(database: Session):
    # Créer un Pokémon fictif dans la base de données
    pokemon = Pokemon(name="Pikachu", trainer_id=1)
    database.add(pokemon)
    database.commit()
    try:
        # Appeler la fonction pour récupérer le Pokémon par son ID
        retrieved_pokemon = get_pokemon(database, pokemon.id)

        # Vérifier si le Pokémon a été récupéré avec succès
        assert retrieved_pokemon is not None
        assert retrieved_pokemon.name == "Pikachu"
        assert retrieved_pokemon.trainer_id == 1
    finally:
        # Supprimer les données ajoutées de la base de données
        database.delete(pokemon)
        database.commit()

def test_get_items(database: Session):
    # Ajouter des items fictifs dans la base de données pour les besoins du test
    items = [
        Item(name="Potion"),
        Item(name="Revive"),
        Item(name="Great Ball")
    ]
    database.add_all(items)
    database.commit()

    try:
        # Appeler la fonction pour récupérer les items
        retrieved_items = get_items(database)

        # Vérifier si les items ont été récupérés avec succès
        assert len(retrieved_items) == 3
        assert retrieved_items[0].name == "Potion"
        assert retrieved_items[1].name == "Revive"
        assert retrieved_items[2].name == "Great Ball"
    finally:
        # Supprimer les données ajoutées de la base de données
        for item in items:
            database.delete(item)
        database.commit()

def test_add_trainer_pokemon(database: Session):
    # Créer un entraîneur fictif dans la base de données
    trainer = Trainer(name="John Doe", birthdate=datetime.date(1990, 1, 1))
    database.add(trainer)
    database.commit()
    # Données pour créer un nouveau Pokémon
    pokemon_data = PokemonCreate(api_id=25, custom_name="Pikachu")  # Ajouter le niveau
    # Définir le comportement du mock pour get_pokemon_name
    with patch("app.actions.get_pokemon_name") as mock_get_pokemon_name:
        mock_get_pokemon_name.return_value = "Pikachu"

        # Appeler la fonction pour ajouter le Pokémon à l'entraîneur
        new_pokemon = add_trainer_pokemon(database, pokemon_data, trainer.id)

        # Vérifier si le mock a été appelé avec le bon API ID
        mock_get_pokemon_name.assert_called_once_with(25)
    # Vérifier si le Pokémon a été correctement créé et lié à l'entraîneur
    assert new_pokemon is not None
    assert new_pokemon.name == "Pikachu"
    # assert new_pokemon.level == 50  # Vérifier le niveau
    assert new_pokemon.trainer_id == trainer.id

    # Supprimer les données ajoutées
    database.delete(new_pokemon)
    database.delete(trainer)
    database.commit()

def test_create_trainer(database: Session):
    # Données pour créer un nouvel entraîneur
    new_trainer_data = TrainerCreate(name="John Doe", birthdate=datetime.date(1990, 1, 1))

    # Appeler la fonction pour créer un nouvel entraîneur
    new_trainer = create_trainer(database, new_trainer_data)

    # Vérifier si l'entraîneur a été correctement créé
    assert new_trainer is not None
    assert new_trainer.name == "John Doe"
    assert new_trainer.birthdate == datetime.date(1990, 1, 1)

    # Vérifier si l'entraîneur a été correctement enregistré dans la base de données
    db_trainer = database.query(Trainer).filter(Trainer.id == new_trainer.id).first()
    assert db_trainer is not None
    assert db_trainer.name == "John Doe"
    assert db_trainer.birthdate == datetime.date(1990, 1, 1)

    # Supprimer l'entraîneur de la base de données
    database.delete(new_trainer)
    database.commit()

# Test de la fonction add_trainer_item
def test_add_trainer_item(database: Session):
    # Créer un entraîneur fictif dans la base de données
    trainer = Trainer(name="John Doe", birthdate=datetime.date(1990, 1, 1))
    database.add(trainer)
    database.commit()
    # Données pour créer un nouvel item
    item_data = ItemCreate(name="Potion", description="Restores HP by 20")
    # Appeler la fonction pour ajouter l'item à l'entraîneur
    new_item = add_trainer_item(database, item_data, trainer.id)
    # Vérifier si l'item a été correctement créé et lié à l'entraîneur
    assert new_item is not None
    assert new_item.name == "Potion"
    assert new_item.description == "Restores HP by 20"
    assert new_item.trainer_id == trainer.id
    # Rafraîchir l'entraîneur depuis la base de données pour obtenir les items mis à jour
    database.refresh(trainer)
    # Accéder directement aux items depuis la base de données et vérifier la longueur
    items_count = database.query(Item).filter(Item.trainer_id == trainer.id).count()
    assert items_count == 1
    # Nettoyage après le test
    database.delete(trainer)
    database.delete(new_item)
    database.commit()

def test_get_trainer(database: Session):
    # Créez un entraîneur fictif dans la base de données pour les besoins du test
    fake_trainer = Trainer(name="Eric Gansa", birthdate=datetime.date(1990, 1, 1))
    database.add(fake_trainer)
    database.commit()
    # Appelez la fonction get_trainer pour récupérer l'entraîneur par son ID
    retrieved_trainer = get_trainer(database, fake_trainer.id)
    # Vérifiez si l'entraîneur récupéré correspond à l'entraîneur ajouté
    assert retrieved_trainer is not None
    assert retrieved_trainer.id == fake_trainer.id
    assert retrieved_trainer.name == fake_trainer.name
    assert retrieved_trainer.birthdate == fake_trainer.birthdate
    # Supprimez l'entraîneur fictif de la base de données
    database.delete(fake_trainer)
    database.commit()

def test_get_trainer_by_name(database: Session):
    # Créez deux entraîneurs fictifs dans la base de données pour les besoins du test
    trainer1 = Trainer(name="Eric Gansa", birthdate=datetime.date(1990, 1, 1))
    trainer2 = Trainer(name="Aboubacar", birthdate=datetime.date(1992, 5, 4))
    database.add(trainer1)
    database.add(trainer2)
    database.commit()
    # Appelez la fonction get_trainer_by_name pour récupérer les entraîneurs par leur nom
    retrieved_trainers = get_trainer_by_name(database, "Eric Gansa")
    # Vérifiez si les entraîneurs récupérés correspondent à l'entraîneur ajouté
    assert len(retrieved_trainers) == 1
    assert retrieved_trainers[0].name == "Eric Gansa"
    # Supprimez les entraîneurs fictifs de la base de données
    database.delete(trainer1)
    database.delete(trainer2)
    database.commit()


def test_get_trainers(database: Session):
    # Créez quelques entraîneurs fictifs dans la base de données pour les besoins du test
    trainers = [
        Trainer(name="Eric Gansa", birthdate=datetime.date(1990, 1, 1)),
        Trainer(name="Aboubacar", birthdate=datetime.date(1992, 5, 4)),
        Trainer(name="Brock", birthdate=datetime.date(1993, 8, 30))
    ]
    database.add_all(trainers)
    database.commit()
    # Appelez la fonction get_trainers pour récupérer tous les entraîneurs
    retrieved_trainers = get_trainers(database)
    # Vérifiez si la liste des entraîneurs récupérés correspond aux entraîneurs ajoutés
    assert len(retrieved_trainers) == len(trainers)  # Correction ici
    # Supprimez les entraîneurs fictifs de la base de données
    for trainer in trainers:
        database.delete(trainer)
    database.commit()
