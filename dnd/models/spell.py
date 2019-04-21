from typing import List

from dnd.models.damage import Damage, DamageType
from dnd.models.die import Die


class Spell:
    def __init__(self, damage: List[Die]):
        self.__damage = Damage(damage, DamageType.MAGIC)

    def get_damage(self) -> int:
        return self.__damage.get_damage()
