from __future__ import annotations

import argparse
import pathlib

import pytest

import aoc

INPUT_TXT = pathlib.Path(__file__) / "input.txt"

CYCLES = [20, 60, 100, 140, 180, 220]


class Computer:
    def __init__(self, program) -> None:
        self.program = program
        self.x = 1
        self.cycle = 0
        self.signal_strengths = []

    def run(self):
        for command in self.program:
            parts = command.split()
            for part in parts:
                self.signal_strengths.append(self.x)
                if part == "noop":
                    self.cycle += 1
                    continue
                elif part == "addx":
                    self.cycle += 1
                    continue
                elif part[-1].isdigit():
                    self.addx(int(part))
                    self.cycle += 1

        self.signal_strengths.append(self.x)

    def addx(self, value: int):
        self.x += value


def compute(string_: str) -> int:
    lines = string_.splitlines()
    computer = Computer(lines)
    computer.run()
    print("\n")

    top = 40
    for i in range(0, 6):
        for curr_pixel in range(0, top):
            cycle = top * i + curr_pixel
            signal = computer.signal_strengths[cycle]
            sprite_range = [signal - 1, signal, signal + 1]
            char = ". "

            if curr_pixel in sprite_range:
                char = "# "
            print(char, end="")
            if curr_pixel == 39:
                print("\n")


INPUT_S = """\
addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop
"""
EXPECTED = 13140


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
