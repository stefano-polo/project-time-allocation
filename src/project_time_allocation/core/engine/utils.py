from typing import List, Union


def dict_from_lists(
    list_keys: List[Union[int, str]], list_values: List[Union[int, float, str]]
):
    return dict(zip(list_keys, list_values))
