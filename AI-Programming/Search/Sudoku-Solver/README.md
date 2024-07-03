# [Sudoku Solver](https://github.com/carcassonkp/Sudoku-Solver/files/8042078/SUDOKU.pdf)
## Brute-Force Backtracking Approach (Depth First Search)

<p align="justify">
In this approach the first step is to find an empty Sudoku cell and fill it with a digit from one to nine. The algorithm verifies which digits are safe to use whenever it finds an empty
cell; if a digit is already present in that cell’s row, column, or square, it will not be inserted. Once a digit has been placed, the algorithm will use recursion to run the solving function
again, this time finding the next empty cell and repeating the process until there are no empty cells, the problem has been solved. If a cell cannot be filled with a number, the algorithm will return to the previous cell and change the digit to another
valid option, a process known as backtracking.
</p>



<p align="center">
  <img src="https://upload.wikimedia.org/wikipedia/commons/8/8c/Sudoku_solved_by_bactracking.gif" alt="animated" />
</p>

## CSP Approach with Backtracking ( Depth First Search with MRV)
<p align="justify">
When approaching Sudoku solving as a CSP it’s required to
define and identify the problem’s components. The components
include the variables, the domain and the problem’s constraints.
</p>


* Variables = {Cell1 . . . Cell81}. 
* Domain = {1, 2, 3, 4, 5, 6, 7, 8, 9
* Constraint 1 = {Rows must have unique values}
* Constraint 2 = {Columns must have unique values}
* Constraint 3 = {Squares must have unique values}

<p align="justify">
The main objective of this approach is to reduce the search
space of the problem before we implement recursion and
backtracking. The first step is to attribute to each cell in
the Sudoku a list of its peers, a cell’s peers are the cells
present in the corresponding row, column and square. This will
greatly improve the search time when the algorithm needs to
check if a digit is already present on that cell’s peers. The
second step consists in filling every single empty cell with all
the digits in the domain, which are digits from one to nine,
shown in the next figure.
</p>


<p align="center" width="100%">
    <img width="30%" src="https://user-images.githubusercontent.com/70576587/150957524-1e97744a-2a5c-4bb4-8ba2-4496407006a7.png"> 
</p>

<p align="justify">
The elements inside the list of every cell can be removed
if any of those digits are already present in that cell’s peers,
this is the third step. It will improve the algorithms speed
considering that this reduces the amount of digits that it needs
to test. In the simple backtracking approach every digit from
the domain is tested even though it might not be unique in that
cell’s peer list. With this technique it’s also possible to find
the solution for a cell if there is a single suitable digit after
removing the duplicate digits, this is called single possibility
or naked single, a common Sudoku strategy.
  </p>

<p align="justify">
The fourth step is to implement the hidden single strategy
this is another technique used to further reduce the search space
before the algorithm commits to recursion and backtracking to
solve the rest of the puzzle. The term ”hidden single” refers to
a single candidate cell remaining for a specific digit in a row,
column or square, even if the cell has multiple possible digits
if a digit is unique in that cell’s peer row, column or square
then that specific digit must be placed there.
</p>


<p align="center" width="100%">
    <img width="30%" src="https://user-images.githubusercontent.com/70576587/150958365-f1996032-709a-44b5-a820-f485a7b91341.png"> 
</p>

<p align="justify">
  After eliminating duplicate values from the possible digits
and checking the puzzle for hidden singles, shown inthe previous figure
, if any number of cells are solved with these techniques
the algorithm will repeat them, otherwise the algorithm starts
utilizing recursion.
 </p>
 
<p align="justify">
The fifth step is where recursion takes place. Here, the
algorithm will choose a cell with the fewest number of
possibilities and place the first digit on that list in that cell.
This heuristic is called minimum remaining values (MRV) and
it was chosen because it helps in discovering inconsistencies
earlier. Then the algorithm will repeat the third and fourth
step until it either finishes solving the Sudoku or until a cell
is left with no possible digits, this means that the digit we
chose for the cell, with the fewest possibilities, was incorrect
forcing the algorithm to backtrack and try another digit. After
multiple iterations of these steps the Sudoku puzzle will finally
be solved.

  </p>

## Experimental Results and Analyses
<p align="justify">
In order to measure the efficiency of the algorithms, during
the solving of each puzzle, it was taken into account the solving
time, the number of recursions and backtracks that were needed
to reach the final solution.
In table I it’s possible to see that the backtracking-only
method was actually faster than the CSP. This was because the
CSP algorithm spends more time trying to reduce the search
space, like creating each variable’s peer list. Meanwhile the
backtrack brute-force approach can just start solving the puzzle.
The brute-force approach only solves faster because this Sudoku
already has a large amount of its cells filled from the get-go,
so the backtracking algorithm doesn’t have to brute-force test
that many possibilities.
    </p>


| Table I - Easy  |      BT only     |  CSP with BT |   
|----------|:-------------:|------:|
| Solve time (ms)  |  1.5 | 3.3 |
| Recursions  |    166   |   0 |
| Backtracks  | 120 |    0 |


| Table II - Intermediate  |      BT only     |  CSP with BT |   
|----------|:-------------:|------:|
| Solve time (ms)  |  430.5 | 272.7 |
| Recursions  |    49 498   |   186 |
| Backtracks  |49 558  |    90 |

| Table III - Hard  |      BT only     |  CSP with BT |   
|----------|:-------------:|------:|
| Solve time (ms)  |  17 179 | 6 |
| Recursions  |    1 904 479   |   0 |
| Backtracks  |1 904 540  |    0 |
<p align="justify">
From table II and III, it’s possible to observe a huge
difference in speed, mainly because the Sudoku puzzles have
less cells filled from the get-go, so the CSP method takes
advantage of being able to highly reduce the search space,
while the brute-force has to test out an astonishing number of
possibilities.
</p>
