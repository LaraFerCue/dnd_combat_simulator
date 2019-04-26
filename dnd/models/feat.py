from enum import Enum
from typing import Union

from dnd.models.damage import DamageType


class FeatType(Enum):
    NONE = "None"
    RESISTANCE = "Resistance"


class Feat:
    def __init__(self, name: str, feat_type: FeatType = FeatType.NONE):
        self.__name = name
        self.__type = feat_type

    def __hash__(self):
        return hash(self.name) + hash(self.feat_type.value)

    @property
    def name(self):
        return self.__name

    @property
    def feat_type(self) -> FeatType:
        return self.__type

    @staticmethod
    def get_feat_by_name(name: str, **kwargs):
        module = getattr(getattr(__import__('dnd'), 'models'), 'feat')
        feat = getattr(module, name)
        return feat(**kwargs)

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __ne__(self, other):
        return not self == other

    def __gt__(self, other):
        return hash(self) > hash(other)

    def __lt__(self, other):
        return hash(self) < hash(other)

    def __le__(self, other):
        return self < other or self == other

    def __ge__(self, other):
        return self > other or self == other


class Resistance(Feat):
    def __init__(self, damage_type: Union[DamageType, str]):
        super().__init__("Resistance", FeatType.RESISTANCE)
        if isinstance(damage_type, str):
            damage_type = DamageType(damage_type)
        self.__damage_type = damage_type

    def __hash__(self):
        return hash(self.name) + hash(self.feat_type.value) + hash(self.damage_type.value)

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


class Vulnerability(Feat):
    def __init__(self, damage_type: Union[str, DamageType]):
        super().__init__("Vulnerability", FeatType.RESISTANCE)
        if isinstance(damage_type, str):
            damage_type = DamageType(damage_type)
        self.__damage_type = damage_type

    def __hash__(self):
        return hash(self.name) + hash(self.feat_type.value) + hash(self.damage_type.value)

    @property
    def damage_type(self) -> DamageType:
        return self.__damage_type

    def modify_damage(self, damage: int, damage_type: DamageType) -> int:
        if damage_type == self.__damage_type:
            return int(damage * 2)
        return damage

    @staticmethod
    def from_dict(**kwargs):
        if 'damage_type' not in kwargs.keys():
            raise ValueError(f'Wrong dictionary passed for Resistance {kwargs}')
        return Resistance(damage_type=kwargs['damage_type'])
