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


def intersection_lists(list1: List[int], list2: List[int], list3: List[int]) -> List[int]:
    """
    Find all common values between three lists.

    Parameters
    ----------
    list1 : List[int]
        List of integers 1.
    list2 : List[int]
        List of integers 2.
    list3 : List[int]
        List of integers 3.

    Returns
    -------
    List[int]
        List of integers in common.

    """
    return [value for value in list1 if (value in list2 and value in list3)]


def read_puzzle(sudoku_path: str) -> List[List[int]]:
    """
    Read a Sudoku puzzle from a file path.
    Return the puzzle in a list of lists.

    Parameters
    ----------
    sudoku_path : str
        sudoku puzzle file path.

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


def select_square(cell_coordinates: Tuple[int, int], board: List[List[int]]) -> List[int]:
    """
        Select all cells in a given square in the board.

        Parameters
        ----------
        cell_coordinates : Tuple[int, int]
            Cell coordinates.
        board : List[List[int]]
            Sudoku board.

        Returns
        -------
        List[int]
            List of cell values in square.

        """
    square_row, square_col = cell_coordinates[0] // 3, cell_coordinates[1] // 3
    square_rows = board[3 * square_row:3 * square_row + 3][:]
    square_values = list()

    for sr in square_rows:
        square_values.extend(sr[3 * square_col:3 * square_col + 3])
    return square_values


def solve_board(board: List[List[int]]) -> List[List[int]]:
    row_possibility_space = dict.fromkeys([rr for rr in range(9)], [])
    column_possibility_space = dict.fromkeys([cc for cc in range(9)], [])

    square_possibility_space = dict.fromkeys([(r, c) for r in range(9) for c in range(9)], [])

    iters = 0
    max_iterations = 6
    # TODO: Priority: High: re-factor code to handle the maximum iteration depth.

    while iters < max_iterations:
        print(f"Iteration {iters}")

        for r in range(9):
            existing_row_vals = remove_values_from_list(board[r][:], 0)
            row_possibility_space[r] = [_ for _ in range(1, 10) if _ not in existing_row_vals]
        for c in range(9):
            column = [board[i][c] for i in range(9)]
            existing_col_vals = remove_values_from_list(column, 0)
            column_possibility_space[c] = [_ for _ in range(1, 10) if _ not in existing_col_vals]

        empty_cells_count = 0
        for r in range(9):
            for c in range(9):
                if puzzle[r][c] == 0:
                    empty_cells_count += 1
                    square_vals = select_square((r, c), board)
                    existing_square_vals = remove_values_from_list(square_vals, 0)
                    square_possibility_space[(r, c)] = [_ for _ in range(1, 10) if _ not in existing_square_vals]

                    common_elements = intersection_lists(row_possibility_space[r], column_possibility_space[c],
                                                         square_possibility_space[(r, c)])

                    if len(common_elements) == 1:
                        print(f"we uniquely identified the value at {r}, {c} = {common_elements[0]}")
                        board[r][c] = common_elements[0]
                        empty_cells_count -= 1

        print(f"empty cells count {empty_cells_count}")
        iters += 1
        if empty_cells_count == 0:
            iters = max_iterations
            print("puzzle solved")
    return board


if __name__ == '__main__':
    input_file = os.path.abspath("puzzles/puzzle_0001.txt")

    if not os.path.isfile(input_file):
        fnf_error = f"File {input_file} not found"
        raise FileNotFoundError(fnf_error)

    # TODO: Priority: medium: implement IO checks on output file path.
    output_file = os.path.abspath("puzzles_solved/puzzle_0001_solved.txt")

    puzzle = read_puzzle(input_file)

    is_validated = validate_puzzle(puzzle)

    if not is_validated:
        bad_puzzle_error = f"File {input_file} contains a bad puzzle."
        raise RuntimeError(bad_puzzle_error)

    solved_puzzle = solve_board(puzzle)

    # TODO: Priority: low: re-factor output file writing.
    with open(output_file, 'w') as f:
        for solved_row in solved_puzzle:
            f.write(str(solved_row)+'\n')
