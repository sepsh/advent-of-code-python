"""Solution for for puzzle '2024/02_2'"""

from pathlib import Path

INPUT_FILE = "input.txt"
RESULT_FILE = "result.txt"
ADJACENT_DIFFER_AT_LEAST = 1
ADJACENT_DIFFER_AT_MOST = 3
MARGIN_FOR_ERROR = 1


def read_input():
    """Read input from file"""
    input_file = Path(__file__).parent / INPUT_FILE
    with open(input_file, "r") as f:
        return [list(map(int, line.strip().split())) for line in f.readlines()]


def write_result(data: str):
    """Write results to a file"""
    result_file = Path(__file__).parent / RESULT_FILE
    with open(result_file, "w") as f:
        f.write(data)


def is_ascending(ls: list[int], margin_for_error: int = 0) -> bool:
    if margin_for_error < 0:
        return False
    for i in range(len(ls) - 1):
        if ls[i] > ls[i + 1]:
            return is_ascending(ls=ls[i + 1 :], margin_for_error=margin_for_error - 1)
    return True


def is_descending(ls: list[int], margin_for_error: int = 0) -> bool:
    return is_ascending(ls=ls[::-1], margin_for_error=margin_for_error)


def is_adjacent_difference_safe(
    ls: list[int],
    least_safe_difference: int,
    most_safe_difference: int,
    margin_for_error: int = 0,
) -> bool:
    if margin_for_error < 0:
        return False
    safe_range = range(least_safe_difference, most_safe_difference + 1)
    for i in range(1, len(ls) - 1):
        diff_prev = abs(ls[i - 1] - ls[i])
        diff_next = abs(ls[i] - ls[i + 1])
        if not all((diff in safe_range) for diff in (diff_prev, diff_next)):
            return is_adjacent_difference_safe(
                ls=ls[:i] + ls[i + 1 :],
                least_safe_difference=least_safe_difference,
                most_safe_difference=most_safe_difference,
                margin_for_error=margin_for_error - 1,
            )
    return True


def is_safe(
    ls: list[int],
    least_safe_difference: int,
    most_safe_difference: int,
    margin_for_error: int = 0,
) -> bool:
    return (
        is_ascending(ls=ls, margin_for_error=margin_for_error)
        or is_descending(ls=ls, margin_for_error=margin_for_error)
    ) and is_adjacent_difference_safe(
        ls=ls,
        least_safe_difference=least_safe_difference,
        most_safe_difference=most_safe_difference,
        margin_for_error=margin_for_error,
    )


def main():
    """Solve the puzzle"""
    reports = read_input()
    safe_report_count = sum(
        is_safe(
            ls=report,
            least_safe_difference=ADJACENT_DIFFER_AT_LEAST,
            most_safe_difference=ADJACENT_DIFFER_AT_MOST,
            margin_for_error=MARGIN_FOR_ERROR,
        )
        for report in reports
    )
    write_result(str(safe_report_count))


if __name__ == "__main__":
    main()
