from __future__ import annotations

import argparse
import pathlib

import pytest

import aoc

INPUT_TXT = pathlib.Path(__file__) / "input.txt"


def scenic_score(tree_height, other_trees):
    count = 0
    i = 0
    while i < len(other_trees):
        count += 1
        if other_trees[i] >= tree_height:
            break
        i += 1
    return count


def compute(string_: str) -> int:
    lines = string_.splitlines()
    cover = []
    for line in lines:
        cover.append([int(i) for i in line])

    visible = 0
    max_scenic_score = -1
    rows = len(lines)
    cols = len(lines[0])
    for i in range(1, rows - 1):
        for j in range(1, cols - 1):
            tree = cover[i][j]

            left = cover[i][0:j]
            right = cover[i][j + 1 :]
            top = [cover[r][j] for r in range(i)]
            bottom = [cover[r][j] for r in range(rows - 1, i, -1)]

            left_score = scenic_score(tree, list(reversed(left)))
            right_score = scenic_score(tree, right)
            top_score = scenic_score(tree, list(reversed(top)))
            bottom_score = scenic_score(tree, list(reversed(bottom)))

            sum_score = left_score * right_score * top_score * bottom_score
            if sum_score > max_scenic_score:
                max_scenic_score = sum_score

    return max_scenic_score


INPUT_S = """\
30373
25512
65332
33549
35390
"""
EXPECTED = 8


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
