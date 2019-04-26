import json
from pathlib import Path
from typing import List, Dict, Tuple, Union

from dnd.models.armor import Armor, ArmorType
from dnd.models.character import Character, CharacterCategory
from dnd.models.damage import DamageType
from dnd.models.die import Die, DICE
from dnd.models.weapon import WeaponType, Weapon


class MalformedWeaponProperties(BaseException):
    pass


INVENTORY_PATH: Path = Path('inventory')


def create_weapon_from_json_file(json_file_path: Path) -> Weapon:
    with open(json_file_path.as_posix()) as json_file:
        json_dict = json.load(json_file)

    return create_weapon_from_dictionary(json_dict)


def create_weapon_from_dictionary(json_dict: Dict) -> Weapon:
    die_list = get_die_list(json_dict["die_list"])
    damage_type: DamageType = DamageType(json_dict['damage_type'])
    weapon_type: WeaponType = WeaponType(json_dict['weapon_type'])
    properties = get_properties_from_dictionary(json_dict)
    return Weapon.create_weapon(weapon_type=weapon_type, die_list=die_list,
                                damage_type=damage_type, **properties)


def create_armor_from_json_file(json_file_path: Path) -> Armor:
    with open(json_file_path.as_posix()) as json_file:
        json_dict = json.load(json_file)

    return create_armor_from_dictionary(json_dict)


def create_armor_from_dictionary(json_dict: Dict) -> Armor:
    return Armor(armor_class=json_dict['armor_class'],
                 armor_type=ArmorType(json_dict['armor_type']))


def create_character_from_json(json_file_path: Path) -> Character:
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


def create_character_from_dictionary(json_dict: Dict) -> Character:
    name: str = ''
    if 'name' in json_dict:
        name = json_dict['name']
    category: CharacterCategory = CharacterCategory.INDIFFERENT
    if 'category' in json_dict:
        category = CharacterCategory(json_dict['category'])
    parameters = {
        'hit_points': json_dict['hit_points'],
        'category': category,
        'name': name,
        **json_dict['abilities']
    }
    return Character(**parameters)


def load_armor_by_name(armor_name: str):
    return create_armor_from_json_file(INVENTORY_PATH.joinpath('armors', f"{armor_name.replace(' ', '_')}.json"))


def load_weapon_by_name(weapon_name: str):
    return create_weapon_from_json_file(INVENTORY_PATH.joinpath('weapons', f"{weapon_name.replace(' ', '_')}.json"))


def load_party_from_folder(folder_path: Path) -> List[Character]:
    character_list: List[Character] = []
    for file in folder_path.iterdir():
        character_list.append(create_character_from_json(file))
    return character_list


def get_die_list(string_list: List[str]) -> List[Die]:
    local_die_list: List[Die] = []
    for local_die in string_list:
        local_die_list.append(DICE[local_die])
    return local_die_list


def get_properties_from_dictionary(json_dict):
    properties: Dict[str, Union[bool, Tuple[int, int], List[Die]]] = {}
    for property_name, property_value in json_dict['properties'].items():
        if isinstance(property_value, bool):
            properties[property_name] = property_value
        elif isinstance(property_value, list):
            if isinstance(property_value[0], int):
                properties[property_name] = (property_value[0], property_value[1])
            elif isinstance(property_value[0], str):
                properties[property_name] = get_die_list(property_value)
            else:
                raise MalformedWeaponProperties(
                    f"Wrong property list: {property_name} is list of {type(property_value[0])}")
        else:
            raise MalformedWeaponProperties(f"Wrong property type: {property_name} is {type(property_value)}")
            # property_type = JsonValueType(property_value['type'])
        #
        # if property_type == JsonValueType.BOOL:
        #     properties[property_name] = property_value['value']
        # if property_type == JsonValueType.TUPLE:
        #     properties[property_name] = (property_value['value'][0], property_value['value'][1])
        # if property_type == JsonValueType.DIE_LIST:
        #     properties[property_name] = get_die_list(property_value['value'])
    return properties
