import pytest

from dnd.models.damage import DamageType, Damage
from dnd.models.die import D10, D12
from dnd.models.spell import Spell, SpellWornOut


def test_spell():
    spell = Spell(Damage([D10], DamageType.MAGIC_ACID))

    for _ in range(0, 5000):
        assert spell.get_damage() in range(1, 11)


def test_compare_spells():
    spell1 = Spell(Damage([D10], DamageType.MAGIC_ACID))
    spell2 = Spell(Damage([D10], DamageType.MAGIC_ACID))
    spell3 = Spell(Damage([D12], DamageType.MAGIC_ACID))
    spell4 = Spell(Damage([D12], DamageType.MAGIC_COLD))
    spell5 = Spell(Damage([D10], DamageType.MAGIC_COLD))

    assert spell1 == spell2
    assert spell1 != spell3
    assert spell1 != spell4
    assert spell1 != spell5


def test_high_level_spells():
    spell1 = Spell(Damage([D10], DamageType.MAGIC_COLD), spell_lvl=1)
    spell1.slots = 1

    assert spell1.get_damage() in range(1, 11)
    with pytest.raises(SpellWornOut):
        spell1.get_damage()
    assert spell1.times_used == 1
