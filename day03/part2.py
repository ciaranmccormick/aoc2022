from __future__ import annotations

import argparse
import pathlib

import pytest
from decouple import string

INPUT_TXT = pathlib.Path(__file__) / "input.txt"

mapping = dict(zip(string.ascii_lowercase + string.ascii_uppercase, range(1, 53)))


def compute(str_: str) -> int:
    ruck_sacks = str_.splitlines()
    shared = []
    chunk = 3
    for i in range(0, len(ruck_sacks), chunk):
        end = i + chunk
        shared += set.intersection(*[set(sacks) for sacks in ruck_sacks[i:end]])
    return sum(mapping.get(share, 0) for share in shared)


INPUT_S = """\
vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw
"""
EXPECTED = 70


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
