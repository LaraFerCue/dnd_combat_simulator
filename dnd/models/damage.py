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

    MAGIC_ACID = "Magic Acid"
    MAGIC_BLUDGEONING = "Magic Bludgeoning"
    MAGIC_COLD = "Magic Cold"
    MAGIC_FIRE = "Magic Fire"
    MAGIC_FORCE = "Magic Force"
    MAGIC_LIGHTNING = "Magic Lightning"
    MAGIC_NECROTIC = "Magic Necrotic"
    MAGIC_PIERCING = "Magic Piercing"
    MAGIC_POISON = "Magic Poison"
    MAGIC_PSYCHIC = "Magic Psychic"
    MAGIC_RADIANT = "Magic Radiant"
    MAGIC_SLASHING = "Magic Slashing"
    MAGIC_THUNDER = "Magic Thunder"


class Damage:
    def __init__(self, dice_list: List[Die], damage_type: DamageType):
        self.__dice_list = dice_list
        self.__damage_type = damage_type

    def __repr__(self):
        return f"{str(self.__dice_list)} | {str(self.__damage_type.value)}"

    def __hash__(self) -> int:
        calculated_hash: int = 0
        for die in self.__dice_list:
            calculated_hash += hash(die)
        return calculated_hash + hash(self.__damage_type.value)

    def __eq__(self, other: 'Damage'):
        return self.__hash__() == other.__hash__()

    def __ne__(self, other: 'Damage'):
        return self.__hash__() != other.__hash__()

    def __gt__(self, other: 'Damage'):
        return self.__hash__() > other.__hash__()

    def __lt__(self, other: 'Damage'):
        return self.__hash__() < other.__hash__()

    def __ge__(self, other: 'Damage'):
        return self > other or self == other

    def __le__(self, other: 'Damage'):
        return self < other or self == other

    @property
    def damage_type(self):
        return self.__damage_type

    def get_damage(self) -> int:
        damage = 0
        for die in self.__dice_list:
            damage += die.roll()
        return damage
