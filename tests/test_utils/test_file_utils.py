from pathlib import Path

from dnd.models.damage import Damage, DamageType
from dnd.models.die import D6, D8
from dnd.models.weapon import Weapon, WeaponType, WeaponProperty
from dnd.utils.file_utils import create_weapon_from_json


def test_create_weapon_from_json_file():
    weapon = create_weapon_from_json(Path('tests').joinpath('resources', 'weapon.json'))

    assert weapon == Weapon(damage=Damage([D6], DamageType.PIERCING), weapon_type=WeaponType.SIMPLE_MELEE,
                            properties={WeaponProperty.FINESSE: True, WeaponProperty.THROWN: (20, 60),
                                        WeaponProperty.VERSATILE: Damage([D8], DamageType.PIERCING)})
