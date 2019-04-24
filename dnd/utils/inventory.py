from dnd.models.armor import Armor, ArmorType
from dnd.models.damage import DamageType
from dnd.models.die import D4, D8, D6, D10, D12, Die
from dnd.models.weapon import Weapon

PADDED_ARMOR = Armor(11, ArmorType.LIGHT)
LEATHER_ARMOR = Armor(11, ArmorType.LIGHT)
STUDDED_ARMOR = Armor(12, ArmorType.LIGHT)

HIDE_ARMOR = Armor(12, ArmorType.MEDIUM)
CHAIN_SHIRT_ARMOR = Armor(13, ArmorType.MEDIUM)
SCALE_MAIL_ARMOR = Armor(14, ArmorType.MEDIUM)
BREATPLATE_ARMOR = Armor(14, ArmorType.MEDIUM)
HALF_PLATE_ARMOR = Armor(15, ArmorType.MEDIUM)

RING_MAIL_ARMOR = Armor(14, ArmorType.HEAVY)
CHAIN_MAIL_ARMOR = Armor(16, ArmorType.HEAVY)
SPLINT_ARMOR = Armor(17, ArmorType.HEAVY)
PLATE_ARMOR = Armor(18, ArmorType.HEAVY)

# Simple Melee Weapons
CLUB_WEAPON = Weapon.simple_melee(die_list=[D4], damage_type=DamageType.BLUDGEONING, light=True)
DAGGER_WEAPON = Weapon.simple_melee(die_list=[D4], damage_type=DamageType.PIERCING, light=True,
                                    finesse=True, thrown=(20, 60))
GREATCLUB_WEAPON = Weapon.simple_melee(die_list=[D8], damage_type=DamageType.BLUDGEONING, two_handed=True)
HANDAXE_WEAPON = Weapon.simple_melee(die_list=[D6], damage_type=DamageType.SLASHING, light=True, thrown=(20, 60))
JAVELIN_WEAPON = Weapon.simple_melee(die_list=[D6], damage_type=DamageType.PIERCING, thrown=(30, 120))
LIGHT_HAMMER_WEAPON = Weapon.simple_melee(die_list=[D4], damage_type=DamageType.BLUDGEONING, thrown=(20, 60),
                                          light=True)
MACE_WEAPON = Weapon.simple_melee(die_list=[D6], damage_type=DamageType.BLUDGEONING)
QUARTERSTAFF_WEAPON = Weapon.simple_melee(die_list=[D6], damage_type=DamageType.BLUDGEONING, versatile=[D8])
SICKLE_WEAPON = Weapon.simple_melee(die_list=[D4], damage_type=DamageType.SLASHING, light=True)
SPEAR_WEAPON = Weapon.simple_melee(die_list=[D6], damage_type=DamageType.PIERCING, thrown=(20, 60),
                                   versatile=[D8])

# Simple Ranged Weapons
LIGHT_CROSSBOW_WEAPON = Weapon.simple_ranged(die_list=[D8], damage_type=DamageType.PIERCING,
                                             ammunition=(80, 320),
                                             loading=True, two_handed=True)
DART_WEAPON = Weapon.simple_ranged(die_list=[D4], damage_type=DamageType.PIERCING, thrown=(20, 60), finesse=True)
SHORTBOW_WEAPON = Weapon.simple_ranged(die_list=[D6], damage_type=DamageType.PIERCING, two_handed=True,
                                       ammunition=(80, 320))
SLING_WEAPON = Weapon.simple_ranged(die_list=[D4], damage_type=DamageType.BLUDGEONING, ammunition=(30, 120))

# Martial Melee Weapons
BATTLEAXE_WEAPON = Weapon.martial_melee(die_list=[D8], damage_type=DamageType.SLASHING, versatile=[D10])
FLAIL_WEAPON = Weapon.martial_melee(die_list=[D8], damage_type=DamageType.BLUDGEONING)
GLAIVE_WEAPON = Weapon.martial_melee(die_list=[D10], damage_type=DamageType.SLASHING, heavy=True, two_handed=True,
                                     reach=True)
GREATAXE_WEAPON = Weapon.martial_melee(die_list=[D12], damage_type=DamageType.SLASHING, heavy=True, two_handed=True)
GREATSWORD_WEAPON = Weapon.martial_melee(die_list=[D6, D6], damage_type=DamageType.SLASHING, heavy=True,
                                         two_handed=True)
HALBERD_WEAPON = Weapon.martial_melee(die_list=[D10], damage_type=DamageType.SLASHING, heavy=True, two_handed=True,
                                      reach=True)
LANCE_WEAPON = Weapon.martial_melee(die_list=[D12], damage_type=DamageType.PIERCING, special=True, reach=True)
LONGSWORD_WEAPON = Weapon.martial_melee(die_list=[D8], damage_type=DamageType.SLASHING, versatile=[D10])
MAUL_WEAPON = Weapon.martial_melee(die_list=[D6, D6], damage_type=DamageType.BLUDGEONING, heavy=True, two_handed=True)
MORNING_STAR_WEAPON = Weapon.martial_melee(die_list=[D8], damage_type=DamageType.PIERCING)
PIKE_WEAPON = Weapon.martial_melee(die_list=[D10], damage_type=DamageType.PIERCING, two_handed=True, heavy=True,
                                   reach=True)
RAPIER_WEAPON = Weapon.martial_melee(die_list=[D8], damage_type=DamageType.PIERCING, finesse=True)
SCIMITAR_WEAPON = Weapon.martial_melee(die_list=[D6], damage_type=DamageType.SLASHING, finesse=True, light=True)
SHORTSWORD_WEAPON = Weapon.martial_melee(die_list=[D6], damage_type=DamageType.SLASHING, finesse=True, light=True)
TRIDENT_WEAPON = Weapon.martial_melee(die_list=[D6], damage_type=DamageType.PIERCING, thrown=(20, 60), versatile=[D8])
WAR_PICK_WEAPON = Weapon.martial_melee(die_list=[D8], damage_type=DamageType.PIERCING)
WARHAMMER_WEAPON = Weapon.martial_melee(die_list=[D8], damage_type=DamageType.BLUDGEONING, versatile=[D10])
WHIP_WEAPON = Weapon.martial_melee(die_list=[D4], damage_type=DamageType.SLASHING, finesse=True, reach=True)

# Martial Ranged Weapons
BLOWGUN_WEAPON = Weapon.martial_ranged(die_list=[Die(1)], damage_type=DamageType.PIERCING, ammunition=(25, 100),
                                       loading=True)
HAND_CROSSBOW_WEAPON = Weapon.martial_ranged(die_list=[D6], damage_type=DamageType.PIERCING, ammunition=(30, 120),
                                             loading=True, light=True)
HEAVY_CROSSBOW_WEAPON = Weapon.martial_ranged(die_list=[D10], damage_type=DamageType.PIERCING, ammunition=(100, 400),
                                              heavy=True, loading=True, two_handed=True)
LONGBOW_WEAPON = Weapon.martial_ranged(die_list=[D8], damage_type=DamageType.PIERCING, ammunition=(150, 600),
                                       heavy=True,
                                       two_handed=True)
NET_WEAPON = Weapon.martial_ranged(die_list=[], damage_type=DamageType.BLUDGEONING, special=True, thrown=(5, 15))
