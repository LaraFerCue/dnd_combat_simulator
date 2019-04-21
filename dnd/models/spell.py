from dnd.models.damage import Damage


class Spell:
    def __init__(self, damage: Damage):
        self.__damage = damage

    def get_damage(self) -> int:
        return self.__damage.get_damage()
