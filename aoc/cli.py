import re
import sys

import typer

from aoc.utils import (
    _post_answer,
    get_current_day,
    get_input,
    print_failure,
    print_sample,
    print_success,
)

RIGHT = "That's the right answer!"
TOO_QUICK = re.compile("You gave an answer too recently.*to wait.")
WRONG = re.compile(r"That's not the right answer.*?\.")
ALREADY_DONE = re.compile(r"You don't seem to be solving.*\?")
ERRORS = (WRONG, TOO_QUICK, ALREADY_DONE)


app = typer.Typer()


@app.command()
def download_input() -> int:
    year, day = get_current_day()

    input_str = get_input(year, day)

    with open("input.txt", "w") as f:
        f.write(input_str)

    print_sample(input_str)
    return 0


@app.command()
def submit(part: int = typer.Option(...)) -> int:
    year, day = get_current_day()
    answer = int(sys.stdin.read())

    print(f"answer: {answer}")
    response = _post_answer(year, day, part, answer)

    for error_regex in ERRORS:
        error_match = error_regex.search(response)
        if error_match:
            print_failure(error_match[0])
            return 1

    if RIGHT in response:
        print_success(RIGHT)
        return 0
    else:
        print(response)
        return 1


if __name__ == "__main__":
    app()
