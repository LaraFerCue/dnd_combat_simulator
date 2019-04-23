from enum import Enum
from typing import List

from dnd.models.die import Die


class DamageType(Enum):
    ACID = "Acid"
    BLUDGEONING = "Bludgeoning"
    COLD = "Cold"
    FIRE = "Fire"
    FORCE = "Force"
    LIGHTNING = "Lightning"
    NECROTIC = "Necrotic"
    PIERCING = "Piercing"
    POISON = "Poison"
    PSYCHIC = "Psychic"
    RADIANT = "Radiant"
    SLASHING = "Slashing"
    THUNDER = "Thunder"

    MAGIC_ACID = "Acid"
    MAGIC_BLUDGEONING = "Bludgeoning"
    MAGIC_COLD = "Cold"
    MAGIC_FIRE = "Fire"
    MAGIC_FORCE = "Force"
    MAGIC_LIGHTNING = "Lightning"
    MAGIC_NECROTIC = "Necrotic"
    MAGIC_PIERCING = "Piercing"
    MAGIC_POISON = "Poison"
    MAGIC_PSYCHIC = "Psychic"
    MAGIC_RADIANT = "Radiant"
    MAGIC_SLASHING = "Slashing"
    MAGIC_THUNDER = "Thunder"


class Damage:
    def __init__(self, dice_list: List[Die], damage_type: DamageType):
        if len(dice_list) == 0:
            raise ValueError(f"The dice list cannot be empty")
        self.__dice_list = dice_list
        self.__damage_type = damage_type

    def __repr__(self):
        return f"{str(self.__dice_list)} | {str(self.__damage_type.value)}"

    @property
    def damage_type(self):
        return self.__damage_type

    def get_damage(self) -> int:
        damage = 0
        for die in self.__dice_list:
            damage += die.roll()
        return damage
