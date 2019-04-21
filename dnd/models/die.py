from random import uniform


class Die:
    def __init__(self, sides: int):
        self.__sides = sides

    def roll(self):
        return round(uniform(1, self.__sides))
