from random import uniform


class Die:
    def __init__(self, sides: int):
        self._sides: int = sides

    def __repr__(self):
        return f"D{self._sides}"

    def __hash__(self) -> int:
        return self._sides

    def __eq__(self, other: 'Die'):
        return self._sides == other._sides

    def __ne__(self, other):
        return not self.__eq__(other)

    def __gt__(self, other):
        return self._sides > other.__sides

    def __lt__(self, other):
        return self._sides < other.__sides

    def __ge__(self, other):
        return self.__gt__(other) or self.__eq__(other)

    def __le__(self, other):
        return self.__lt__(other) or self.__eq__(other)

    def roll(self) -> int:
        return round(uniform(1, self._sides))


D4 = Die(4)
D6 = Die(6)
D8 = Die(8)
D10 = Die(10)
D12 = Die(12)
D20 = Die(20)
