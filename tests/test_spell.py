from dnd.models.damage import DamageType, Damage
from dnd.models.die import D10
from dnd.models.spell import Spell


def test_spell():
    spell = Spell(Damage([D10], DamageType.MAGIC))

    for _ in range(0, 5000):
        assert spell.get_damage() in range(1, 11)
