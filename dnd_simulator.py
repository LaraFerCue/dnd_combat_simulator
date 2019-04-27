from pathlib import Path
from typing import List

import argparse

from dnd.models.character import Character
from dnd.simulator.combat import Combat
from dnd.simulator.statistics_tracker import StatisticsTracker
from dnd.utils.configuration import read_configuration


def lose_checker_function(characters: List[Character]) -> bool:
    for character in characters:
        if character.hit_points <= 0:
            return True
    return False


parser = argparse.ArgumentParser(description="D&D 5th Combat Simulator")
parser.add_argument('--config-file', help="Configuration file to be loaded")

args = parser.parse_args()

players, enemies, iteration, results_file = read_configuration(Path(args.config_file))

combat = Combat(players=players, enemies=enemies, lose_checker=lose_checker_function)
statistics_tracker = StatisticsTracker()

for _ in range(0, iteration):
    result = combat.initiate_combat()
    statistics_tracker.add(combat.get_statistics(), result)

with open(results_file.as_posix(), 'w') as csv_file:
    csv_file.write(statistics_tracker.to_csv())
print(f"Percentage of victories: {statistics_tracker.get_win_percentage()}")
