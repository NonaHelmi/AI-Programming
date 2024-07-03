# Automatic Sudoku Puzzle Solver

Sudoku Puzzle posed as a CSP [(Constraint Satisfaction Problem)](https://en.wikipedia.org/wiki/Constraint_satisfaction_problem). There are three options available to solve a puzzle, **Backtracking**, **Forward Checking**, and **BackJumping**. You can also check the Search Heuristic, *Basic* and *Minimum Reamaining Value*.

## Authors

- [@Sawyer Paccione](https://github.com/paccionesawyer) -  Tufts University COMP 131, Summer 2020

## Demo 

![Demo](https://github.com/paccionesawyer/sodokuSolver-CSP/blob/main/sudoku-solver-demo.gif)

## Run Locally

Clone the project

```bash
  git clone https://github.com/paccionesawyer/sodokuSolver-CSP.git
```

Go to the project directory

```bash
  cd sodokuSolver-CSP
```

Install dependencies

Run Terminal Based:

```bash
  python3 solver.py [--board board_file.txt]
```

Run GUI Sudoku:

```bash
  python3 sudoku.py [--board board_file.txt]
```

Examples:

```bash
  python3 solver.py --board easy_puzzle.txt
  python3 sudoku.py --board evil_puzzle.txt
```

If the --board flag is not provided the program is run with easy_puzzle

Notes:  I can't get conflict-directed back-jumping to work with find_empty_basic sorry

## Acknowledgements

- [GUI Python Help](http://newcoder.io/gui.)
- [RadioBar](https://www.python-course.eu/tkinter_radiobuttons.php)
- [Hardest Sudoku Puzzle](https://www.conceptispuzzles.com/index.aspx?uri=info/article/424#:~:text=In)

## License

[MIT](https://choosealicense.com/licenses/mit/)
  
## Appendix

**SudokuBoard.py:** The representation of the Sudoku by a 2D array of int, where 0 represents an empty cell

**solver.py:** Holds the various search algorithms for solving the sudoku CSP

**sudoku.py:** Program that runs the program UI

**SudokuUI.py:** The Graphical User Interface (GUI) representation of a Sudoku Board. It can be played simply or it can be solved with a combination of Algorithms and Search Heuristics. The Tkinter UI, responsible for drawing the board and accepting user input.

**SudokuError.py:** Throw exceptions when there is an error input

**RadioBar.py:** A collection of Radio Buttons all indicating various options for the same value

**evil_puzzle.txt:** Text file representation of the evil puzzle given in class

**easy_puzzle.txt:** Text file representation of the easy puzzle given in class

**blank_puzzle.txt:** Text file representation of an empty board with all blanks spaces
