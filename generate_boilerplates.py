from argparse import ArgumentParser
from dataclasses import dataclass
from datetime import datetime
from os import linesep
from pathlib import Path
from typing import NoReturn


README_FILENAME = "README.md"
INPUT_FILE = "input.txt"
RESULT_FILE = "result.txt"
MAIN_FILE = "main.py"
main_file_content = f"""
from pathlib import Path

INPUT_FILE = "{INPUT_FILE}"
RESULT_FILE = "{RESULT_FILE}"


def read_input():
    \"""Read input from file\"""
    input_file = Path(__file__).parent / INPUT_FILE
    raise NotImplementedError


def write_result(data: str):
    \"""Write results to a file\"""
    result_file = Path(__file__).parent / RESULT_FILE
    raise NotImplementedError


def main():
    \"""Solve the puzzle\"""
    raise NotImplementedError


if __name__ == "__main__":
    main()"""

DEFAULT_PATH = Path(".")
DEFAULT_YEAR = datetime.now().year
DEFAULT_DAYS_PER_EVENT = 25
DEFAULT_PUZZLES_PER_DAY = 2


@dataclass
class UserInput:
    path: Path
    years: list[int]
    days_count: int
    puzzles_count: int


@dataclass
class UserInputCLI(UserInput):
    pass


def run_cli() -> UserInputCLI:
    parser = ArgumentParser()

    parser.add_argument(
        "-p",
        "--path",
        type=Path,
        default=DEFAULT_PATH,
        help=f"Path to wherever you want the templates to be created. Default: '{DEFAULT_PATH}'",
    )

    parser.add_argument(
        "-d",
        "--days-count",
        type=int,
        default=DEFAULT_DAYS_PER_EVENT,
        help=f"For how many days does the events run for. Default : '{DEFAULT_DAYS_PER_EVENT}'",
    )

    parser.add_argument(
        "-z",
        "--puzzles-count",
        type=int,
        default=DEFAULT_PUZZLES_PER_DAY,
        help=f"Puzzles per day. Default: '{DEFAULT_PUZZLES_PER_DAY}'",
    )

    parser.add_argument(
        "years",
        nargs="*",
        type=int,
        default=[DEFAULT_YEAR],
        help=f"For which years should the templates be generated. Default: '{DEFAULT_YEAR}'",
    )

    args = vars(parser.parse_args())

    return UserInputCLI(**args)


def add_line_break(line: str) -> str:
    return f"{line}{linesep}"


def create_file_if_not_exist(file: Path, *lines: list[str]) -> NoReturn:
    if not file.exists():
        with open(file, "w") as f:
            f.writelines(map(add_line_break, lines))


def main(user_input: UserInput) -> NoReturn:
    years = [user_input.path / str(year) for year in user_input.years]
    for year in years:
        days = range(1, user_input.days_count + 1)
        puzzles = [
            puzzle
            for day in days
            for puzzle in [
                f"{day:02}_{i}" for i in range(1, user_input.puzzles_count + 1)
            ]
        ]
        year.mkdir(exist_ok=True)
        create_file_if_not_exist(
            year / README_FILENAME,
            f"# {year}",
            "",
            f"Event's official website page: <https://adventofcode.com/{year}>",
            "",
            "## Puzzles",
            "",
            *[
                f"- [Day-{d.split('_')[0]} Puzzle-{d.split('_')[1]}](./{d}/{README_FILENAME})"
                for d in puzzles
            ],
        )
        for puzzle_dir in [year / p for p in puzzles]:
            puzzle_dir.mkdir(exist_ok=True)
            create_file_if_not_exist(
                puzzle_dir / MAIN_FILE,
                f'"""Solution for for puzzle \'{puzzle_dir}\'"""',
                main_file_content,
            )
            create_file_if_not_exist(puzzle_dir / INPUT_FILE)
            create_file_if_not_exist(puzzle_dir / RESULT_FILE)
            create_file_if_not_exist(
                puzzle_dir / README_FILENAME,
                f"# {puzzle_dir}",
                "",
                "## Input",
                "",
                f"[{INPUT_FILE}](./{INPUT_FILE})",
                "",
                "## Result",
                "",
                f"[{RESULT_FILE}](./{RESULT_FILE})",
                "",
                "## Solution",
                "",
                f"[{MAIN_FILE}](./{MAIN_FILE})",
                "",
                f"[<-{year}](../{README_FILENAME})",
            )


if __name__ == "__main__":
    cli_input_data = run_cli()
    main(cli_input_data)
