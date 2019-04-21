from typing import List

from dnd.models.die import Die


class Spell:
    def __init__(self, damage: List[Die]):
        self.__damage = damage

    def get_damage(self) -> int:
        damage = 0
        for die in self.__damage:
            damage += die.roll()
        return damage
