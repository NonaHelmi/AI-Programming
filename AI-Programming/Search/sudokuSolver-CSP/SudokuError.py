#  Tufts University COMP 131, Summer 2020
#  SudokuError.py    
#  By:          Sawyer Bailey Paccione
#  Completed:   6/30/2020
#               
#  Description: An application specific error.
#  Purpose:     Throw exceptions when there is an error input

"""
SudokuError
Purpose:    Throw exceptions when there is an error input
Parameters: Exception [string], The text to be printed when the exception 
            is thrown
Returns:    Nothing
Effects:    If this class is called the program stops and prints 'Exception'
Notes:      Parent class is Exception
"""
class SudokuError(Exception):
    pass