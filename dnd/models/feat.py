from enum import Enum

from dnd.models.damage import DamageType


class FeatType(Enum):
    NONE = "None"
    RESISTANCE = "Resistance"


class Feat:
    def __init__(self, name: str, feat_type: FeatType = FeatType.NONE):
        self.__name = name
        self.__type = feat_type

    @property
    def name(self):
        return self.__name

    @property
    def feat_type(self) -> FeatType:
        return self.__type

    @staticmethod
    def from_dict(**kwargs):
        raise NotImplementedError

    @staticmethod
    def get_feat_by_name(name: str, **kwargs):
        module = getattr(getattr(__import__('dnd'), 'models'), 'feat')
        feat = getattr(module, name)
        return feat.from_dict(**kwargs)


class Resistance(Feat):
    def __init__(self, damage_type: DamageType):
        super().__init__("Resistance", FeatType.RESISTANCE)
        self.__damage_type = damage_type

    @property
    def damage_type(self) -> DamageType:
        return self.__damage_type

    def modify_damage(self, damage: int, damage_type: DamageType) -> int:
        if damage_type == self.__damage_type:
            return int(damage / 2)
        return damage

    @staticmethod
    def from_dict(**kwargs):
        if 'damage_type' not in kwargs.keys():
            raise ValueError(f'Wrong dictionary passed for Resistance {kwargs}')
        return Resistance(damage_type=kwargs['damage_type'])
