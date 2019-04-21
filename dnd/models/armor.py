from enum import Enum


class ArmorType(Enum):
    LIGHT = "Light"
    MEDIUM = "Medium"
    HEAVY = "Heavy"


class Armor:
    def __init__(self, armor_class: int, armor_type: ArmorType):
        self.__armor_class = armor_class
        self.__type = armor_type

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
