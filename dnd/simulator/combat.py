from enum import Enum
from typing import List, Callable, Dict

from dnd.models.character import Character, CharacterCategory
from dnd.models.die import D20, Die
from dnd.simulator.initiative_tracker import InitiativeTracker


class Combat:
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
    def select_spell_or_weapon(character: Character):
        for spell in character.spell_list:
            if spell.can_be_casted():
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
                action = Combat.select_spell_or_weapon(character)

                if action == Combat.Action.ATTACK and character.attack(self.__die) >= target.armor_class:
                    target.apply_damage(character.damage(), character.active_weapon.damage.damage_type)
            character = self.__initiative_tracker.get_next_character()
