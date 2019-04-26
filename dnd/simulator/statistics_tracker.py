from typing import Dict, Union, List

from dnd.simulator.combat import Combat


class StatisticsTracker:
    def __init__(self):
        self.__tracker: List[Dict[str, Union[int, Dict[str, int], Combat.Result]]] = []

    def add(self, turn: Dict[str, Union[int, Dict[str, int]]], result: Combat.Result):
        self.__tracker.append({**turn, 'result': result})

    def to_csv(self):
        header = 'result;# turns;'
        for player_name, _ in self.__tracker[0]['players'].items():
            header += f"player: {player_name};"
        for enemy_name, _ in self.__tracker[0]['enemies'].items():
            header += f"enemy: {enemy_name};"

        header += '\n'
        body = ''
        for iterate in self.__tracker:
            body += f'{iterate["result"].value};{iterate["turns"]};'
            for _, player_hit_points in iterate['players'].items():
                body += f"{player_hit_points};"
            for _, enemy_hit_points in iterate['enemies'].items():
                body += f"{enemy_hit_points};"
            body += '\n'
        return header + body
