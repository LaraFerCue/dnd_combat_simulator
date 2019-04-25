from enum import Enum
from typing import Dict, List

from dnd.models.armor import Armor
from dnd.models.damage import DamageType
from dnd.models.die import D20, Die
from dnd.models.feat import Feat, FeatType, Resistance
from dnd.models.weapon import Weapon, WeaponProperty


class Ability(Enum):
    NONE = ''
    STRENGTH = 'strength'
    DEXTERITY = 'dexterity'
    CONSTITUTION = 'constitution'
    INTELLIGENCE = 'intelligence'
    WISDOM = 'wisdom'
    CHARISMA = 'charisma'


class CharacterCategory(Enum):
    INDIFFERENT = "indifferent"
    PLAYABLE = "Playable"
    NON_PLAYABLE = "Non-playable"


class Character:
    def __init__(self, strength: int, dexterity: int, constitution: int,
                 intelligence: int, wisdom: int, charisma: int, hit_points: int,
                 category: CharacterCategory = CharacterCategory.INDIFFERENT):
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
        self.cast_ability: Ability = Ability.NONE

        self.armor: Armor = None
        self.weapons: List[Weapon] = []
        self.active_weapon: Weapon = None
        self.using_shield: bool = False

        self.feat_list: List[Feat] = []

        self.__health_points: int = hit_points
        self.__category = category

    @property
    def armor_class(self):
        return self.armor.get_armor_class(self.get_ability_modifier(Ability.DEXTERITY), self.using_shield)

    @property
    def category(self) -> CharacterCategory:
        return self.__category

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

    @staticmethod
    def new(**kwargs):
        return Character(**kwargs)

    @property
    def hit_points(self):
        return self.__health_points

    def apply_damage(self, damage: int, damage_type: DamageType):
        for feat in self.feat_list:
            if feat.feat_type == FeatType.RESISTANCE:
                resistance: Resistance = feat
                damage = resistance.modify_damage(damage, damage_type)

        self.__health_points -= damage

    def damage(self) -> int:
        return self.active_weapon.get_damage(strength_mod=self.get_ability_modifier(Ability.STRENGTH),
                                             dexterity_mod=self.get_ability_modifier(Ability.DEXTERITY),
                                             use_two_handed=not self.using_shield)

    def attack(self, die: Die = D20):
        attack_mod = self.get_ability_modifier(Ability.STRENGTH)
        if self.active_weapon.check_property(WeaponProperty.FINESSE) or self.active_weapon.is_ranged:
            attack_mod = self.get_ability_modifier(Ability.DEXTERITY)
        return die.roll() + attack_mod + self.__proficiency

    def get_ability_modifier(self, ability: Ability):
        return Character.get_modifier(self.abilities[ability])
