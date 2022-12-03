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
        if code in ("A", "X"):
            return cls.ROCK
        elif code in ("B", "Y"):
            return cls.PAPER
        else:
            return cls.SCISSOR


class Result(enum.Enum):
    WIN = 6
    DRAW = 3
    LOST = 0


OUTCOMES = {
    (Hand.ROCK, Hand.PAPER): "WIN",
    (Hand.ROCK, Hand.SCISSOR): "LOST",
    (Hand.PAPER, Hand.ROCK): "LOST",
    (Hand.PAPER, Hand.SCISSOR): "WIN",
    (Hand.SCISSOR, Hand.PAPER): "LOST",
    (Hand.SCISSOR, Hand.ROCK): "WIN",
}


def compute(string: str) -> int:
    total = 0
    lines = string.splitlines()
    for line in lines:
        elf, you = line.split(" ")
        elf_hand = Hand.from_code(elf)
        your_hand = Hand.from_code(you)
        result = Result[OUTCOMES.get((elf_hand, your_hand), "DRAW")]
        total += result.value + Hand.from_code(you).value

    return total


INPUT_S = """\
A Y
B X
C Z
"""
EXPECTED = 15


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
