from dnd.models.armor import Armor, ArmorType


def test_light_armor_without_shield():
    light_armor = Armor(12, ArmorType.LIGHT)

    for modifier in range(-5, 6):
        assert light_armor.get_armor_class(modifier) == 12 + modifier


def test_light_armor_with_shield():
    light_armor = Armor(12, ArmorType.LIGHT)

    for modifier in range(-5, 6):
        assert light_armor.get_armor_class(modifier, True) == 14 + modifier


def test_medium_armor_without_shield():
    medium_armor = Armor(12, ArmorType.MEDIUM)

    for modifier in range(-5, 6):
        assert medium_armor.get_armor_class(modifier) == 12 + min(modifier, 2)


def test_medium_armor_with_shield():
    medium_armor = Armor(12, ArmorType.MEDIUM)

    for modifier in range(-5, 6):
        assert medium_armor.get_armor_class(modifier, True) == 14 + min(modifier, 2)


def test_heavy_armor_without_shield():
    heavy_armor = Armor(18, ArmorType.HEAVY)

    for modifier in range(-5, 6):
        assert heavy_armor.get_armor_class(modifier) == 18


def test_heavy_armor_with_shield():
    heavy_armor = Armor(18, ArmorType.HEAVY)

    for modifier in range(-5, 6):
        assert heavy_armor.get_armor_class(modifier, True) == 20
