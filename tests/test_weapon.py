from dnd.models.die import D4
from dnd.models.weapon import Weapon, WeaponType, WeaponProperty


def test_ranged_weapon_without_ammo():
    ranged = Weapon(D4, WeaponType.SIMPLE_RANGED)

    damage = ranged.get_damage(0, 0)
    assert damage == 0


def test_ranged_weapon():
    ranged = Weapon(D4, WeaponType.SIMPLE_RANGED)
    ranged.ammo = 20

    damage = ranged.get_damage(0, 0)
    assert damage in range(1, 5)

    damage = ranged.get_damage(5, 0)
    assert damage in range(1, 5)

    damage = ranged.get_damage(0, 5)
    assert damage in range(5, 10)


def test_melee_weapon_without_finesse():
    ranged = Weapon(D4, WeaponType.SIMPLE_MELEE)

    damage = ranged.get_damage(0, 0)
    assert damage in range(1, 5)

    damage = ranged.get_damage(5, 0)
    assert damage in range(5, 10)

    damage = ranged.get_damage(0, 5)
    assert damage in range(1, 5)


def test_melee_weapon_with_finesse():
    ranged = Weapon(D4, WeaponType.SIMPLE_MELEE, [WeaponProperty.FINESSE])

    damage = ranged.get_damage(0, 0)
    assert damage in range(1, 5)

    damage = ranged.get_damage(5, 0)
    assert damage in range(5, 10)

    damage = ranged.get_damage(0, 5)
    assert damage in range(5, 10)
