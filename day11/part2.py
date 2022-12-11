from __future__ import annotations

import argparse
import pathlib
import re
from collections import defaultdict
from collections.abc import Callable
from dataclasses import dataclass
from math import prod

import pytest

INPUT_TXT = pathlib.Path(__file__) / "input.txt"

MONKEY = r"Monkey (\d*):"
ITEMS = r"Starting items: (.*)"
OPERATION = r"Operation: new = (.*)"
CONDITION = r"Test: divisible by (\d*)"
POSITVE = r"If true: throw to monkey (\d*)"
NEGATIVE = r"If false: throw to monkey (\d*)"


@dataclass()
class MonkeyTest:
    condition: int
    positive: int
    negative: int


@dataclass()
class Item:
    name: str
    worry_level: int

    def is_divisible(self, modulo: int):
        return self.worry_level % modulo == 0

    def update_worry_level(self, operation: str, reducer: Callable) -> None:
        _, op, right_str = operation.split(" ")

        if operation == "old * old":
            self.worry_level *= self.worry_level
        elif op == "+":
            self.worry_level += int(right_str)
        elif op == "*":
            self.worry_level *= int(right_str)

        self.worry_level = reducer(self.worry_level)


@dataclass()
class Monkey:
    number: int
    items: list[Item]
    operation: str
    test: MonkeyTest

    def add_to_items(self, item: Item) -> None:
        self.items.append(item)

    @classmethod
    def from_input(cls, lines: list[str]):
        number = int(re.findall(MONKEY, lines[0])[-1])
        items = []
        for pos, value in enumerate(re.findall(ITEMS, lines[1])[-1].split(", ")):
            items.append(
                Item(
                    name=f"{number}{pos}",
                    worry_level=int(value),
                )
            )
        operation = re.findall(OPERATION, lines[2])[-1]

        condition = int(re.findall(CONDITION, lines[3])[-1])
        positive = int(re.findall(POSITVE, lines[4])[-1])
        negative = int(re.findall(NEGATIVE, lines[5])[-1])

        return cls(
            number=number,
            items=items,
            operation=operation,
            test=MonkeyTest(condition=condition, positive=positive, negative=negative),
        )


def compute(string_: str) -> int:
    lines = string_.splitlines()
    chunk = 7
    monkeys: list[Monkey] = []
    for i in range(0, len(lines), chunk):
        end = i + chunk
        monkeys.append(Monkey.from_input(lines[i:end]))

    monkey_items = defaultdict(int)
    for i in range(10000):
        for monkey in monkeys:
            test = monkey.test
            monkey_items[monkey.number] += len(monkey.items)
            while monkey.items:
                item = monkey.items.pop(0)
                item.update_worry_level(
                    monkey.operation,
                    lambda r: r % prod([m.test.condition for m in monkeys]),
                )

                if item.is_divisible(test.condition):
                    new_monkey = monkeys[test.positive]
                else:
                    new_monkey = monkeys[test.negative]
                new_monkey.add_to_items(item)
    return prod(sorted(monkey_items.values(), reverse=True)[:2])


INPUT_S = """\
Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1
"""
EXPECTED = 2713310158


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
