import sys
from typing import Generator, List, Union
import timeit

import requests

SERVICE_URL = "95.165.90.137:9236/api/random_strings"

NestedListStr = Union[str, List["NestedListStr"]]


def string_generator(nested_list: NestedListStr) -> Generator[str, None, None]:
    """
    A recursive generator that straightens arrays of random nesting.
    Args:
        nested_list (NestedListStr): an array of random nesting.
    Yields:
        Generator[str, None, None]: the next element in a straightened array.
    """
    for element in nested_list:
        if isinstance(element, list):
            yield from string_generator(element)
        else:
            yield element


if __name__ == "__main__":
    for strings_num in [10, 1000, 100000]:
        url = f"{SERVICE_URL}/{strings_num}"
        res = requests.get(url).json()
        strings = res["strings"]

        list_container = [string for string in string_generator(strings)]
        set_container = {string for string in string_generator(strings)}

        list_time_taken = sys.getsizeof(list_container)
        set_time_taken = sys.getsizeof(set_container)

        print(f"{list_time_taken} {set_time_taken}")

        list_time_taken = timeit.timeit(
            "[string for string in string_generator(strings)]",
            setup="from __main__ import string_generator",
            number=10,
        )
        set_time_taken = timeit.timeit(
            "{string for string in string_generator(strings)}",
            setup="from __main__ import string_generator",
            number=10,
        )

        print(f"{list_time_taken / 10:.3f} {set_time_taken / 10:.3f}")
