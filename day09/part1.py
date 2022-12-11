from __future__ import annotations

import argparse
import pathlib
from dataclasses import dataclass

import pytest

import aoc

INPUT_TXT = pathlib.Path(__file__) / "input.txt"

Positions = dict[tuple[int, int], int]
RIGHT = "R"
LEFT = "L"
UP = "U"
DOWN = "D"


@dataclass()
class Move:
    direction: str
    magnitude: int

    @classmethod
    def from_str(cls, s: str):
        d, m = s.split(" ")
        return cls(d, int(m))


class Knot:
    def __init__(self) -> None:
        self.x: int = 0
        self.y: int = 0
        self.positions: Positions = {self.current_position: True}

    @property
    def current_position(self) -> tuple[int, int]:
        return (self.x, self.y)

    def record_position(self):
        self.positions[self.current_position] = True

    def right(self):
        self.x += 1

    def left(self):
        self.x -= 1

    def up(self):
        self.y += 1

    def down(self):
        self.y -= 1

    def is_adjacent(self, other: "Knot") -> bool:
        if abs(self.x - other.x) > 1:
            return False

        if abs(self.y - other.y) > 1:
            return False
        return True

    def move_towards(self, other: "Knot"):
        if other.x - self.x > 0:
            self.x += 1
        elif other.x - self.x < 0:
            self.x -= 1

        if other.y - self.y > 0:
            self.y += 1
        elif other.y - self.y < 0:
            self.y -= 1

        self.record_position()

    def same_y(self, other: "Knot"):
        return self.y == other.y

    def same_x(self, other: "Knot"):
        return self.x == other.x

    def perform_move(self, move: str):
        if move == RIGHT:
            self.right()
        elif move == LEFT:
            self.left()
        elif move == UP:
            self.up()
        elif move == DOWN:
            self.down()

        self.record_position()

    def follow(self, other):
        if self.same_y(other) and self.x - other.x < 1:
            self.perform_move(RIGHT)
        elif self.same_y(other) and self.x - other.x > 1:
            self.perform_move(LEFT)
        elif self.same_x(other) and self.y - other.y < 1:
            self.perform_move(UP)
        elif self.same_x(other) and self.y - other.y > 1:
            self.perform_move(DOWN)
        elif not self.same_x(other) and not self.same_y(other):
            self.move_towards(other)


class Grid:
    def __init__(self) -> None:
        self.head: Knot = Knot()
        self.tail: Knot = Knot()

    def perform_move(self, move):
        for _ in range(move.magnitude):
            self.head.perform_move(move.direction)
            if not self.tail.is_adjacent(self.head):
                self.tail.follow(self.head)


def compute(string_: str) -> int:
    lines = string_.splitlines()
    moves = [Move.from_str(line) for line in lines]
    grid = Grid()

    for move in moves:
        grid.perform_move(move)
    return len(grid.tail.positions)


INPUT_S = """\
R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2
"""
EXPECTED = 13


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
