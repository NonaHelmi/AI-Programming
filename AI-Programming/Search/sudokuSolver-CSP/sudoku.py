#  Tufts University COMP 131, Summer 2020
#  sudoku.py    
#  By:          Sawyer Bailey Paccione
#  Completed:   6/29/2020
#  
#  Description: 
#  Purpose:     

import argparse

from tkinter import Tk, Canvas, Frame, Button, BOTH, TOP, BOTTOM

from SudokuUI import SudokuUI
from SudokuBoard import SudokuBoard
from SudokuError import SudokuError

MARGIN  = 20  # Pixels around the board
SIDE    = 50  # Width of every board cell.
WIDTH   = HEIGHT = MARGIN * 2 + SIDE * 9  # Width and height of the whole board

"""
parse_arguments
Purpose:    Parses arguments of the form: sudoku.py <board name>
Parameters: board_name [string] the name of the txt file containing the board
Returns:    The name of the board
Effects:    The board file
Notes:      Nothing
"""
def parse_arguments():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("--board",
                            help = "Desired board name",
                            type = str,
                            required = False)

    # Creates a dictionary of keys = argument flag, and value = argument
    args = vars(arg_parser.parse_args())

    if(args['board'] == None):
        return './SudokuPuzzles/easy_puzzle.txt'
    else:
        return args['board']

if __name__ == '__main__':
    board_name = parse_arguments()

    with open(board_name, 'r') as boards_file:
        game = SudokuBoard(boards_file)

        root = Tk()
        SudokuUI(root, game)
        root.geometry("%dx%d" % (WIDTH, HEIGHT + 160))
        root.mainloop()
