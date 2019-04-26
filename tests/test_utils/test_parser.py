import json

from dnd.models.feat import Resistance, Vulnerability
from dnd.utils.parsers import get_feat_list


def test_get_feat_list_from_string():
    with open('tests/resources/feats.json') as json_file:
        json_dict = json.load(json_file)

    assert get_feat_list(json_dict) == [Resistance('Piercing'), Resistance('Bludgeoning'), Vulnerability('Cold')]
