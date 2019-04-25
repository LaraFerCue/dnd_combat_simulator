from dnd.models.damage import DamageType
from dnd.models.weapon import Weapon
from tests.mocking_models.mocking_die import MockingDie

DUMMY_CHARACTER = {'strength': 10, 'dexterity': 10, 'constitution': 10, 'intelligence': 10, 'wisdom': 10,
                   'charisma': 10,
                   'hit_points': 10}
DUMMY_PLAYER_WEAPON = Weapon.simple_melee(die_list=[MockingDie(4)], damage_type=DamageType.PIERCING)
DUMMY_ENEMY_WEAPON = Weapon.simple_melee(die_list=[MockingDie(1)], damage_type=DamageType.PIERCING)
