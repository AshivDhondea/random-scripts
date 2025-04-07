from typing import Dict, List, Tuple
import argparse
import copy
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
    with open(sudoku_path, 'r') as file:
        content = file.readlines()

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


def solve_board(board_to_solve: List[List[int]], max_iterations: int) -> List[List[int]]:
    # Solve the board iteratively.
    # Combine two approaches:
    # 1. resolve empty cells if they are the only cell in their row, column or square which can contain a given value.
    # 2. resolve empty cells if their possibility space contains only one value.

    iters = 0
    while iters < max_iterations:
        # Fill in the possibility space for each empty cell.
        filled_board_space = fill_board_space(board_to_solve)
        # Resolve empty cells based on unique values in the possibility space.
        board_to_solve = filter_by_possibility_space(filled_board_space, board_to_solve)
        # Update the possibility space.
        filled_board_space = fill_board_space(board_to_solve)

        # Resolve empty cells based on unique possibilities.
        empty_cells_count = 0
        for r in range(9):
            row_board_space = dict()
            for c in range(9):
                if board_to_solve[r][c] == 0:
                    # Empty cell in puzzle.
                    empty_cells_count += 1
                    row_board_space[c] = filled_board_space[(r, c)]
                    if len(filled_board_space[(r, c)]) == 1:
                        # Only one possible value for this empty cell.
                        board_to_solve[r][c] = filled_board_space[(r, c)][0]
                        empty_cells_count -= 1
        print(f"Iteration {iters} , {empty_cells_count} empty cells.")

        iters += 1
        if empty_cells_count == 0:
            iters = max_iterations
            print("Puzzle solved")
    return board_to_solve


def fill_board_space(board_to_solve: List[List[int]]) -> Dict:
    # For each cell, fill in the possibility space according to other cells in the same row, column and square.
    row_possibility_space = dict()
    column_possibility_space = dict()
    for k in range(9):
        row_possibility_space[k] = list()
        column_possibility_space[k] = list()

    square_possibility_space = dict()
    for rk in range(9):
        for ck in range(9):
            square_possibility_space[rk, ck] = list()

    board_space = dict()
    for rk in range(9):
        for ck in range(9):
            board_space[rk, ck] = list()

    for r in range(9):
        existing_row_vals = remove_values_from_list(board_to_solve[r][:], 0)
        row_possibility_space[r] = [_ for _ in range(1, 10) if _ not in existing_row_vals]
        for c in range(9):
            column = [board_to_solve[i][c] for i in range(9)]
            existing_col_vals = remove_values_from_list(column, 0)
            column_possibility_space[c] = [_ for _ in range(1, 10) if _ not in existing_col_vals]

            if board_to_solve[r][c] == 0:
                # fill in board_space according to row, column and square.
                square_vals = select_square((r, c), board_to_solve)
                existing_square_vals = remove_values_from_list(square_vals, 0)
                square_possibility_space[(r, c)] = [_ for _ in range(1, 10) if _ not in existing_square_vals]

                board_space[(r, c)] = intersection_lists(row_possibility_space[r], column_possibility_space[c],
                                                         square_possibility_space[(r, c)])
    return board_space


def filter_by_possibility_space(possibility_space: Dict, board_to_solve: List[List[int]]) -> List[List[int]]:
    for r in range(9):
        # For each row, get the possibility space for each cell.
        row_space = [possibility_space[(r, c_)] for c_ in range(9)]
        # For each possibility (1 to 9), map which cell index can possibly hold it.
        mapping = dict([(_, []) for _ in range(1, 10)])
        for index, item in enumerate(row_space):
            if len(item) != 0:
                # If length is not 0, cell is empty.
                for k in item:
                    # for each item in the possibility space of the empty cell, add it to the map.
                    mapping[k].append(index)
        # Go through the map, if a value appears only once in the map, it can appear only in that cell of the row.
        for key, value in mapping.items():
            if len(value) == 1:
                board_to_solve[r][value[0]] = key

    # Same procedure for columns.
    for c in range(9):
        column_space = [possibility_space[(r_, c)] for r_ in range(9)]

        mapping = dict([(_, []) for _ in range(1, 10)])
        for index, item in enumerate(column_space):
            if len(item) != 0:
                for k in item:
                    mapping[k].append(index)
        for key, value in mapping.items():
            if len(value) == 1:
                board_to_solve[value[0]][c] = key

    # Same procedure for squares.
    for r in [0, 3, 6]:
        for c in [0, 3, 6]:
            square_space = [[possibility_space[(r + rx, c_)] for c_ in range(c, c + 3)] for rx in range(3)]

            mapping = dict([(_, []) for _ in range(1, 10)])
            for i_rr, rr in enumerate(square_space):
                for index, item in enumerate(rr):
                    if len(item) != 0:
                        for k in item:
                            mapping[k].append([i_rr + r, index + c])
            for key, value in mapping.items():
                if len(value) == 1:
                    board_to_solve[value[0][0]][value[0][1]] = key
    return board_to_solve


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--input", help="input file path", type=str, required=True)
    ap.add_argument("-n", "--iterations", help="number of iterations", type=int, required=True)
    ap.add_argument("-o", "--output", help="output file path", type=str, required=True)

    args = ap.parse_args()
    input_file = args.input
    num_iters = args.iterations
    output_file = args.output

    if not os.path.isfile(input_file):
        fnf_error = f"File {input_file} not found"
        raise FileNotFoundError(fnf_error)

    output_path_split = os.path.split(output_file)
    if not os.path.isdir(output_path_split[0]):
        dir_err = f"Output directory {output_path_split} not found"
        raise NotADirectoryError(dir_err)

    # Read in the puzzle and validate it for consistency (no repeated value in row, column and square).
    puzzle = read_puzzle(input_file)
    is_validated = validate_puzzle(puzzle)

    if not is_validated:
        bad_puzzle_error = f"File {input_file} contains a bad puzzle."
        raise RuntimeError(bad_puzzle_error)

    # Copy the puzzle and solve it.
    puzzle_to_solve = copy.deepcopy(puzzle)
    solved_puzzle = solve_board(puzzle_to_solve, num_iters)
    # Verify that the solved puzzle is consistent.
    is_validated = validate_puzzle(solved_puzzle)
    if not is_validated:
        bad_solve_error = f"Solved puzzle is wrong."
        raise RuntimeError(bad_solve_error)

    # TODO: Priority: low: re-factor output file writing.
    with open(output_file, 'w') as f:
        for solved_row in solved_puzzle:
            f.write(str(solved_row) + '\n')
