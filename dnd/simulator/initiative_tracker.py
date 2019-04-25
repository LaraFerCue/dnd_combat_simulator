from typing import List, Dict, Union

from dnd.models.character import Character, Ability
from dnd.models.die import D20, Die


def get_enemies_modifier(enemies):
    dex_mod: int = -99
    for enemy in enemies:
        modifier = enemy.get_ability_modifier(Ability.DEXTERITY)
        if modifier > dex_mod:
            dex_mod = modifier
    return dex_mod


class Initiative:
    def __init__(self):
        self.__character_list: List[Character] = []
        self.__index: int = 0

    def add(self, character: Character) -> None:
        self.__character_list.append(character)

    def get_characters(self) -> List[Character]:
        return self.__character_list.copy()

    def get_next(self) -> Union[Character, None]:
        if self.__index >= len(self.__character_list):
            self.__index = 0
            return None
        character = self.__character_list[self.__index]
        self.__index += 1
        return character


class InitiativeTracker:
    def __init__(self, players: List[Character], enemies: List[Character], die: Die = D20):
        self._initiative_map: Dict[int, Initiative] = {}
        self._current_initiative: int = -1

        self.set_players_initiative(players, die)
        self.set_enemies_initiative(die, enemies)

    def set_players_initiative(self, players: List[Character], die: Die):
        for player in players:
            initiative = die.roll() + player.get_ability_modifier(Ability.DEXTERITY)

            if initiative not in self._initiative_map:
                self._initiative_map[initiative] = Initiative()
            self._initiative_map[initiative].add(player)

    def set_enemies_initiative(self, die: Die, enemies: List[Character]):
        dex_mod = get_enemies_modifier(enemies)
        enemies_initiative = die.roll() + dex_mod

        if enemies_initiative not in self._initiative_map:
            self._initiative_map[enemies_initiative] = Initiative()
        for enemy in enemies:
            self._initiative_map[enemies_initiative].add(enemy)

    def get_next_character(self) -> Union[Character, None]:
        if self._current_initiative < 0:
            self._current_initiative = max(self._initiative_map.keys())

        character = self._initiative_map[self._current_initiative].get_next()
        if character is None:
            self._current_initiative = self.calculate_next_initiative()
            if self._current_initiative < 0:
                return None
            return self.get_next_character()
        return character

    def calculate_next_initiative(self) -> int:
        initiatives = []
        for initiative in self._initiative_map.keys():
            if initiative < self._current_initiative:
                initiatives.append(initiative)
        if len(initiatives) > 0:
            return initiatives[0]
        return -1
