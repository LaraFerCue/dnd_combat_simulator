from pathlib import Path

import pytest

from dnd.models.armor import Armor, ArmorType
from dnd.models.character import Character, CharacterCategory
from dnd.models.damage import Damage, DamageType
from dnd.models.die import D6, D8, D10
from dnd.models.feat import Resistance, Vulnerability
from dnd.models.spell import Spell
from dnd.models.weapon import Weapon, WeaponType, WeaponProperty
from dnd.utils import file_utils
from dnd.utils.file_utils import create_weapon_from_json_file, load_weapon_by_name, create_armor_from_json_file, \
    load_armor_by_name, create_character_from_json_file, load_party_from_folder, create_spell_from_json_file, \
    load_spell_by_name
from tests.mocking_models.dummies import DUMMY_CHARACTER

file_utils.INVENTORY_PATH = Path('tests').joinpath('resources')


def test_create_weapon_from_json_file():
    weapon = create_weapon_from_json_file(Path('tests').joinpath('resources', 'weapons', 'weapon.json'))

    assert weapon == Weapon(damage=Damage([D6], DamageType.PIERCING), weapon_type=WeaponType.SIMPLE_MELEE,
                            properties={WeaponProperty.FINESSE: True, WeaponProperty.THROWN: (20, 60),
                                        WeaponProperty.VERSATILE: Damage([D8], DamageType.PIERCING)})


def test_create_armor_from_json_file():
    armor = create_armor_from_json_file(Path('tests').joinpath('resources', 'armors', 'armor.json'))

    assert armor == Armor(armor_class=13, armor_type=ArmorType.LIGHT)


def test_create_spell_from_json_file():
    spell = create_spell_from_json_file(Path('tests').joinpath('resources', 'spells', 'spell1.json'))

    assert spell == Spell(damage=Damage([D10], DamageType.MAGIC_COLD), spell_lvl=0)


def test_load_spell_by_name():
    assert load_spell_by_name('spell1') == Spell(damage=Damage([D10], DamageType.MAGIC_COLD), spell_lvl=0)

    with pytest.raises(OSError):
        load_spell_by_name('no_spell')


def test_load_armor_by_name():
    armor = load_armor_by_name('armor')

    assert armor == Armor(armor_class=13, armor_type=ArmorType.LIGHT)

    with pytest.raises(OSError):
        load_armor_by_name('no_armor')


def test_load_weapon_by_name():
    weapon = load_weapon_by_name('weapon')
    assert weapon == create_weapon_from_json_file(Path('tests').joinpath('resources', 'weapons', 'weapon.json'))

    with pytest.raises(OSError):
        load_weapon_by_name('no_weapon')


def test_create_character_from_json_file():
    named_character = create_character_from_json_file(
        Path('tests').joinpath('resources', 'characters', 'character_named_items.json'))
    json_character = create_character_from_json_file(
        Path('tests').joinpath('resources', 'characters', 'character_json_items.json'))

    result = Character(**DUMMY_CHARACTER, name='player 1', category=CharacterCategory.PLAYABLE)
    result.active_weapon = load_weapon_by_name('weapon')
    result.armor = load_armor_by_name('armor')

    assert named_character == result
    assert json_character == result


def test_load_character_with_spells():
    loaded_character = create_character_from_json_file(
        Path('tests').joinpath('resources', 'characters', 'character_with_spells.json'))
    character = Character(**DUMMY_CHARACTER, name='player 1', category=CharacterCategory.PLAYABLE)
    spell1 = load_spell_by_name('spell1')
    spell2 = load_spell_by_name('spell2')
    spell3 = load_spell_by_name('spell3')

    spell1.slots = 0
    spell2.slots = 2
    spell3.slots = 1

    character.spell_list = [spell1, spell2, spell3]

    assert loaded_character == character


def test_load_character_with_feats():
    loaded_character = create_character_from_json_file(
        Path('tests').joinpath('resources', 'characters', 'character_with_feats.json'))
    character = Character(**DUMMY_CHARACTER, name='player 1', category=CharacterCategory.PLAYABLE)
    character.feat_list = [
        Resistance(DamageType.PIERCING),
        Vulnerability(DamageType.FIRE)
    ]

    assert loaded_character == character


def test_load_party_from_folder():
    player1 = create_character_from_json_file(Path('tests').joinpath('resources', 'party', 'player1.json'))
    player2 = create_character_from_json_file(Path('tests').joinpath('resources', 'party', 'player2.json'))
    player3 = create_character_from_json_file(Path('tests').joinpath('resources', 'party', 'player3.json'))

    assert set(load_party_from_folder(Path('tests').joinpath('resources', 'party'))) == {player1, player2, player3}


def test_load_party_from_non_existent_folder():
    with pytest.raises(OSError):
        load_party_from_folder(Path('tests').joinpath('resources', 'stupid_folder'))
