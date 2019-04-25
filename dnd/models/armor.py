from enum import Enum


class ArmorType(Enum):
    LIGHT = "Light"
    MEDIUM = "Medium"
    HEAVY = "Heavy"


class Armor:
    def __init__(self, armor_class: int, armor_type: ArmorType):
        self.__armor_class = armor_class
        self.__type = armor_type

    def __hash__(self):
        return self.__armor_class + hash(self.__type.value)

    def __repr__(self):
        return f"{self.__armor_class} | {self.__type.value}"

    def __eq__(self, other: 'Armor'):
        return self.__hash__() == other.__hash__()

    def __ne__(self, other: 'Armor'):
        return not self == other

    def __gt__(self, other: 'Armor'):
        return self.__hash__() > other.__hash__()

    def __lt__(self, other: 'Armor'):
        return self.__hash__() < other.__hash__()

    def __ge__(self, other):
        return not self < other

    def __le__(self, other):
        return not self > other

    @property
    def armor_type(self):
        return self.__type

    def get_armor_class(self, dexterity_modifier: int, with_shield: bool = False) -> int:
        armor_class = self.__armor_class
        if self.__type == ArmorType.MEDIUM:
            armor_class += min(dexterity_modifier, 2)
        elif self.__type == ArmorType.LIGHT:
            armor_class += dexterity_modifier

        if with_shield:
            armor_class += 2
        return armor_class
