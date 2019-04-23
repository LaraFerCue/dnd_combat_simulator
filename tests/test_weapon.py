import pytest

from dnd.models.damage import DamageType, Damage
from dnd.models.die import D6, D4
from dnd.models.weapon import Weapon, WeaponType, WeaponProperty


def test_ranged_weapon_without_ammo():
    damage = Damage([D4], DamageType.PIERCING)
    ranged = Weapon(damage, WeaponType.SIMPLE_RANGED, {WeaponProperty.AMMUNITION: None})

    for _ in range(0, 5000):
        damage = ranged.get_damage(0, 0)
        assert damage == 0


def test_ranged_weapon():
    damage = Damage([D4], DamageType.PIERCING)
    ranged = Weapon(damage, WeaponType.SIMPLE_RANGED, {WeaponProperty.AMMUNITION: None})
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
    damage = Damage([D4], DamageType.PIERCING)
    ranged = Weapon(damage, WeaponType.SIMPLE_MELEE)

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
    damage = Damage([D4], DamageType.PIERCING)
    ranged = Weapon(damage, WeaponType.SIMPLE_MELEE, {WeaponProperty.FINESSE: None})

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
    damage = Damage([D6, D6], DamageType.PIERCING)
    ranged = Weapon(damage, WeaponType.SIMPLE_MELEE, {WeaponProperty.FINESSE: None})

    for _ in range(0, 5000):
        damage = ranged.get_damage(0, 0)
        assert damage in range(2, 13)

    for _ in range(0, 5000):
        damage = ranged.get_damage(5, 0)
        assert damage in range(7, 18)

    for _ in range(0, 5000):
        damage = ranged.get_damage(0, 5)
        assert damage in range(7, 18)


def test_weapon_with_versatility_but_only_one_die():
    with pytest.raises(ValueError):
        Weapon(Damage([D4], DamageType.SLASHING), WeaponType.MARTIAL_MELEE, {WeaponProperty.VERSATILE: None})


def test_weapon_damage_with_versatility():
    weapon = Weapon(Damage([D4], DamageType.SLASHING), WeaponType.MARTIAL_MELEE,
                    {WeaponProperty.VERSATILE: Damage([D6], DamageType.SLASHING)})

    for _ in range(0, 5000):
        assert weapon.get_damage(0, 0, False) in range(1, 5)
        assert weapon.get_damage(0, 0, True) in range(1, 7)
