# random-scripts
Odds and ends - miscellaneous scripts for random purposes


## Sudoku
This is a basic sudoku puzzle solver. It combines two search methods, which means that it can solve Easy and Medium Sudokus. 

Save your puzzles in the puzzles folder as a text file.

```python
python solve_sudoku.py -i 'path\to\puzzle.txt' -n 10 -o 'path\to\puzzle_solved.txt'
```

10 iterations is more than sufficient to solve Easy and Medium difficulty puzzles. 