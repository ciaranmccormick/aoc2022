from __future__ import annotations

import argparse
import pathlib

import pytest

import aoc

INPUT_TXT = pathlib.Path(__file__) / "input.txt"


def compute(s: str) -> int:
    calories = []
    count = 0
    for entry in s.split("\n"):
        if entry == "":
            calories.append(count)
            count = 0
        else:
            count += int(entry)

    return sum(sorted(calories)[-3:])


INPUT_S = """\
1000
2000
3000

4000

5000
6000

7000
8000
9000

10000
"""
EXPECTED = 45000


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
