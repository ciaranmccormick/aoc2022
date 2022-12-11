from __future__ import annotations

import argparse
import pathlib
from collections import defaultdict
from dataclasses import dataclass
from typing import Optional

import pytest

import aoc

INPUT_TXT = pathlib.Path(__file__) / "input.txt"
DIRS = {}
TOTALS = defaultdict(int)
HARD_DISK = 70000000
REQUIRED = 30000000


@dataclass()
class File:
    filetype: str
    size: Optional[int]
    name: str

    @classmethod
    def from_string(cls, line: str):
        if line.startswith("dir"):
            type_, name = line.split(" ")
            return cls(type_, None, name)
        else:
            size, name = line.split(" ")
            return cls("file", int(size), name)


@dataclass()
class Command:
    name: str
    arg: Optional[str]
    output: list[str]

    @classmethod
    def from_string(cls, str_: str):
        parts = str_.split(" ")
        if not parts[2:]:
            return cls(parts[1], None, [])
        else:
            return cls(parts[1], parts[2], [])


def compute(string_: str) -> int:
    lines = string_.splitlines()
    cwd = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("$"):
            command = Command.from_string(line)
            if command.name == "cd" and command.arg != "..":
                cwd.append(command.arg)
            elif command.name == "cd" and command.arg == "..":
                cwd.pop()
            elif command.name == "ls":
                i += 1
                continue
        else:
            f = File.from_string(line)
            DIRS[tuple(cwd) + (f.name,)] = f
        i += 1

    for path, file_ in DIRS.items():
        filepath = ""
        for node in path[:-1]:
            filepath += node + "/"
            if file_.size:
                TOTALS[filepath] += file_.size

    unused = HARD_DISK - TOTALS["//"]
    to_delete = REQUIRED - unused
    deletable = {key: value for key, value in TOTALS.items() if value >= to_delete}
    return min(deletable.items(), key=lambda d: d[1])[1]


INPUT_S = """\
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
"""
EXPECTED = 24933642


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
