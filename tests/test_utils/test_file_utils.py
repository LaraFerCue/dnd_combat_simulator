from pathlib import Path

import pytest

from dnd.models.armor import Armor, ArmorType
from dnd.models.damage import Damage, DamageType
from dnd.models.die import D6, D8
from dnd.models.weapon import Weapon, WeaponType, WeaponProperty
from dnd.utils import file_utils
from dnd.utils.file_utils import create_weapon_from_json, load_weapon_by_name, create_armor_from_json, \
    load_armor_by_name

file_utils.INVENTORY_PATH = Path('tests').joinpath('resources')


def test_create_weapon_from_json_file():
    weapon = create_weapon_from_json(Path('tests').joinpath('resources', 'weapons', 'weapon.json'))

    assert weapon == Weapon(damage=Damage([D6], DamageType.PIERCING), weapon_type=WeaponType.SIMPLE_MELEE,
                            properties={WeaponProperty.FINESSE: True, WeaponProperty.THROWN: (20, 60),
                                        WeaponProperty.VERSATILE: Damage([D8], DamageType.PIERCING)})


def test_create_armor_from_json_file():
    armor = create_armor_from_json(Path('tests').joinpath('resources', 'armors', 'armor.json'))

    assert armor == Armor(armor_class=13, armor_type=ArmorType.LIGHT)


def test_load_armor_by_name():
    armor = load_armor_by_name('armor')

    assert armor == Armor(armor_class=13, armor_type=ArmorType.LIGHT)

    with pytest.raises(OSError):
        load_armor_by_name('no_armor')


def test_load_weapon_by_name():
    weapon = load_weapon_by_name('weapon')
    assert weapon == create_weapon_from_json(Path('tests').joinpath('resources', 'weapons', 'weapon.json'))

    with pytest.raises(OSError):
        load_weapon_by_name('no_weapon')
