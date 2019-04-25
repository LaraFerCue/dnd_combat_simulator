from enum import Enum
from typing import Union, Dict, Tuple

from dnd.models.damage import Damage


class WeaponType(Enum):
    SIMPLE_MELEE = "Simple Melee"
    SIMPLE_RANGED = "Simple Ranged"
    MARTIAL_MELEE = "Martial Melee"
    MARTIAL_RANGED = "Martial Ranged"


class WeaponProperty(Enum):
    AMMUNITION = "ammunition"
    FINESSE = "finesse"
    HEAVY = "heavy"
    LIGHT = "light"
    LOADING = "loading"
    RANGE = "range"
    REACH = "reach"
    SPECIAL = "special"
    THROWN = "thrown"
    TWO_HANDED = "two_handed"
    VERSATILE = "versatile"


class Weapon:
    def __init__(self, damage: Damage, weapon_type: WeaponType,
                 properties: Dict[WeaponProperty, Union[Tuple[int, int], bool, Damage]] = {}):
        self.__damage: Damage = damage
        self.__weapon_type = weapon_type
        self.__properties: Dict[WeaponProperty, Union[Tuple[int, int], bool, Damage]] = properties
        self.__ammo: int = 0

        if WeaponProperty.VERSATILE in properties and not isinstance(properties[WeaponProperty.VERSATILE], Damage):
            raise ValueError('Versatile needs a Damage value')

    @property
    def is_ranged(self) -> bool:
        return self.__weapon_type == WeaponType.SIMPLE_RANGED or self.__weapon_type == WeaponType.MARTIAL_RANGED

    @property
    def damage(self) -> Damage:
        return self.__damage

    @property
    def ammo(self):
        return self.__ammo

    @ammo.setter
    def ammo(self, value):
        if value < 0:
            raise AttributeError("Ammo cannot be negative")
        self.__ammo = value

    def get_damage(self, strength_mod: int, dexterity_mod: int, use_two_handed: bool = False):
        if self.__weapon_type in [WeaponType.SIMPLE_MELEE, WeaponType.MARTIAL_MELEE]:
            attack_mod = strength_mod
            if WeaponProperty.FINESSE in self.__properties:
                if dexterity_mod > strength_mod:
                    attack_mod = dexterity_mod
        else:
            if WeaponProperty.AMMUNITION in self.__properties and self.__ammo <= 0:
                return 0
            self.ammo -= 1
            attack_mod = dexterity_mod
        if WeaponProperty.VERSATILE in self.__properties and use_two_handed:
            return self.__properties[WeaponProperty.VERSATILE].get_damage() + attack_mod
        return self.__damage.get_damage() + attack_mod

    def check_property(self, weapon_property: WeaponProperty):
        return weapon_property in self.__properties

    def __hash__(self):
        calculated_hash: int = 0

        for key, value in self.__properties.items():
            calculated_hash += hash(key.value)
            if isinstance(value, Damage) or isinstance(value, bool):
                calculated_hash += hash(value)
            else:
                calculated_hash += hash(value[0] + value[1])
        return hash(self.__damage) + hash(self.__weapon_type.value) + calculated_hash + self.__ammo

    def __eq__(self, other: 'Weapon'):
        return self.__hash__() == other.__hash__()

    def __ne__(self, other: 'Weapon'):
        return self.__hash__() != other.__hash__()

    def __gt__(self, other: 'Weapon'):
        return self.__hash__() > other.__hash__()

    def __lt__(self, other: 'Weapon'):
        return self.__hash__() < other.__hash__()

    def __ge__(self, other: 'Weapon'):
        return not self < other

    def __le__(self, other):
        return not self > other

    @staticmethod
    def simple_melee(**kwargs):
        return Weapon.create_weapon(WeaponType.SIMPLE_MELEE, **kwargs)

    @staticmethod
    def simple_ranged(**kwargs):
        return Weapon.create_weapon(WeaponType.SIMPLE_RANGED, **kwargs)

    @staticmethod
    def martial_melee(**kwargs):
        return Weapon.create_weapon(WeaponType.MARTIAL_MELEE, **kwargs)

    @staticmethod
    def martial_ranged(**kwargs):
        return Weapon.create_weapon(WeaponType.MARTIAL_RANGED, **kwargs)

    @staticmethod
    def create_weapon(weapon_type: WeaponType, **kwargs):
        if 'versatile' in kwargs:
            versatile = Damage(kwargs['versatile'], kwargs['damage_type'])
            kwargs['versatile'] = versatile

        damage = Damage(kwargs['die_list'], kwargs['damage_type'])
        del kwargs['die_list']
        del kwargs['damage_type']

        properties = {}
        for key, value in kwargs.items():
            properties[WeaponProperty(key)] = value
        return Weapon(damage=damage, weapon_type=weapon_type, properties=properties)
