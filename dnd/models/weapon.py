from enum import Enum
from typing import Union, Dict, Tuple

from dnd.models.damage import Damage


class WeaponType(Enum):
    SIMPLE_MELEE = "Simple Melee"
    SIMPLE_RANGED = "Simple Ranged"
    MARTIAL_MELEE = "Martial Melee"
    MARTIAL_RANGED = "Martial Ranged"


class WeaponProperty(Enum):
    AMMUNITION = "Ammunition"
    FINESSE = "Finesse"
    HEAVY = "Heavy"
    LIGHT = "Light"
    LOADING = "Loading"
    RANGE = "Range"
    REACH = "Reach"
    SPECIAL = "Special"
    THROWN = "Thrown"
    TWO_HANDED = "Two-Handed"
    VERSATILE = "Versatile"


class Weapon:
    def __init__(self, damage: Damage, weapon_type: WeaponType,
                 properties: Dict[WeaponProperty, Union[Tuple[int, int], None, Damage]] = ()):
        self.__damage: Damage = damage
        self.__weapon_type = weapon_type
        self.__properties = properties
        self.__ammo: int = 0

        if WeaponProperty.VERSATILE in properties and not isinstance(properties[WeaponProperty.VERSATILE], Damage):
            raise ValueError('Versatile needs a Damage value')

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

    @staticmethod
    def create_simple_melee_weapon(damage: Damage, **kwargs):
        return Weapon(damage=damage, weapon_type=WeaponType.SIMPLE_MELEE, properties={**kwargs})
