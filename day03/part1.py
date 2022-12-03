from __future__ import annotations

import argparse
import pathlib

import pytest
from decouple import string


INPUT_TXT = pathlib.Path(__file__) / "input.txt"

mapping = dict(zip(string.ascii_lowercase + string.ascii_uppercase, range(1, 53)))


def compute(str_: str) -> int:
    misplaced_items = []
    for line in str_.splitlines():
        half_way = len(line) // 2
        diff = list(set.intersection(set(line[:half_way]), set(line[half_way:])))
        misplaced_items += diff
    return sum(mapping.get(item, 0) for item in misplaced_items)


INPUT_S = """\
vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw
"""
EXPECTED = 157


@pytest.mark.parametrize(
    ("input_s", "expected"),
    ((INPUT_S, EXPECTED),),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("data_file", nargs="?", default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f:
        print(compute(f.read()))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
