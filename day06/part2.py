from __future__ import annotations

import argparse
import pathlib

import pytest

import aoc

INPUT_TXT = pathlib.Path(__file__) / "input.txt"


def compute(string_: str) -> int:
    line = string_.splitlines()[0]
    i = 0
    chunk = 14
    while True:
        end = i + chunk
        substream = line[i:end]
        if len(set(substream)) == len(substream):
            return i + chunk
        i += 1


INPUT_S = """\
mjqjpqmgbljsphdztnvjfqwrcgsmlb
"""
EXPECTED = 19


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
