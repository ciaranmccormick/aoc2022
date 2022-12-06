from __future__ import annotations

import argparse
import pathlib
import re
from collections import defaultdict
from dataclasses import dataclass

import pytest

INPUT_TXT = pathlib.Path(__file__) / "input.txt"

STACKS = defaultdict(list)


@dataclass()
class Move:
    quantity: int
    start: int
    end: int

    @classmethod
    def from_str(cls, string_: str):
        split = string_.split(" ")
        q = split[1]
        s = split[3]
        e = split[5]
        return cls(int(q), int(s), int(e))


def perform_move(move: Move):
    start = STACKS[move.start]
    end = STACKS[move.end]
    for _ in range(0, move.quantity):
        end.insert(0, start.pop(0))


def parse_crate(str_: str):
    chunk = 4
    for i in range(0, len(str_) - 1, 4):
        end = i + chunk
        if match := re.findall(r"\[(.)\]", str_[i:end]):
            STACKS[1 + i // chunk] += match

    return str_[1]


def compute(string_: str) -> str:
    lines = string_.splitlines()
    moves = []
    for line in lines:
        if line.startswith("move"):
            moves.append(Move.from_str(line))
        elif line == "":
            continue
        else:
            parse_crate(line)

    for m in moves:
        perform_move(m)

    chars = []
    for i in range(1, len(STACKS) + 1):
        chars.append(STACKS[i][0])

    return "".join(chars)


INPUT_S = """\
    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
"""
EXPECTED = "CMZ"


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
