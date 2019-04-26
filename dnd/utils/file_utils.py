import json
from pathlib import Path
from typing import List

from dnd.models.armor import Armor
from dnd.models.character import Character
from dnd.models.spell import Spell
from dnd.models.weapon import Weapon
from dnd.utils.parsers import create_weapon_from_dictionary, create_armor_from_dictionary, \
    create_character_from_dictionary, create_spell_from_dictionary

INVENTORY_PATH: Path = Path('inventory')


def create_weapon_from_json_file(json_file_path: Path) -> Weapon:
    with open(json_file_path.as_posix()) as json_file:
        json_dict = json.load(json_file)

    return create_weapon_from_dictionary(json_dict)


def create_armor_from_json_file(json_file_path: Path) -> Armor:
    with open(json_file_path.as_posix()) as json_file:
        json_dict = json.load(json_file)

    return create_armor_from_dictionary(json_dict)


def create_spell_from_json_file(json_file_path: Path) -> Spell:
    with open(json_file_path.as_posix()) as json_file:
        json_dict = json.load(json_file)

    return create_spell_from_dictionary(json_dict)


def create_character_from_json_file(json_file_path: Path) -> Character:
    with open(json_file_path.as_posix()) as json_file:
        json_dict = json.load(json_file)
    character = create_character_from_dictionary(json_dict)

    if 'weapon' in json_dict:
        if isinstance(json_dict['weapon'], str):
            character.active_weapon = load_weapon_by_name(json_dict['weapon'])
        else:
            character.active_weapon = create_weapon_from_dictionary(json_dict['weapon'])

    if 'armor' in json_dict:
        if isinstance(json_dict['armor'], str):
            character.armor = load_armor_by_name(json_dict['armor'])
        else:
            character.armor = create_armor_from_dictionary(json_dict['armor'])
    return character


def load_armor_by_name(armor_name: str) -> Armor:
    return create_armor_from_json_file(INVENTORY_PATH.joinpath('armors', f"{armor_name.replace(' ', '_')}.json"))


def load_weapon_by_name(weapon_name: str) -> Weapon:
    return create_weapon_from_json_file(INVENTORY_PATH.joinpath('weapons', f"{weapon_name.replace(' ', '_')}.json"))


def load_spell_by_name(spell_name: str) -> Spell:
    return create_spell_from_json_file(INVENTORY_PATH.joinpath('spells', f"{spell_name.replace(' ', '_')}.json"))


def load_party_from_folder(folder_path: Path) -> List[Character]:
    character_list: List[Character] = []
    for file in folder_path.iterdir():
        character_list.append(create_character_from_json_file(file))
    return character_list
