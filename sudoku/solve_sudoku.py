from typing import List, Tuple
import os


def remove_values_from_list(the_list: List[int], val: int) -> List[int]:
    """
    Remove all occurrences of a value in a list.

    Parameters
    ----------
    the_list : List[int]
        List of integers
    val : int
        Value to be removed from list.

    Returns
    -------
    List[int]
        List after removing all occurrences of a value.

    """
    return [value for value in the_list if value != val]


def read_puzzle(sudoku_path: str) -> List[List[int]]:
    """
    Read a Sudoku puzzle from a file path.
    Return the puzzle in a list of lists.

    Parameters
    ----------
    sudoku_path : str
        sudoku puzzle fil path.

    Raises
    ------
    RuntimeError
        If puzzle is not square, there are missing values in the file.

    Returns
    -------
    List[List[int]]
        The sudoku puzzle as a list of rows of integers.

    """
    with open(sudoku_path, 'r') as f:
        content = f.readlines()

    board = list()
    for line in content:
        new_line = line.rstrip()
        if new_line:
            new_line = list(map(int, new_line.split(' ')))
            board.append(new_line)

    if not all((len(row) == len(board) for row in board)):
        dimension_error = "Missing values in puzzle"
        raise RuntimeError(dimension_error)

    return board


def validate_puzzle(board: List[List[int]]) -> bool:
    """
    Validate that numbers are not duplicated in any row, column or square.

    Parameters
    ----------
    board : List[List[int]]
        Sudoku puzzle to solve.

    Returns
    -------
    bool
        True if board is validated.

    """
    for r in board:
        row = remove_values_from_list(r, 0)
        if len(row) != len(set(row)):
            return False

    for c in range(9):
        column = [board[_][c] for _ in range(9)]
        column = remove_values_from_list(column, 0)
        if len(column) != len(set(column)):
            return False

    for r in [0, 3, 6]:
        for c in [0, 3, 6]:
            existing_values = select_square((r, c), board)
            existing_values = remove_values_from_list(existing_values, 0)
            if len(existing_values) != len(set(existing_values)):
                return False

    return True


def select_square(cell_coordinates: Tuple[int, int], list2d: List[List[int]]) -> List[int]:
    square_row, square_col = cell_coordinates[0] // 3, cell_coordinates[1] // 3
    square_rows = list2d[3 * square_row:3 * square_row + 3][:]
    square_values = list()

    for sr in square_rows:
        square_values.extend(sr[3 * square_col:3 * square_col + 3])
    return square_values


if __name__ == '__main__':
    input_file = os.path.abspath("puzzles/puzzle_0001_fail.txt")

    if not os.path.isfile(input_file):
        fnf_error = f"File {input_file} not found"
        raise FileNotFoundError(fnf_error)

    puzzle = read_puzzle(input_file)

    is_validated = validate_puzzle(puzzle)

    if not is_validated:
        bad_puzzle_error = f"File {input_file} contains a bad puzzle."
        raise RuntimeError(bad_puzzle_error)


