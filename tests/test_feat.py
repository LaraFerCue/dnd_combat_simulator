from dnd.models.damage import DamageType
from dnd.models.feat import Feat, Resistance


def test_get_feat_by_name():
    feat = Feat.get_feat_by_name(name='Resistance', damage_type=DamageType.PIERCING)
    assert feat.name == "Resistance"


def test_resistance():
    resistance = Resistance(DamageType.PIERCING)

    assert resistance.modify_damage(10, DamageType.PIERCING) == 5
    assert resistance.modify_damage(10, DamageType.MAGIC) == 10
