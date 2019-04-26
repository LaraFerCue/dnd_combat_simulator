from typing import Dict, List, Union, Tuple

from dnd.models.armor import Armor, ArmorType
from dnd.models.character import Character, CharacterCategory
from dnd.models.damage import DamageType, Damage
from dnd.models.die import Die, DICE
from dnd.models.spell import Spell
from dnd.models.weapon import Weapon, WeaponType


def create_weapon_from_dictionary(json_dict: Dict) -> Weapon:
    die_list = get_die_list(json_dict["die_list"])
    damage_type: DamageType = DamageType(json_dict['damage_type'])
    weapon_type: WeaponType = WeaponType(json_dict['weapon_type'])
    properties = get_properties_from_dictionary(json_dict)
    return Weapon.create_weapon(weapon_type=weapon_type, die_list=die_list,
                                damage_type=damage_type, **properties)


def create_armor_from_dictionary(json_dict: Dict) -> Armor:
    return Armor(armor_class=json_dict['armor_class'],
                 armor_type=ArmorType(json_dict['armor_type']))


def create_spell_from_dictionary(json_dict: Dict) -> Spell:
    die_list = get_die_list(json_dict['die_list'])
    damage_type: DamageType = DamageType(json_dict['damage_type'])
    spell_level: int = int(json_dict['level'])
    return Spell(damage=Damage(dice_list=die_list, damage_type=damage_type), spell_lvl=spell_level)


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
    return properties


class MalformedWeaponProperties(BaseException):
    pass
