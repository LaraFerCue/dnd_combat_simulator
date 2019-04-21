import pytest

from dnd.models.damage import Damage, DamageType
from dnd.models.die import D10, D6


def test_damage_single_die():
    damage_system = Damage([D10], DamageType.BLUDGEONING)

    for _ in range(0, 5000):
        assert damage_system.get_damage() in range(1, 11)


def test_damage_multiple_dice():
    damage_system = Damage([D6, D6], DamageType.BLUDGEONING)

    for _ in range(0, 5000):
        assert damage_system.get_damage() in range(2, 13)


def test_damage_without_die():
    with pytest.raises(ValueError):
        Damage([], DamageType.BLUDGEONING)
