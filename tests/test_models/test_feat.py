from dnd.models.damage import DamageType
from dnd.models.feat import Feat, Resistance, Vulnerability


def test_get_feat_by_name():
    feat = Feat.get_feat_by_name(name='Resistance', damage_type=DamageType.PIERCING)
    assert feat.name == "Resistance"


def test_resistance():
    resistance = Resistance(DamageType.PIERCING)

    assert resistance.modify_damage(10, DamageType.PIERCING) == 5
    assert resistance.modify_damage(10, DamageType.MAGIC_ACID) == 10


def test_vulnerability():
    vulnerability = Vulnerability(DamageType.PIERCING)

    assert vulnerability.modify_damage(10, DamageType.PIERCING) == 20
    assert vulnerability.modify_damage(10, DamageType.MAGIC_ACID) == 10


def test_equal_feats():
    feat1 = Resistance(DamageType.PIERCING)
    feat2 = Resistance(DamageType.PIERCING)

    assert feat1 == feat2


def test_different_feats():
    feat1 = Resistance(DamageType.PIERCING)
    feat2 = Resistance(DamageType.BLUDGEONING)
    feat3 = Vulnerability(DamageType.PIERCING)
    feat4 = Vulnerability(DamageType.BLUDGEONING)

    assert feat1 != feat2
    assert feat1 != feat3
    assert feat1 != feat4
    assert feat2 != feat3
    assert feat2 != feat4
    assert feat3 != feat4
