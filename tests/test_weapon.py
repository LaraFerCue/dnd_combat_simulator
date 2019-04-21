from dnd.models.die import D6, D4

from dnd.models.weapon import Weapon, WeaponType, WeaponProperty


def test_ranged_weapon_without_ammo():
    ranged = Weapon([D4], WeaponType.SIMPLE_RANGED, [WeaponProperty.AMMUNITION])

    for _ in range(0, 5000):
        damage = ranged.get_damage(0, 0)
        assert damage == 0


def test_ranged_weapon():
    ranged = Weapon([D4], WeaponType.SIMPLE_RANGED, [WeaponProperty.AMMUNITION])
    ranged.ammo = 200000

    for _ in range(0, 5000):
        damage = ranged.get_damage(0, 0)
        assert damage in range(1, 5)

    for _ in range(0, 5000):
        damage = ranged.get_damage(5, 0)
        assert damage in range(1, 5)

    for _ in range(0, 5000):
        damage = ranged.get_damage(0, 5)
        assert damage in range(5, 10)


def test_melee_weapon_without_finesse():
    ranged = Weapon([D4], WeaponType.SIMPLE_MELEE)

    for _ in range(0, 5000):
        damage = ranged.get_damage(0, 0)
        assert damage in range(1, 5)

    for _ in range(0, 5000):
        damage = ranged.get_damage(5, 0)
        assert damage in range(5, 10)

    for _ in range(0, 5000):
        damage = ranged.get_damage(0, 5)
        assert damage in range(1, 5)


def test_melee_weapon_with_finesse():
    ranged = Weapon([D4], WeaponType.SIMPLE_MELEE, [WeaponProperty.FINESSE])

    for _ in range(0, 5000):
        damage = ranged.get_damage(0, 0)
        assert damage in range(1, 5)

    for _ in range(0, 5000):
        damage = ranged.get_damage(5, 0)
        assert damage in range(5, 10)

    for _ in range(0, 5000):
        damage = ranged.get_damage(0, 5)
        assert damage in range(5, 10)


def test_weapon_with_several_damage_die():
    ranged = Weapon([D6, D6], WeaponType.SIMPLE_MELEE, [WeaponProperty.FINESSE])

    for _ in range(0, 5000):
        damage = ranged.get_damage(0, 0)
        assert damage in range(2, 13)

    for _ in range(0, 5000):
        damage = ranged.get_damage(5, 0)
        assert damage in range(7, 18)

    for _ in range(0, 5000):
        damage = ranged.get_damage(0, 5)
        assert damage in range(7, 18)
