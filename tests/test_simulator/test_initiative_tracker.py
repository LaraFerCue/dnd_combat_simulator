from dnd.models.character import Character
from dnd.simulator.initiative_tracker import Initiative, InitiativeTracker
from tests.mocking_models.dummies import DUMMY_CHARACTER
from tests.mocking_models.mocking_die import MockingDie


def test_initiative_one_character():
    character1 = Character.new(**DUMMY_CHARACTER)
    initiative = Initiative()

    initiative.add(character1)
    assert initiative.get_next() == character1
    assert set(initiative.get_characters()) == {character1}


def test_initiative_two_characters():
    character1 = Character.new(**DUMMY_CHARACTER)
    character2 = Character(11, 11, 11, 10, 10, 10, 10)
    initiative = Initiative()

    initiative.add(character1)
    initiative.add(character2)
    assert initiative.get_next() == character1
    assert initiative.get_next() == character2
    assert initiative.get_next() is None
    assert initiative.get_next() == character1
    assert set(initiative.get_characters()) == {character1, character2}


def test_initiative_tracker_one_player_one_monster():
    character1 = Character.new(**DUMMY_CHARACTER)
    enemy = Character(10, 8, 9, 10, 8, 9, 10)

    initiative_tracker = InitiativeTracker([character1], [enemy], MockingDie(3))
    assert initiative_tracker.get_next_character() == character1
    assert initiative_tracker.get_next_character() == enemy
    assert initiative_tracker.get_next_character() is None
    assert initiative_tracker.get_next_character() == character1
    assert initiative_tracker.get_next_character() == enemy
