from enum import Enum
from random import uniform
from typing import List, Tuple


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
    def __init__(self, damage: Tuple[int, int], weapon_type: WeaponType, properties: List[WeaponProperty] = ()):
        self.__damage = damage
        self.__weapon_type = weapon_type
        self.__properties = properties
        self.__ammo: int = 0

    @property
    def ammo(self):
        return self.__ammo

    @ammo.setter
    def ammo(self, value):
        if value < 0:
            raise AttributeError("Ammo cannot be negative")
        self.__ammo = value

    def get_damage(self, strength_mod: int, dexterity_mod: int):
        if self.__weapon_type in [WeaponType.SIMPLE_MELEE, WeaponType.MARTIAL_MELEE]:
            attack_mod = strength_mod
            if WeaponProperty.FINESSE in self.__properties:
                if dexterity_mod > strength_mod:
                    attack_mod = dexterity_mod
        else:
            if self.__ammo <= 0:
                return 0
            self.ammo -= 1
            attack_mod = dexterity_mod

        damage = int(uniform(self.__damage[0], self.__damage[1]))
        return damage + attack_mod
