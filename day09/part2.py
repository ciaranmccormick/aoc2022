from __future__ import annotations

import argparse
import pathlib
from dataclasses import dataclass

import pytest

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
    def __init__(self, name: str) -> None:
        self.name = name
        self.x: int = 0
        self.y: int = 0
        self.positions: Positions = {self.current_position: True}

    def __repr__(self) -> str:
        return f"Knot(name={self.name}, position={self.current_position})"

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
        self.knots = []
        for i in range(0, 10):
            self.knots.append(Knot(name=f"{i}"))

    def perform_move(self, move):
        head = self.knots[0]
        for _ in range(move.magnitude):
            head.perform_move(move.direction)

            for i in range(1, len(self.knots)):
                leader = self.knots[i - 1]
                follower = self.knots[i]
                if not follower.is_adjacent(leader):
                    follower.follow(leader)


def compute(string_: str) -> int:
    lines = string_.splitlines()
    moves = [Move.from_str(line) for line in lines]
    grid = Grid()

    for move in moves:
        grid.perform_move(move)
    return len(grid.knots[-1].positions)


INPUT_S = """\
R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20
"""
EXPECTED = 36


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
