import pytest

from project_time_allocation.core.engine.utils import dict_from_lists


def test_dict_from_lists():
    list_1 = [1, 2, 3, 4, 5]
    list_2 = [11, 12, 13, 14, 15]
    dict_out = dict_from_lists(list_keys=list_1, list_values=list_2)
    keys = list(dict_out.keys())
    values = list(dict_out.values())
    assert list_1 == keys
    assert list_2 == values
