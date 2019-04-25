from dnd.models.damage import Damage


class Spell:
    def __init__(self, damage: Damage):
        self.__damage = damage

    def get_damage(self) -> int:
        return self.__damage.get_damage()

    def __hash__(self) -> int:
        return hash(self.__damage)

    def __eq__(self, other: 'Spell'):
        return hash(self) == hash(other)

    def __gt__(self, other):
        return hash(self) > hash(other)

    def __ne__(self, other):
        return not self == other

    def __ge__(self, other):
        return self > other or self == other

    def __lt__(self, other):
        return not self >= other

    def __le__(self, other):
        return not self > other
