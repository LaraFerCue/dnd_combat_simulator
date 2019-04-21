from enum import Enum
from typing import List

from dnd.models.die import Die


class DamageType(Enum):
    BLUDGEONING = "Bludgeoning"
    PIERCING = "Piercing"
    SLASHING = "Slashing"
    MAGIC = "Magic"


class Damage:
    def __init__(self, dice_list: List[Die], damage_type: DamageType):
        if len(dice_list) == 0:
            raise ValueError(f"The dice list cannot be empty")
        self.__dice_list = dice_list
        self.__damage_type = damage_type

    @property
    def damage_type(self):
        return self.__damage_type

    def get_damage(self) -> int:
        damage = 0
        for die in self.__dice_list:
            damage += die.roll()
        return damage
