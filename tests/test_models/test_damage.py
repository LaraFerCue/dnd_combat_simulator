from dnd.models.damage import Damage, DamageType
from dnd.models.die import D10, D6, D4


def test_damage_single_die():
    damage_system = Damage([D10], DamageType.BLUDGEONING)

    for _ in range(0, 5000):
        assert damage_system.get_damage() in range(1, 11)


def test_damage_multiple_dice():
    damage_system = Damage([D6, D6], DamageType.BLUDGEONING)

    for _ in range(0, 5000):
        assert damage_system.get_damage() in range(2, 13)


def test_damage_without_die():
    damage = Damage([], DamageType.BLUDGEONING)
    assert damage.get_damage() == 0


def test_two_equal_damage_classes():
    damage1 = Damage([D6], DamageType.BLUDGEONING)
    damage2 = Damage([D6], DamageType.BLUDGEONING)

    assert damage1 == damage2


def test_different_damage_classes():
    damage1 = Damage([D4], DamageType.BLUDGEONING)
    damage2 = Damage([D6], DamageType.BLUDGEONING)

    assert damage1 != damage2

    damage1 = Damage([D6, D6], DamageType.BLUDGEONING)
    assert damage1 != damage2

    damage1 = Damage([D6], DamageType.PIERCING)
    assert damage1 != damage2
