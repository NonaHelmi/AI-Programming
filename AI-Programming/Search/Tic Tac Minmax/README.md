# Tic Tac Toe with Minmax (and alpha beta pruning)

**Demo**

<div align='center'>
  
![](ezgif.com-gif-maker.gif)

</div>

## Functionality
There are two algorithms, 
1) [With MinMax Algorithm](https://github.com/Arshad221b/Connect_4/blob/master/tictactoe_minmax.py)
2) [With MinMax and Alpha-Beta Pruning](https://github.com/Arshad221b/Connect_4/blob/master/tic_tac_toe_minmax.py)

### Details about each method 
#### 1) def winning_conditions()
It checks for each winning condition possible in the game (horizontal, vertical, digonal). It returns the score for winning, losing and tie conditons.

#### 2) def possible_moves()
Checks all the blank spaces(available spaces) in the grid.

#### 3) def minmax()

##### In Minmax:
In simple terms, it checks for each condition in the game. There are two parts, first part is maximizing player (Human) and other is minimizing player (AI).In both types, we first check for the blank spaces available. Based on this, they check the score for each condition. The minimiser and maximizer play one after other. 

##### In Minmax with alpha beta pruning:
In alpha beta pruning, we pass two extra parameters (alpha and beta). These parameters store the best value at that particular depth in the tree. Alpha stores best value for maximizer and beta stores best value for minimiser. In each case, we don't have to solve the entire tree. If the value at that depth is not useful for the minimiser/maximizer that branch of tree never gets played and hence saves the computational cost. 

## References
1) MIT Opencourseware: [Search: Games, Minimax, and Alpha-Beta](https://youtu.be/STjW3eH0Cik)
3) The Coding train: [Coding Challenge 154: Tic Tac Toe AI with Minimax Algorithm](https://www.youtube.com/watch?v=trKjYdBASyQ)
4) Geeks for Geeks: [Minimax Algorithm in Game Theory](https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-4-alpha-beta-pruning/)
5) Stack abuse:[Minimax with Alpha-Beta Pruning in Python](https://stackabuse.com/minimax-and-alpha-beta-pruning-in-python)

## How to run
1) Run [tictactoe_minmax.py](https://github.com/Arshad221b/unbeatable_tic_tac_toe/blob/master/tictactoe_minmax.py) for Minmax
2) Run [tic_tac_toe_minmax.py](https://github.com/Arshad221b/unbeatable_tic_tac_toe/blob/master/tic_tac_toe_minmax.py) for Minmax with Alpha-Beta Pruning
