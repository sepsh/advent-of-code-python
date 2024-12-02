"""Solution for for puzzle '2024/01_2'"""

from pathlib import Path

INPUT_FILE = "input.txt"
RESULT_FILE = "result.txt"


def read_input() -> list[tuple[int, int]]:
    """Read input from file"""
    input_file = Path(__file__).parent / INPUT_FILE
    with open(input_file, "r") as f:
        return [tuple(map(int, line.strip().split())) for line in f.readlines()]


def write_result(data: str):
    """Write results to a file"""
    result_file = Path(__file__).parent / RESULT_FILE
    with open(result_file, "w") as f:
        f.write(data)


def main():
    """Solve the puzzle"""
    left_list: list[int] = []
    right_list: list[int] = []
    for left, right in read_input():
        left_list.append(left)
        right_list.append(right)
    similarity_scores = [left_point * right_list.count(left_point) for left_point in left_list]
    write_result(str(sum(similarity_scores)))


if __name__ == "__main__":
    main()
