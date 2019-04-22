from enum import Enum
from typing import Dict, List

from dnd.models.armor import Armor
from dnd.models.damage import DamageType
from dnd.models.feat import Feat, FeatType, Resistance
from dnd.models.spell import Spell
from dnd.models.weapon import Weapon


class Ability(Enum):
    STRENGTH = 'strength'
    DEXTERITY = 'dexterity'
    CONSTITUTION = 'constitution'
    INTELLIGENCE = 'intelligence'
    WISDOM = 'wisdom'
    CHARISMA = 'charismas'


class Character:
    def __init__(self, strength: int, dexterity: int, constitution: int,
                 intelligence: int, wisdom: int, charisma: int, hit_points: int):
        Character.check_ability(strength, Ability.STRENGTH)
        Character.check_ability(dexterity, Ability.DEXTERITY)
        Character.check_ability(constitution, Ability.CONSTITUTION)
        Character.check_ability(intelligence, Ability.INTELLIGENCE)
        Character.check_ability(wisdom, Ability.WISDOM)
        Character.check_ability(charisma, Ability.CHARISMA)

        self.abilities: Dict[Ability, int] = {
            Ability.STRENGTH: strength,
            Ability.DEXTERITY: dexterity,
            Ability.CONSTITUTION: constitution,
            Ability.INTELLIGENCE: intelligence,
            Ability.WISDOM: wisdom,
            Ability.CHARISMA: charisma
        }
        self.__proficiency: int = 2
        self.armor: Armor = None
        self.weapons: List[Weapon] = []
        self.active_weapon: Weapon = None
        self.spell_list: List[Spell] = []
        self.feat_list: List[Feat] = []
        self.__health_points: int = hit_points

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

    @property
    def hit_points(self):
        return self.__health_points

    def apply_damage(self, damage: int, damage_type: DamageType):
        for feat in self.feat_list:
            if feat.feat_type == FeatType.RESISTANCE:
                resistance: Resistance = feat
                damage = resistance.modify_damage(damage, damage_type)

        self.__health_points -= damage
