from dnd.models.damage import DamageType
from dnd.models.feat import Feat


def test_get_feat_by_name():
    feat = Feat.get_feat_by_name(name='Resistance', damage_type=DamageType.PIERCING)
    assert feat.name == "Resistance"
