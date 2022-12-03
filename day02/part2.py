from __future__ import annotations

import argparse
import enum
import pathlib

import pytest


INPUT_TXT = pathlib.Path(__file__) / "input.txt"


class Hand(enum.Enum):
    ROCK = 1
    PAPER = 2
    SCISSOR = 3

    @classmethod
    def from_code(cls, code):
        if code == "A":
            return cls.ROCK
        elif code in ("B", "Y"):
            return cls.PAPER
        else:
            return cls.SCISSOR


class Result(enum.Enum):
    WIN = 6
    DRAW = 3
    LOST = 0

    @classmethod
    def from_code(cls, code: str):
        if code == "X":
            return cls.LOST
        elif code == "Y":
            return cls.DRAW
        else:
            return cls.WIN


OUTCOMES = {
    (Hand.ROCK, Result.DRAW): Hand.ROCK,
    (Hand.ROCK, Result.LOST): Hand.SCISSOR,
    (Hand.ROCK, Result.WIN): Hand.PAPER,
    (Hand.PAPER, Result.DRAW): Hand.PAPER,
    (Hand.PAPER, Result.LOST): Hand.ROCK,
    (Hand.PAPER, Result.WIN): Hand.SCISSOR,
    (Hand.SCISSOR, Result.DRAW): Hand.SCISSOR,
    (Hand.SCISSOR, Result.LOST): Hand.PAPER,
    (Hand.SCISSOR, Result.WIN): Hand.ROCK,
}


def compute(string: str) -> int:
    total = 0
    lines = string.splitlines()
    for line in lines:
        elf, you = line.split(" ")
        elf_hand = Hand.from_code(elf)
        result = Result.from_code(you)
        total += result.value + OUTCOMES[(elf_hand, result)].value

    return total


INPUT_S = """\
A Y
B X
C Z
"""
EXPECTED = 12


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
