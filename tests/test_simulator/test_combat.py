from typing import List

from dnd.models.armor import Armor, ArmorType
from dnd.models.character import Character, CharacterCategory
from dnd.models.damage import Damage, DamageType
from dnd.models.weapon import Weapon, WeaponType
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


def test_won_combat_with_two_characters():
    player = Character(strength=10, dexterity=10, constitution=10, intelligence=10, wisdom=10, charisma=10,
                       hit_points=10, category=CharacterCategory.PLAYABLE)
    player.active_weapon = DUMMY_PLAYER_WEAPON
    enemy = Character(strength=10, dexterity=10, constitution=10, intelligence=10, wisdom=10, charisma=10, hit_points=2,
                      category=CharacterCategory.NON_PLAYABLE)
    enemy.active_weapon = DUMMY_ENEMY_WEAPON

    combat = Combat(players=[player], enemies=[enemy], lose_checker=dummy_lose_checker, die=MockingDie(15))
    assert combat.initiate_combat() == Combat.Result.WIN


def test_lost_combat_with_two_characters():
    player = Character(strength=10, dexterity=10, constitution=10, intelligence=10, wisdom=10, charisma=10,
                       hit_points=1, category=CharacterCategory.PLAYABLE)
    player.active_weapon = DUMMY_PLAYER_WEAPON
    enemy = Character(strength=10, dexterity=10, constitution=10, intelligence=10, wisdom=10, charisma=10,
                      hit_points=20,
                      category=CharacterCategory.NON_PLAYABLE)
    enemy.active_weapon = DUMMY_ENEMY_WEAPON

    combat = Combat(players=[player], enemies=[enemy], lose_checker=dummy_lose_checker, die=MockingDie(15))
    assert combat.initiate_combat() == Combat.Result.LOSE


def test_won_combat_several_players_one_enemy():
    player1 = Character(strength=15, dexterity=10, constitution=14, intelligence=10, wisdom=10, charisma=10,
                        hit_points=20, category=CharacterCategory.PLAYABLE)
    player2 = Character(strength=15, dexterity=10, constitution=14, intelligence=10, wisdom=10, charisma=10,
                        hit_points=20, category=CharacterCategory.PLAYABLE)
    player3 = Character(strength=15, dexterity=10, constitution=14, intelligence=10, wisdom=10, charisma=10,
                        hit_points=20, category=CharacterCategory.PLAYABLE)
    player1.active_weapon = DUMMY_PLAYER_WEAPON
    player2.active_weapon = DUMMY_PLAYER_WEAPON
    player3.active_weapon = DUMMY_PLAYER_WEAPON

    enemy = Character(strength=18, dexterity=10, constitution=16, intelligence=10, wisdom=10, charisma=10,
                      hit_points=30, category=CharacterCategory.NON_PLAYABLE)
    enemy.active_weapon = DUMMY_ENEMY_WEAPON

    combat = Combat(players=[player1, player2, player3], enemies=[enemy], lose_checker=dummy_lose_checker,
                    die=MockingDie(10))

    assert combat.initiate_combat() == Combat.Result.WIN


def test_lost_combat_several_players_one_enemy():
    player1 = Character(strength=15, dexterity=10, constitution=14, intelligence=10, wisdom=10, charisma=10,
                        hit_points=20, category=CharacterCategory.PLAYABLE)
    player2 = Character(strength=15, dexterity=10, constitution=14, intelligence=10, wisdom=10, charisma=10,
                        hit_points=20, category=CharacterCategory.PLAYABLE)
    player3 = Character(strength=15, dexterity=10, constitution=14, intelligence=10, wisdom=10, charisma=10,
                        hit_points=20, category=CharacterCategory.PLAYABLE)
    player1.active_weapon = DUMMY_PLAYER_WEAPON
    player2.active_weapon = DUMMY_PLAYER_WEAPON
    player3.active_weapon = DUMMY_PLAYER_WEAPON

    enemy = Character(strength=18, dexterity=10, constitution=16, intelligence=10, wisdom=10, charisma=10,
                      hit_points=90, category=CharacterCategory.NON_PLAYABLE)
    enemy.active_weapon = Weapon(damage=Damage([MockingDie(10)], DamageType.PIERCING),
                                 weapon_type=WeaponType.MARTIAL_MELEE)

    combat = Combat(players=[player1, player2, player3], enemies=[enemy], lose_checker=dummy_lose_checker,
                    die=MockingDie(10))

    assert combat.initiate_combat() == Combat.Result.LOSE
