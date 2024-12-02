"""Solution for for puzzle '2024/02_1'"""

from pathlib import Path

INPUT_FILE = "input.txt"
RESULT_FILE = "result.txt"
ADJACENT_DIFFER_AT_LEAST = 1
ADJACENT_DIFFER_AT_MOST = 3


def read_input() -> list[list[int]]:
    """Read input from file"""
    input_file = Path(__file__).parent / INPUT_FILE
    with open(input_file, "r") as f:
        return [list(map(int, line.strip().split())) for line in f.readlines()]


def write_result(data: str):
    """Write results to a file"""
    result_file = Path(__file__).parent / RESULT_FILE
    with open(result_file, "w") as f:
        f.write(data)


def is_ascending(ls: list[int]) -> bool:
    return ls == sorted(ls)


def is_descending(ls: list[int]) -> bool:
    return ls == sorted(ls)[::-1]


def adjacent_do_differ(ls: list[int], least: int, most: int) -> bool:
    for i in range(1, len(ls) - 1):
        difference_with_previous = abs(ls[i - 1] - ls[i])
        difference_with_next = abs(ls[i] - ls[i + 1])
        if not (
            (least <= difference_with_previous <= most)
            and (least <= difference_with_next <= most)
        ):
            return False
    else:
        return True


def is_safe(ls: list[int], least: int, most: int) -> bool:
    return (is_ascending(ls=ls) or is_descending(ls=ls)) and adjacent_do_differ(
        ls=ls, least=least, most=most
    )


def main():
    """Solve the puzzle"""
    reports = read_input()
    safe_reports = [
        is_safe(ls=report, least=ADJACENT_DIFFER_AT_LEAST, most=ADJACENT_DIFFER_AT_MOST)
        for report in reports
    ]
    write_result(str(sum(safe_reports)))


if __name__ == "__main__":
    main()
