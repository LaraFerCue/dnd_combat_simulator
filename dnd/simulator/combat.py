from enum import Enum
from typing import List, Callable, Dict, Union, Tuple

from dnd.models.character import Character, CharacterCategory, Ability
from dnd.models.damage import DamageType
from dnd.models.die import D20, Die
from dnd.models.spell import Spell
from dnd.simulator.initiative_tracker import InitiativeTracker


class UnknownActionError(BaseException):
    pass


class Combat:
    CRITICAL_HIT = 20
    CRITICAL_MISS = 1

    class Result(Enum):
        TIE = "tie"
        WIN = "win"
        LOSE = "lose"

    class Action(Enum):
        ATTACK = 0
        CAST = 1

    def __init__(self, players: List[Character], enemies: List[Character],
                 lose_checker: Callable[[List[Character]], bool], die: Die = D20):
        self.__players = players
        self.__enemies = enemies
        self.__die = die
        self.__initiative_tracker: InitiativeTracker = InitiativeTracker(players=players, enemies=enemies, die=die)
        self.__turn: int = 0
        self.__lose_checker: Callable[[List[Character]], bool] = lose_checker

    def get_player_target(self) -> Character:
        armor_class = 0
        target = None
        for player in self.__players:
            if player.armor_class + player.hit_points > armor_class:
                target = player
                armor_class = player.armor_class + player.hit_points
        return target

    def get_enemy_target(self) -> Character:
        armor_class = -1
        target = None
        for enemy in self.__enemies:
            if enemy.hit_points > 0 and (enemy.armor_class < armor_class or armor_class < 0):
                target = enemy
                armor_class = enemy.armor_class
        return target

    def get_statistics(self) -> Dict:
        statistics = {'turns': self.__turn, 'players': {}, 'enemies': {}}

        for player in self.__players:
            statistics['players'][player.name] = player.hit_points
        for enemy in self.__enemies:
            statistics['enemies'][enemy.name] = enemy.hit_points
        return statistics

    def initiate_combat(self) -> Result:
        while not self.__lose_checker(self.__players):
            self._turn_actions()
            self.__turn += 1

            hit_points: int = 0
            for enemy in self.__enemies:
                hit_points += enemy.hit_points
            if hit_points <= 0:
                return Combat.Result.WIN

        return Combat.Result.LOSE

    @staticmethod
    def select_available_spell(character: Character) -> Union[Spell, None]:
        for spell in character.spell_list:
            if spell.can_be_casted():
                return spell
        return None

    @staticmethod
    def select_spell_or_weapon(character: Character):
        if Combat.select_available_spell(character) is not None:
            return Combat.Action.CAST
        return Combat.Action.ATTACK

    def _turn_actions(self) -> None:
        character = self.__initiative_tracker.get_next_character()
        while character is not None:
            if character.category == CharacterCategory.NON_PLAYABLE:
                target = self.get_player_target()
            elif character.category == CharacterCategory.PLAYABLE:
                target = self.get_enemy_target()
            else:
                raise AttributeError(f"No implemented behavior for character category {character.category.value}")
            if target is None:
                return
            if character.hit_points > 0:
                self.perform_attack(character, target)
            character = self.__initiative_tracker.get_next_character()

    def perform_attack(self, character, target):
        action = Combat.select_spell_or_weapon(character)

        attack_roll = self.__die.roll()
        is_critical_hit = attack_roll == Combat.CRITICAL_HIT
        is_critical_miss = attack_roll == Combat.CRITICAL_MISS

        if is_critical_miss:
            if character.category == CharacterCategory.NON_PLAYABLE:
                target = Combat.get_target_on_critical_miss(character, self.__enemies)
            elif character.category == CharacterCategory.PLAYABLE:
                target = Combat.get_target_on_critical_miss(character, self.__players)

        if action == Combat.Action.ATTACK:
            attack_roll += character.attack_modifier
        elif action == Combat.Action.CAST:
            attack_roll += character.cast_modifier
        if attack_roll >= target.armor_class or is_critical_hit:
            damage, damage_type = self.get_damage(action, character, is_critical_hit)
            target.apply_damage(damage, damage_type)

        return character

    def get_damage(self, action, character, is_critical_hit):
        if action == Combat.Action.CAST:
            damage, damage_type = self.get_spell_damage(character, is_critical_hit)
        elif action == Combat.Action.ATTACK:
            damage, damage_type = self.get_weapon_damage(character, is_critical_hit)
        else:
            raise UnknownActionError(f"Unknown action to perform {action}")
        return damage, damage_type

    @staticmethod
    def get_weapon_damage(character: Character, is_critical_hit: bool) -> Tuple[int, DamageType]:
        damage = character.active_weapon.get_damage(character.get_ability_modifier(Ability.STRENGTH),
                                                    character.get_ability_modifier(Ability.DEXTERITY),
                                                    not character.using_shield)
        damage_type = character.active_weapon.damage.damage_type
        if is_critical_hit:
            damage += character.active_weapon.get_damage(
                character.get_ability_modifier(Ability.STRENGTH),
                character.get_ability_modifier(Ability.DEXTERITY),
                not character.using_shield)
        return damage, damage_type

    @staticmethod
    def get_spell_damage(character: Character, is_critical_hit: bool) -> Tuple[int, DamageType]:
        spell = Combat.select_available_spell(character)
        spell.cast()
        damage = spell.get_damage()
        damage_type = spell.damage_type
        if is_critical_hit:
            damage += spell.get_damage()
        return damage, damage_type

    @staticmethod
    def get_target_on_critical_miss(character: Character, list_of_characters: List[Character]) -> Character:
        for enemy in list_of_characters:
            if enemy.hit_points > 0 and enemy != character:
                return enemy
        return character
