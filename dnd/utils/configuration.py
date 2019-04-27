import json
from pathlib import Path
from typing import Tuple, List

from dnd.models.character import Character
from dnd.utils.file_utils import load_party_from_folder


def read_configuration(configuration_json_file: Path) -> Tuple[List[Character], List[Character], int, Path]:
    with open(configuration_json_file.as_posix()) as json_file:
        json_dict = json.load(json_file)

    iterations = json_dict['iterations']
    players_folder = configuration_json_file.parent.joinpath(json_dict['players-folder'])
    enemies_folder = configuration_json_file.parent.joinpath(json_dict['enemies-folder'])
    players = load_party_from_folder(players_folder)
    enemies = load_party_from_folder(enemies_folder)
    results_directory = configuration_json_file.parent.joinpath(json_dict['results-file'])
    return players, enemies, iterations, results_directory
