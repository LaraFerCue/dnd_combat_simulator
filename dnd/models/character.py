from enum import Enum


class Ability(Enum):
    STRENGTH = 'strength'
    DEXTERITY = 'dexterity'
    CONSTITUTION = 'constitution'
    INTELLIGENCE = 'intelligence'
    WISDOM = 'wisdom'
    CHARISMA = 'charismas'


class Character:
    def __init__(self, strength: int, dexterity: int, constitution: int, intelligence: int, wisdom: int, charisma: int):
        Character.check_ability(strength, Ability.STRENGTH)
        Character.check_ability(dexterity, Ability.DEXTERITY)
        Character.check_ability(constitution, Ability.CONSTITUTION)
        Character.check_ability(intelligence, Ability.INTELLIGENCE)
        Character.check_ability(wisdom, Ability.WISDOM)
        Character.check_ability(charisma, Ability.CHARISMA)

        self.strength = strength
        self.dexterity = dexterity
        self.constitution = constitution
        self.intelligence = intelligence
        self.wisdom = wisdom
        self.charisma = charisma
        self.__proficiency: int = 2
        self.__armor_class = 10 + Character.get_modifier(self.dexterity)

    @property
    def proficiency(self) -> int:
        return self.__proficiency

    @proficiency.setter
    def proficiency(self, value: int):
        if value < 0:
            raise AttributeError(f"The proficiency value cannot be negative. Value: {value}.")
        self.__proficiency = value

    @staticmethod
    def check_ability(ability: int, ability_name: Ability):
        if ability < 0 or ability > 20:
            raise AttributeError(f"The abilities must be in range [0, 20]. Found: {ability_name.value} = {ability}")

    @staticmethod
    def get_modifier(ability: int) -> int:
        mod = int(ability / 2) - 5
        return mod