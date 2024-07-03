#  Tufts University COMP 131, Summer 2020
#  unittesting.py
#  By:          Sawyer Bailey Paccione
#  Completed:   
#  
#  Description: 
#  Purpose:     Clean up the dirt

import unittest

from SudokuBoard import SudokuBoard
from solver import backtracking

easy_puzzle =       [   [6,0,8,7,0,2,1,0,0],
                        [4,0,0,0,1,0,0,0,2],
                        [0,2,5,4,0,0,0,0,0],
                        [7,0,1,0,8,0,4,0,5],
                        [0,8,0,0,0,0,0,7,0],
                        [5,0,9,0,6,0,3,0,1],
                        [0,0,0,0,0,6,7,5,0],
                        [2,0,0,0,9,0,0,0,8],
                        [0,0,6,8,0,5,2,0,3],    ]

easy_puzzle_solved =[   [6,9,8,7,5,2,1,3,4],
                        [4,7,3,6,1,8,5,9,2],
                        [1,2,5,4,3,9,8,6,7],
                        [7,6,1,9,8,3,4,2,5],
                        [3,8,2,5,4,1,9,7,6],
                        [5,4,9,2,6,7,3,8,1],
                        [8,3,4,1,2,6,7,5,9],
                        [2,5,7,3,9,4,6,1,8],
                        [9,1,6,8,7,5,2,4,3],    ]

evil_puzzle_solved =[   [1,7,6,3,4,2,9,8,5],
                        [4,2,5,9,7,8,6,1,3],
                        [3,9,8,5,6,1,4,2,7],
                        [2,6,1,7,8,4,5,3,9],
                        [9,8,3,2,5,6,7,4,1],
                        [5,4,7,1,9,3,2,6,8],
                        [8,1,9,4,2,5,3,7,6],
                        [6,5,4,8,3,7,1,9,2],
                        [7,3,2,6,1,9,8,5,4],    ]

class testSolver(unittest.TestCase):
    
    """
    funcname
    Purpose:    
    Arguments:  
    Returns:    
    Effects:    
    Notes:      
    """
    def setUp(self):
        self.puzzle = SudokuBoard()

    #Testing Task
    """
    funcname
    Purpose:    
    Arguments:  
    Returns:    
    Effects:    
    Notes:      
    """    
    def test_SetUp(self):
        self.assertEqual(self.puzzle.board, easy_puzzle)
    
    def test_easySolve(self):
        backtracking(self.puzzle)
        self.assertEqual(self.puzzle.board, easy_puzzle_solved)

    def test_evilSolve(self):
        self.puzzle.initialize("evil_puzzle.txt")
        backtracking(self.puzzle)
        self.assertEqual(self.puzzle.board, evil_puzzle_solved)

if __name__ == '__main__':
    unittest.main()
