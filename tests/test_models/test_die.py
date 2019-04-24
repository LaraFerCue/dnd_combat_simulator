from typing import Set

from dnd.models.die import Die


def get_die_results(sides: int) -> Set[int]:
    die = Die(sides)
    results = []

    for _ in range(0, 5000):
        results.append(die.roll())

    return set(results)


def get_incremental_set(end: int) -> Set[int]:
    incremental_set = []

    for idx in range(1, end + 1):
        incremental_set.append(idx)

    return set(incremental_set)


def test_four_sided_die():
    assert get_die_results(4) == get_incremental_set(4)


def test_six_sided_die():
    assert get_die_results(6) == get_incremental_set(6)


def test_eight_sided_die():
    assert get_die_results(8) == get_incremental_set(8)


def test_ten_sided_die():
    assert get_die_results(10) == get_incremental_set(10)


def test_twelve_sided_die():
    assert get_die_results(12) == get_incremental_set(12)


def test_twenty_sided_die():
    assert get_die_results(20) == get_incremental_set(20)


def test_dice_with_same_number_of_sides():
    die1 = Die(8)
    die2 = Die(8)

    assert die1 == die2


def test_dice_with_different_number_of_sides():
    die1 = Die(8)
    die2 = Die(10)

    assert die1 != die2
