from enum import Enum
from typing import Dict, List

from dnd.models.armor import Armor
from dnd.models.damage import DamageType
from dnd.models.die import D20, Die
from dnd.models.feat import Feat, FeatType, Resistance
from dnd.models.spell import Spell
from dnd.models.weapon import Weapon, WeaponProperty


class Ability(Enum):
    NONE = ''
    STRENGTH = 'strength'
    DEXTERITY = 'dexterity'
    CONSTITUTION = 'constitution'
    INTELLIGENCE = 'intelligence'
    WISDOM = 'wisdom'
    CHARISMA = 'charisma'

    def __repr__(self):
        return self.value


class CharacterCategory(Enum):
    INDIFFERENT = "indifferent"
    PLAYABLE = "Playable"
    NON_PLAYABLE = "Non-playable"


class Character:
    def __init__(self, strength: int, dexterity: int, constitution: int,
                 intelligence: int, wisdom: int, charisma: int, hit_points: int,
                 category: CharacterCategory = CharacterCategory.INDIFFERENT, name: str = ""):
        Character.check_ability(strength, Ability.STRENGTH)
        Character.check_ability(dexterity, Ability.DEXTERITY)
        Character.check_ability(constitution, Ability.CONSTITUTION)
        Character.check_ability(intelligence, Ability.INTELLIGENCE)
        Character.check_ability(wisdom, Ability.WISDOM)
        Character.check_ability(charisma, Ability.CHARISMA)

        self.__name = name

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
        self.using_shield: bool = False

        self.feat_list: List[Feat] = []

        self.cast_ability: Ability = Ability.NONE
        self.spell_list: List[Spell] = []
        self.__casted_spell: Spell = None

        self.__health_points: int = hit_points
        self.__category = category

    def __repr__(self) -> str:
        dictionary = {
            'name': self.__name,
            **self.abilities,
            'proficiency': self.__proficiency,
            'armor': str(self.armor),
            'weapons': str(self.weapons),
            'active_weapon': str(self.active_weapon),
            'using_shield': str(self.using_shield),
            'feats': str(self.feat_list),
            'hit_points': str(self.__health_points),
            'category': self.category.value
        }
        return str(dictionary)

    def __hash__(self) -> int:
        calculated_hash: int = 0
        for _, value in self.abilities.items():
            calculated_hash += value
        calculated_hash += hash(self.__name)
        calculated_hash += self.__proficiency
        calculated_hash + hash(self.armor)

        for item in self.weapons:
            calculated_hash += hash(item)
        calculated_hash += hash(self.active_weapon)
        calculated_hash += hash(self.using_shield)

        for item in self.feat_list:
            calculated_hash += hash(item.feat_type)
        calculated_hash += hash(self.cast_ability.value)

        for item in self.spell_list:
            calculated_hash += hash(item)
        calculated_hash += self.__health_points
        calculated_hash += hash(self.__category.value)
        return calculated_hash

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __gt__(self, other):
        return hash(self) > hash(other)

    def __ne__(self, other):
        return not self == other

    def __lt__(self, other):
        return not self > other and not self == other

    def __ge__(self, other):
        return not self < other

    def __le__(self, other):
        return not self > other

    @property
    def name(self) -> str:
        return self.__name

    @property
    def armor_class(self):
        if self.armor is not None:
            return self.armor.get_armor_class(self.get_ability_modifier(Ability.DEXTERITY), self.using_shield)
        return 10 + self.get_ability_modifier(Ability.DEXTERITY)

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
        if self.__casted_spell is not None:
            return self.__casted_spell.get_damage()
        return self.active_weapon.get_damage(strength_mod=self.get_ability_modifier(Ability.STRENGTH),
                                             dexterity_mod=self.get_ability_modifier(Ability.DEXTERITY),
                                             use_two_handed=not self.using_shield)

    def cast(self, die: Die = D20) -> int:
        for spell in self.spell_list:
            if spell.can_be_casted():
                self.__casted_spell = spell
                spell.cast()
                return die.roll() + self.get_ability_modifier(self.cast_ability) + self.__proficiency
        self.__casted_spell = None
        return -1

    def attack(self, die: Die = D20) -> int:
        attack_mod = self.get_ability_modifier(Ability.STRENGTH)
        if self.active_weapon.check_property(WeaponProperty.FINESSE) or self.active_weapon.is_ranged:
            attack_mod = self.get_ability_modifier(Ability.DEXTERITY)
        return die.roll() + attack_mod + self.__proficiency

    def get_ability_modifier(self, ability: Ability):
        return Character.get_modifier(self.abilities[ability])
