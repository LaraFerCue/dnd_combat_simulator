from dnd.models.die import D10
from dnd.models.spell import Spell


def test_spell():
    spell = Spell([D10])

    for _ in range(0, 5000):
        assert spell.get_damage() in range(1, 11)
