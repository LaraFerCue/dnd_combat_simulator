from typing import List

from dnd.models.armor import Armor, ArmorType
from dnd.models.character import Character, CharacterCategory
from dnd.simulator.combat import Combat
from tests.mocking_models.dummies import DUMMY_PLAYER_WEAPON, DUMMY_ENEMY_WEAPON, DUMMY_CHARACTER
from tests.mocking_models.mocking_die import MockingDie


def dummy_lose_checker(characters: List[Character]) -> bool:
    for character in characters:
        if character.hit_points <= 0:
            return True
    return False


def test_get_player_target_single_player():
    player1 = Character.new(**DUMMY_CHARACTER)
    player1.armor = Armor(11, ArmorType.LIGHT)

    combat = Combat(players=[player1], enemies=[], lose_checker=dummy_lose_checker)
    assert combat.get_player_target() == player1


def test_get_player_target_multiple_player():
    player1 = Character.new(**DUMMY_CHARACTER)
    player2 = Character.new(**DUMMY_CHARACTER)
    player1.armor = Armor(11, ArmorType.LIGHT)
    player2.armor = Armor(14, ArmorType.LIGHT)

    combat = Combat(players=[player1, player2], enemies=[], lose_checker=dummy_lose_checker)
    assert combat.get_player_target() == player2


def test_get_enemy_target_single_enemy():
    enemy1 = Character.new(**DUMMY_CHARACTER)
    enemy1.armor = Armor(11, ArmorType.LIGHT)

    combat = Combat(enemies=[enemy1], players=[], lose_checker=dummy_lose_checker)
    assert combat.get_enemy_target() == enemy1


def test_get_enemy_target_multiple_enemies():
    enemy1 = Character.new(**DUMMY_CHARACTER)
    enemy2 = Character.new(**DUMMY_CHARACTER)
    enemy1.armor = Armor(11, ArmorType.LIGHT)
    enemy2.armor = Armor(14, ArmorType.LIGHT)

    combat = Combat(enemies=[enemy1, enemy2], players=[], lose_checker=dummy_lose_checker)
    assert combat.get_enemy_target() == enemy1


def test_combat_with_two_characters():
    player = Character(strength=10, dexterity=10, constitution=10, intelligence=10, wisdom=10, charisma=10,
                       hit_points=10, category=CharacterCategory.PLAYABLE)
    player.active_weapon = DUMMY_PLAYER_WEAPON
    enemy = Character(strength=10, dexterity=10, constitution=10, intelligence=10, wisdom=10, charisma=10, hit_points=2,
                      category=CharacterCategory.NON_PLAYABLE)
    enemy.active_weapon = DUMMY_ENEMY_WEAPON

    combat = Combat(players=[player], enemies=[enemy], lose_checker=dummy_lose_checker, die=MockingDie(15))
    assert combat.initiate_combat() == Combat.Result.WIN
