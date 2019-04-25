import json
from enum import Enum
from pathlib import Path
from typing import List, Dict, Tuple, Union

from dnd.models.damage import DamageType
from dnd.models.die import Die, DICE
from dnd.models.weapon import WeaponType, Weapon


class JsonValueType(Enum):
    BOOL = 'bool'
    TUPLE = 'Tuple'
    DIE_LIST = 'Die List'


INVENTORY_PATH: Path = Path('inventory')


def create_weapon_from_json(json_file_path: Path) -> Weapon:
    with open(json_file_path.as_posix()) as json_file:
        json_dict = json.load(json_file)

    die_list = get_die_list(json_dict["die_list"])
    damage_type: DamageType = DamageType(json_dict['damage_type'])
    weapon_type: WeaponType = WeaponType(json_dict['weapon_type'])

    properties = get_properties_from_dictionary(json_dict)
    return Weapon.create_weapon(weapon_type=weapon_type, die_list=die_list,
                                damage_type=damage_type, **properties)


def load_weapon_by_name(weapon_name: str):
    return create_weapon_from_json(INVENTORY_PATH.joinpath('weapons', f"{weapon_name}.json"))


def get_die_list(string_list: List[str]) -> List[Die]:
    local_die_list: List[Die] = []
    for local_die in string_list:
        local_die_list.append(DICE[local_die])
    return local_die_list


def get_properties_from_dictionary(json_dict):
    properties: Dict[str, Union[bool, Tuple[int, int], List[Die]]] = {}
    for property_name, property_value in json_dict['properties'].items():
        property_type = JsonValueType(property_value['type'])

        if property_type == JsonValueType.BOOL:
            properties[property_name] = property_value['value']
        if property_type == JsonValueType.TUPLE:
            properties[property_name] = (property_value['value'][0], property_value['value'][1])
        if property_type == JsonValueType.DIE_LIST:
            properties[property_name] = get_die_list(property_value['value'])
    return properties
