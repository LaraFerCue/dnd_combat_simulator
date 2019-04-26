import json

from dnd.simulator.combat import Combat
from dnd.simulator.statistics_tracker import StatisticsTracker


def test_statistics_tracker_one_track():
    statistics_tracker = StatisticsTracker()

    with open('tests/resources/statistics_one_track.json') as json_file:
        statistics_tracker.add(json.load(json_file), Combat.Result.WIN)
    with open('tests/resources/statistics_one_track.csv') as csv_file:
        csv_data = csv_file.read()
    assert statistics_tracker.to_csv() == csv_data


def test_statistics_tracker_several_tracks():
    statistics_tracker = StatisticsTracker()

    with open('tests/resources/statistics_several_tracks.json') as json_file:
        for track in json.load(json_file):
            statistics_tracker.add(track, Combat.Result.WIN)
    with open('tests/resources/statistics_several_tracks.csv') as csv_file:
        csv_data = csv_file.read()
    assert statistics_tracker.to_csv() == csv_data
