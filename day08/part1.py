from __future__ import annotations

import argparse
import pathlib

import pytest

import aoc

INPUT_TXT = pathlib.Path(__file__) / "input.txt"


def compute(string_: str) -> int:
    lines = string_.splitlines()
    cover = []
    for line in lines:
        cover.append([int(i) for i in line])

    visible = 0
    rows = len(lines)
    cols = len(lines[0])
    for i in range(1, rows - 1):
        for j in range(1, cols - 1):
            tree = cover[i][j]

            left = cover[i][0:j]
            right = cover[i][j + 1 :]
            top = [cover[r][j] for r in range(i)]
            bottom = [cover[r][j] for r in range(rows - 1, i, -1)]
            # 122212201111221321022211311332344223042233341324332523523451325341142120141122414312310331033122112
            if not bottom:
                breakpoint()


            if max(left) < tree:
                visible += 1
                continue

            if max(right) < tree:
                visible += 1
                continue

            if max(top) < tree:
                visible += 1
                continue

            if max(bottom) < tree:
                visible += 1
                continue

    return visible + 2 * rows + 2 * (cols - 2)


INPUT_S = """\
30373
25512
65332
33549
35390
"""
EXPECTED = 21


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
