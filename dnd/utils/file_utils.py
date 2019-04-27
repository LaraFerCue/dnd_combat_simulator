import json
from pathlib import Path
from typing import List

from dnd.models.armor import Armor
from dnd.models.character import Character, Ability
from dnd.models.spell import Spell
from dnd.models.weapon import Weapon
from dnd.utils.parsers import create_weapon_from_dictionary, create_armor_from_dictionary, \
    create_character_from_dictionary, create_spell_from_dictionary, get_feat_list

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
    if 'spells' in json_dict:
        for spell_name, spell_slots in json_dict['spells'].items():
            spell = load_spell_by_name(spell_name)
            spell.slots = spell_slots
            character.spell_list.append(spell)
    if 'feats' in json_dict:
        character.feat_list = get_feat_list(json_dict['feats'])
    if 'using_shield' in json_dict:
        character.using_shield = json_dict['using_shield']
    if 'cast_ability' in json_dict:
        character.cast_ability = Ability(json_dict['cast_ability'])
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
