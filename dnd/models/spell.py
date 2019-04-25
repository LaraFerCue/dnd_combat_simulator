from dnd.models.damage import Damage


class SpellWornOut(BaseException):
    pass


class Spell:
    def __init__(self, damage: Damage, spell_lvl: int = 0):
        self.__damage = damage
        self.__spell_lvl = spell_lvl
        self.__used: int = 0
        self.slots = 0

    @property
    def level(self) -> int:
        return self.__spell_lvl

    @property
    def times_used(self) -> int:
        return self.__used

    def get_damage(self) -> int:
        if self.__used >= self.slots:
            raise SpellWornOut(f"Spell casted maximum number of times ({self.slots})")
        self.__used += 1
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
