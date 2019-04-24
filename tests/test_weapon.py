import pytest

from dnd.models.damage import DamageType, Damage
from dnd.models.die import D6, D4
from dnd.models.weapon import Weapon, WeaponType, WeaponProperty


def test_ranged_weapon_without_ammo():
    damage = Damage([D4], DamageType.PIERCING)
    ranged = Weapon(damage, WeaponType.SIMPLE_RANGED, {WeaponProperty.AMMUNITION: (20, 60)})

    for _ in range(0, 5000):
        damage = ranged.get_damage(0, 0)
        assert damage == 0


def test_ranged_weapon():
    damage = Damage([D4], DamageType.PIERCING)
    ranged = Weapon(damage, WeaponType.SIMPLE_RANGED, {WeaponProperty.AMMUNITION: (20, 60)})
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
    ranged = Weapon(damage, WeaponType.SIMPLE_MELEE, {WeaponProperty.FINESSE: True})

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
    ranged = Weapon(damage, WeaponType.SIMPLE_MELEE, {WeaponProperty.FINESSE: True})

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
        Weapon(Damage([D4], DamageType.SLASHING), WeaponType.MARTIAL_MELEE,
               {WeaponProperty.VERSATILE: True})


def test_weapon_damage_with_versatility():
    weapon = Weapon(Damage([D4], DamageType.SLASHING), WeaponType.MARTIAL_MELEE,
                    {WeaponProperty.VERSATILE: Damage([D6], DamageType.SLASHING)})

    for _ in range(0, 5000):
        assert weapon.get_damage(0, 0, False) in range(1, 5)
        assert weapon.get_damage(0, 0, True) in range(1, 7)


def test_simple_melee_weapon():
    weapon1 = Weapon.simple_melee(die_list=[D4], damage_type=DamageType.BLUDGEONING)
    weapon2 = Weapon.simple_melee(die_list=[D4], damage_type=DamageType.BLUDGEONING, two_handed=True)
    weapon3 = Weapon.simple_melee(die_list=[D4], damage_type=DamageType.BLUDGEONING, versatile=[D6])
    weapon4 = Weapon.simple_melee(die_list=[D4], damage_type=DamageType.BLUDGEONING, thrown=(10, 20))

    assert weapon1 == Weapon(damage=Damage([D4], DamageType.BLUDGEONING), weapon_type=WeaponType.SIMPLE_MELEE)
    assert weapon2 == Weapon(damage=Damage([D4], DamageType.BLUDGEONING), weapon_type=WeaponType.SIMPLE_MELEE,
                             properties={WeaponProperty.TWO_HANDED: True})
    assert weapon3 == Weapon(damage=Damage([D4], DamageType.BLUDGEONING), weapon_type=WeaponType.SIMPLE_MELEE,
                             properties={WeaponProperty.VERSATILE: Damage([D6], DamageType.BLUDGEONING)})
    assert weapon4 == Weapon(damage=Damage([D4], DamageType.BLUDGEONING), weapon_type=WeaponType.SIMPLE_MELEE,
                             properties={WeaponProperty.THROWN: (10, 20)})


def test_simple_ranged_weapon():
    weapon1 = Weapon.simple_ranged(die_list=[D4], damage_type=DamageType.BLUDGEONING)
    weapon2 = Weapon.simple_ranged(die_list=[D4], damage_type=DamageType.BLUDGEONING, two_handed=True)
    weapon3 = Weapon.simple_ranged(die_list=[D4], damage_type=DamageType.BLUDGEONING, versatile=[D6])
    weapon4 = Weapon.simple_ranged(die_list=[D4], damage_type=DamageType.BLUDGEONING, thrown=(10, 20))

    assert weapon1 == Weapon(damage=Damage([D4], DamageType.BLUDGEONING), weapon_type=WeaponType.SIMPLE_RANGED)
    assert weapon2 == Weapon(damage=Damage([D4], DamageType.BLUDGEONING), weapon_type=WeaponType.SIMPLE_RANGED,
                             properties={WeaponProperty.TWO_HANDED: True})
    assert weapon3 == Weapon(damage=Damage([D4], DamageType.BLUDGEONING), weapon_type=WeaponType.SIMPLE_RANGED,
                             properties={WeaponProperty.VERSATILE: Damage([D6], DamageType.BLUDGEONING)})
    assert weapon4 == Weapon(damage=Damage([D4], DamageType.BLUDGEONING), weapon_type=WeaponType.SIMPLE_RANGED,
                             properties={WeaponProperty.THROWN: (10, 20)})


def test_martial_melee_weapon():
    weapon1 = Weapon.martial_melee(die_list=[D4], damage_type=DamageType.BLUDGEONING)
    weapon2 = Weapon.martial_melee(die_list=[D4], damage_type=DamageType.BLUDGEONING, two_handed=True)
    weapon3 = Weapon.martial_melee(die_list=[D4], damage_type=DamageType.BLUDGEONING, versatile=[D6])
    weapon4 = Weapon.martial_melee(die_list=[D4], damage_type=DamageType.BLUDGEONING, thrown=(10, 20))

    assert weapon1 == Weapon(damage=Damage([D4], DamageType.BLUDGEONING), weapon_type=WeaponType.MARTIAL_MELEE)
    assert weapon2 == Weapon(damage=Damage([D4], DamageType.BLUDGEONING), weapon_type=WeaponType.MARTIAL_MELEE,
                             properties={WeaponProperty.TWO_HANDED: True})
    assert weapon3 == Weapon(damage=Damage([D4], DamageType.BLUDGEONING), weapon_type=WeaponType.MARTIAL_MELEE,
                             properties={WeaponProperty.VERSATILE: Damage([D6], DamageType.BLUDGEONING)})
    assert weapon4 == Weapon(damage=Damage([D4], DamageType.BLUDGEONING), weapon_type=WeaponType.MARTIAL_MELEE,
                             properties={WeaponProperty.THROWN: (10, 20)})


def test_martial_ranged_weapon():
    weapon1 = Weapon.martial_ranged(die_list=[D4], damage_type=DamageType.BLUDGEONING)
    weapon2 = Weapon.martial_ranged(die_list=[D4], damage_type=DamageType.BLUDGEONING, two_handed=True)
    weapon3 = Weapon.martial_ranged(die_list=[D4], damage_type=DamageType.BLUDGEONING, versatile=[D6])
    weapon4 = Weapon.martial_ranged(die_list=[D4], damage_type=DamageType.BLUDGEONING, thrown=(10, 20))

    assert weapon1 == Weapon(damage=Damage([D4], DamageType.BLUDGEONING), weapon_type=WeaponType.MARTIAL_RANGED)
    assert weapon2 == Weapon(damage=Damage([D4], DamageType.BLUDGEONING), weapon_type=WeaponType.MARTIAL_RANGED,
                             properties={WeaponProperty.TWO_HANDED: True})
    assert weapon3 == Weapon(damage=Damage([D4], DamageType.BLUDGEONING), weapon_type=WeaponType.MARTIAL_RANGED,
                             properties={WeaponProperty.VERSATILE: Damage([D6], DamageType.BLUDGEONING)})
    assert weapon4 == Weapon(damage=Damage([D4], DamageType.BLUDGEONING), weapon_type=WeaponType.MARTIAL_RANGED,
                             properties={WeaponProperty.THROWN: (10, 20)})
