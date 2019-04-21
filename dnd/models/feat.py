from dnd.models.damage import DamageType


class Feat:
    def __init__(self, name: str):
        self.__name = name

    @property
    def name(self):
        return self.__name

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
        super().__init__("Resistance")
        self.__damage_type = damage_type

    def modify_damage(self, damage: int, damage_type: DamageType) -> int:
        if damage_type == self.__damage_type:
            return int(damage / 2)
        return damage

    @staticmethod
    def from_dict(**kwargs):
        if 'damage_type' not in kwargs.keys():
            raise ValueError(f'Wrong dictionary passed for Resistance {kwargs}')
        return Resistance(damage_type=kwargs['damage_type'])
