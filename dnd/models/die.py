from random import uniform


class Die:
    def __init__(self, sides: int):
        self.__sides = sides

    def roll(self):
        return round(uniform(1, self.__sides))


D4 = Die(4)
D6 = Die(6)
D8 = Die(8)
D10 = Die(10)
D12 = Die(12)
D20 = Die(20)
