import logging
from pathlib import Path

from dnd.utils.file_utils import create_weapon_from_json_file, \
    create_armor_from_json_file
from dnd.utils.parsers import MalformedWeaponProperties

log = logging.getLogger('inventory_checker')
log.setLevel(logging.DEBUG)

try:
    for weapon_json_file in Path('weapons').iterdir():
        try:
            create_weapon_from_json_file(weapon_json_file)
        except MalformedWeaponProperties as exception:
            log.exception(exception)
    for armor_json_file in Path('armors').iterdir():
        try:
            create_armor_from_json_file(armor_json_file)
        except MalformedWeaponProperties as exception:
            log.exception(exception)
except OSError as exception:
    log.exception(exception)
