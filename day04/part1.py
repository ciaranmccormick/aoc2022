from __future__ import annotations

import argparse
import pathlib
from typing import Set

import pytest

INPUT_TXT = pathlib.Path(__file__) / "input.txt"


def to_set(r: list[int]) -> Set[int]:
    return set(range(r[0], r[1] + 1))


def string_to_set(str_: str):
    return to_set([int(i) for i in str_.split("-")])


def intersects(pair: str) -> bool:
    first, second = pair.split(",")
    first_s = string_to_set(first)
    second_s = string_to_set(second)
    intersection = first_s.intersection(second_s)
    return len(intersection) == len(first_s) or len(intersection) == len(second_s)


def compute(string_: str) -> int:
    return sum(intersects(pair) for pair in string_.splitlines())


INPUT_S = """\
2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8
"""
EXPECTED = 2


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
