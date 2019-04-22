import pytest

from dnd.models.character import Character, Ability
from dnd.models.damage import DamageType
from dnd.models.feat import Resistance


def test_character_check_ability_negative():
    with pytest.raises(AttributeError):
        Character.check_ability(-1, Ability.CHARISMA)


def test_character_check_ability_huge():
    with pytest.raises(AttributeError):
        Character.check_ability(22, Ability.CHARISMA)


def test_character_check_ability_normal():
    Character.check_ability(15, Ability.CHARISMA)


def test_character_get_modifier():
    assert Character.get_modifier(10) == 0
    assert Character.get_modifier(9) == -1
    assert Character.get_modifier(8) == -1
    assert Character.get_modifier(11) == 0
    assert Character.get_modifier(12) == 1


def test_character_default_proficiency_value():
    assert Character(10, 10, 10, 10, 10, 10, 10).proficiency == 2


def test_character_set_proficiency_value():
    character = Character(10, 10, 10, 10, 10, 10, 10)
    character.proficiency = 3

    assert character.proficiency == 3

    with pytest.raises(AttributeError):
        character.proficiency = -2


def test_character_apply_damage():
    character = Character(10, 10, 10, 10, 10, 10, 10)
    character.apply_damage(5, DamageType.MAGIC)

    assert character.hit_points == 5


def test_character_apply_damage_with_resistance():
    character = Character(10, 10, 10, 10, 10, 10, 10)
    character.feat_list.append(Resistance(DamageType.PIERCING))

    character.apply_damage(4, DamageType.PIERCING)
    assert character.hit_points == 8
    character.apply_damage(4, DamageType.MAGIC)
    assert character.hit_points == 4
