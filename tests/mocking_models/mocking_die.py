from dnd.models.die import Die


class MockingDie(Die):
    def __init__(self, sides: int):
        super().__init__(sides)

    def roll(self):
        return self._sides
