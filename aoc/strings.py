from typing import Optional


def parse_ints_split(s: str, sep: Optional[str] = None) -> list[int]:
    return [int(x) for x in s.split(sep)]


def parse_ints_comma(s: str) -> list[int]:
    return parse_ints_split(s, sep=",")
