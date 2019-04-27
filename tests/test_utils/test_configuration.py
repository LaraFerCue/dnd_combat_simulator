from pathlib import Path

from dnd.utils.configuration import read_configuration
from dnd.utils.file_utils import create_character_from_json_file


def test_load_configuration():
    player1 = create_character_from_json_file(Path('tests').joinpath('resources', 'party', 'player1.json'))
    player2 = create_character_from_json_file(Path('tests').joinpath('resources', 'party', 'player2.json'))
    player3 = create_character_from_json_file(Path('tests').joinpath('resources', 'party', 'player3.json'))

    enemy1 = create_character_from_json_file(Path('tests').joinpath('resources', 'enemies', 'enemy.json'))

    players, enemies, iterations, results_folder = read_configuration(
        Path('tests').joinpath('resources', 'configuration.json'))

    assert set(players) == {player1, player2, player3}
    assert set(enemies) == {enemy1}
    assert iterations == 5000
    assert results_folder.absolute() == Path('tests').joinpath('resources', 'results.csv').absolute()
