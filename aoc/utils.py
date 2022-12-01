from pathlib import Path

import httpx
from decouple import AutoConfig

config = AutoConfig(search_path=Path(__file__).parent.parent)


def print_success(msg: str) -> None:
    print(f"\033[42m{msg}\033[m")


def print_failure(msg: str) -> None:
    print(f"\033[41m{msg}\033[m")


def _get_headers() -> dict[str, str]:
    session = config("SESSION")
    print(f"Current session={session}")
    return {"Cookie": f"session={session}"}


def get_input(year: int, day: int) -> str:
    url = f"https://adventofcode.com/{year}/day/{day}/input"
    resp = httpx.get(url, headers=_get_headers())
    return resp.text


def get_current_day() -> tuple[int, int]:
    cwd = Path.cwd()
    day = cwd.name
    year = cwd.parent.name

    if not day.startswith("day") or not year.startswith("aoc"):
        raise AssertionError(f"weird cwd dir: {cwd}")

    return int(year.replace("aoc", "")), int(day.replace("day", ""))


def print_sample(s: str) -> None:
    lines = s.splitlines()

    if len(lines) > 10:
        for line in lines[:10]:
            print(line)
        print("...")
    else:
        print(lines[0][:80])
        print("...")


def _post_answer(year: int, day: int, part: int, answer: int) -> str:
    data = {"answer": answer, "level": part}
    url = f"https://adventofcode.com/{year}/day/{day}/answer"
    resp = httpx.post(url, data=data, headers=_get_headers())
    return resp.text
