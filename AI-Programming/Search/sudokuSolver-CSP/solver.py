#  Tufts University COMP 131, Summer 2020
#  solver.py    
#  By:          Sawyer Bailey Paccione
#  Completed:   6/29/2020
#  
#  Description: 
#  Purpose:     Holds the various CSP algorithms for the sudoku puzzle 

from SudokuBoard import SudokuBoard

import sys
import pprint
import time
import argparse
###############################################################################
##                                  Domains                                  ##
###############################################################################
"""
set_domains
Purpose:    Initialize the domains of each cell in the board
Parameters: sudoku_puzzle   [SudokuBoard],  The Board to base the domains off of
Returns:    domains [3D Array], The possible values for each position in the 
            board
Effects:    Memory 
Notes:      
"""
def set_domains(sudoku_puzzle):
    n = 9
    domains = [[[1, 2, 3, 4, 5, 6, 7, 8,9] for j in range(n)] for i in range(n)]
    
    for i in range(len(sudoku_puzzle.board)):
        for j in range(len(sudoku_puzzle.board[i])):
            val = sudoku_puzzle.board[i][j]
            if (val != 0):
                domains[i][j] = [-1]
                constrict_domains(sudoku_puzzle, i, j, val, domains)
                if(len(domains[i][j]) == 0):
                    print("IMPOSSIBLE TABLE: There are no possible values for", 
                    [i,j])
                    exit(0)
    return domains  


"""
constrict_domains
Purpose:    Constrict the domains of the board given the number inserted in a 
            given position
Parameters: sudoku_puzzle   [SudokuBoard],  The Board 
            row             [int],          the row index of the most recently 
                                            inserted number
            col             [int],          the column index of the most 
                                            recently inserted num    
            domains         [3D Array],     The values for each position 
Returns:    Nothing
Effects:    domains
Notes:
"""
def constrict_domains(sudoku_puzzle, row, col, num, domains):
    # Remove Num from Box Domains
    constrict_box_domains(sudoku_puzzle, row, col, num, domains)
    
    # Remove Num from Row Domains
    constrict_row_domains(sudoku_puzzle, row, col, num, domains)

    # Remove Num from Col Domains
    constrict_col_domains(sudoku_puzzle, row, col, num, domains)


"""
constrict_box_domains
Purpose:    Constrict the domains of the box given the number inserted in a 
            given position
Parameters: sudoku_puzzle   [SudokuBoard],  The Board 
            row             [int],          the row index of the most recently 
                                            inserted number
            col             [int],          the column index of the most 
                                            recently inserted num    
            domains         [3D Array],     The values for each position 
Returns:    Nothing
Effects:    domains
Notes:
"""
def constrict_box_domains(sudoku_puzzle, row, col, num, domains):
    box_x = col // 3
    box_y = row // 3

    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if (num in domains[i][j] and [i,j] != [row, col]
                and sudoku_puzzle.board[i][j] == 0):
                domains[i][j].remove(num)


"""
constrict_row_domains
Purpose:    Constrict the domains of the row given the number inserted in a 
            given position
Parameters: sudoku_puzzle   [SudokuBoard],  The Board 
            row             [int],          the row index of the most recently 
                                            inserted number
            col             [int],          the column index of the most 
                                            recently inserted num    
            domains         [3D Array],     The values for each position 
Returns:    Nothing
Effects:    domains
Notes:
"""
def constrict_row_domains(sudoku_puzzle, row, col, num, domains):
    for j in range(len(sudoku_puzzle.board[row])):
        if (num in domains[row][j] and col != j
            and sudoku_puzzle.board[row][j] == 0):
            domains[row][j].remove(num)


"""
constrict_col_domains
Purpose:    Constrict the domains of the col given the number inserted in a 
            given position
Parameters: sudoku_puzzle   [SudokuBoard],  The Board 
            row             [int],          the row index of the most recently 
                                            inserted number
            col             [int],          the column index of the most 
                                            recently inserted num    
            domains         [3D Array],     The values for each position 
Returns:    Nothing
Effects:    domains
Notes:
"""
def constrict_col_domains(sudoku_puzzle, row, col, num, domains):
    for i in range(len(sudoku_puzzle.board)):
        if (num in domains[i][col] and row != i
            and sudoku_puzzle.board[i][col] == 0):
            domains[i][col].remove(num)


"""
empty_domain
Purpose:    Find an empty domain
Parameters: sudoku_puzzle   [SudokuBoard],  The Board 
            domains         [3D Array],     The values for each position 
Returns:    [list] The [row, col] of the empty domain
            [bool] False if there is no empty domain
Effects:    Nothing
Notes:
"""
def empty_domain(sudoku_puzzle, domains):
    for i in range(len(sudoku_puzzle.board)):
        for j in range(len(sudoku_puzzle.board[i])):
            if(sudoku_puzzle.board[i][j] == 0 and len(domains[i][j]) == 0):
                return [i, j]
    
    return False


"""
find_empty_domain
Purpose:    Find an empty domain
Parameters: sudoku_puzzle   [SudokuBoard],  The Board 
            domains         [3D Array],     The values for each position 
Returns:    [list] The [row, col] of the empty domain
Effects:    Nothing
Notes:      
"""
def find_empty_domain(sudoku_puzzle, domains):
    for i in range(len(domains)):
        for j in range(len(domains[i])):
            if(len(domains[i][j]) == 0 and sudoku_puzzle.board[i][j] == 0):
                return [i, j]


"""
repair_domains
Purpose:    Repair the domains of the board given the number inserted in a 
            given position
Parameters: sudoku_puzzle   [SudokuBoard],  The Board 
            row             [int],          the row index of the most recently 
                                            inserted number
            col             [int],          the column index of the most 
                                            recently inserted num    
            domains         [3D Array],     The values for each position 
Returns:    Nothing
Effects:    domains
Notes:
"""
def repair_domains(sudoku_puzzle, row, col, num, domains):
    # Add Num to Box Domains
    repair_box_domains(sudoku_puzzle, row, col, num, domains)

    # Remove Num from Row Domains
    repair_row_domains(sudoku_puzzle, row, col, num, domains)

    # Remove Num from Col Domains
    repair_col_domains(sudoku_puzzle, row, col, num, domains)


"""
repair_domains
Purpose:    Repair the domains of the box given the number inserted in a 
            given position
Parameters: sudoku_puzzle   [SudokuBoard],  The Board 
            row             [int],          the row index of the most recently 
                                            inserted number
            col             [int],          the column index of the most 
                                            recently inserted num    
            domains         [3D Array],     The values for each position 
Returns:    Nothing
Effects:    domains
Notes:
"""
def repair_box_domains(sudoku_puzzle, row, col, num, domains):
    box_x = col // 3
    box_y = row // 3

    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if (num not in domains[i][j] and [i,j] != [row, col] 
            and sudoku_puzzle.valid_input(i,j,num)):
                domains[i][j].append(num)


"""
repair_domains
Purpose:    Repair the domains of the row given the number inserted in a 
            given position
Parameters: sudoku_puzzle   [SudokuBoard],  The Board 
            row             [int],          the row index of the most recently 
                                            inserted number
            col             [int],          the column index of the most 
                                            recently inserted num    
            domains         [3D Array],     The values for each position 
Returns:    Nothing
Effects:    domains
Notes:
"""
def repair_row_domains(sudoku_puzzle, row, col, num, domains):
    for j in range(len(sudoku_puzzle.board[row])):
        if (num not in domains[row][j] and col != j 
        and sudoku_puzzle.valid_input(row, j, num)):
            domains[row][j].append(num)


"""
repair_domains
Purpose:    Repair the domains of the col given the number inserted in a 
            given position
Parameters: sudoku_puzzle   [SudokuBoard],  The Board 
            row             [int],          the row index of the most recently 
                                            inserted number
            col             [int],          the column index of the most 
                                            recently inserted num    
            domains         [3D Array],     The values for each position 
Returns:    Nothing
Effects:    domains
Notes:
"""
def repair_col_domains(sudoku_puzzle, row, col, num, domains):
    for i in range(len(sudoku_puzzle.board)):
        if (num not in domains[i][col] and row != i 
        and sudoku_puzzle.valid_input(i, col, num)):
            domains[i][col].append(num)




###############################################################################
##                             Variable Ordering                             ##
###############################################################################
"""
find_empty_basic
Purpose:    Find the top-most, left-most empty cell 
Parameters: Nothing
Returns:    A list of elements that represents the row, column
Effects:    backtracking in solver.py
Notes:      
"""
def find_empty_basic(sudoku_puzzle, domains):
    for i in range(len(sudoku_puzzle.board)):
        for j in range(len(sudoku_puzzle.board[i])):
            if (sudoku_puzzle.board[i][j] == 0):
                return [i, j]
    return False


"""
minimum_remaining_values
Purpose:    Find the position with the minimum remaining values in its 
            domain
Parameters: sudoku_puzzle   [SudokuBoard],  The Board 
            domains         [3D Array],     The values for each position 
Returns:    A list of elements that represents the row, column
Effects:
Notes:
"""
def minimum_remaining_values(sudoku_puzzle, domains):
    mrv = find_empty_basic(sudoku_puzzle, domains)

    if(mrv == False):
        return False

    for i in range(len(domains)):
        for j in range(len(domains[i])):
            if (sudoku_puzzle.board[i][j] == 0 and 
                len(domains[i][j]) < len(domains[mrv[0]][mrv[1]])):
                mrv[0] = i
                mrv[1] = j
    return mrv




###############################################################################
##                             Basic Backtracking                            ##
###############################################################################
"""
backtracking
Purpose:    Sets the domains and runs a recursive backtracking algorithm
Parameters: sudoku_puzzle   [SudokuBoard],  The Board 
            heuristic       [function],     The search function to find the 
                                            next value
Returns:    Nothing
Effects:    board values
Notes:
"""
def backtracking(sudoku_puzzle, heuristic):
    domains = set_domains(sudoku_puzzle)

    backtracking_rec(sudoku_puzzle, heuristic, domains)

"""
backtracking_rec
Purpose:    Runs a simple backtracking algorithm
Parameters: sudoku_puzzle   [SudokuPuzzle], The given sudoku puzzle
            heuristic       [function],     The search function to find the 
                                            next value
            domains         [3D Array],     The values for each position 
Returns:    [bool], whether the current stateof the board can return a solution
Effects:    sudoku_puzzle
Notes:      Recursive algorithm
"""
def backtracking_rec(sudoku_puzzle, heuristic, domains):
    next = heuristic(sudoku_puzzle, domains)
    if not next:
        return True
    else:
        sudoku_puzzle.unique_states += 1 

        row = next[0]
        col = next[1]

    for i in range(1,10):
        if sudoku_puzzle.valid_input(row, col, i):
            sudoku_puzzle.board[row][col] = i

            if backtracking_rec(sudoku_puzzle, heuristic, domains):
                return True

        sudoku_puzzle.board[row][col] = 0

    return False




###############################################################################
##                             Forward  Checking                             ##
###############################################################################
"""
forward_checking
Purpose:    Sets the domains of the board and runs a recursive forward checking
            algorithm
Parameters: sudoku_puzzle   [SudokuBoard],  The Board 
            heuristic       [function],     The search function to find the 
                                            next value
Returns:    Nothing
Effects:    The values in the board, and in the domains
Notes:      
"""
def forward_checking(sudoku_puzzle, heuristic):
    domains = set_domains(sudoku_puzzle)

    forward_checking_rec(sudoku_puzzle, heuristic, domains)


"""
forward_checking_rec
Purpose:    A recursive forwardchecking algorithm that returns false when a 
            domain is emptied by an assignment
Parameters: sudoku_puzzle   [SudokuBoard],  The Board 
            heuristic       [function],     The search function to find the 
                                            next value
            domains         [3D Array],     
Returns:    [bool], whether the current stateof the board can return a solution
Effects:    sudoku_puzzle, domains
Notes:      
"""
def forward_checking_rec(sudoku_puzzle, heuristic, domains):
    next = heuristic(sudoku_puzzle, domains)
    if (not next):
        return True
    else:
        sudoku_puzzle.unique_states += 1 

        row = next[0]
        col = next[1]
 
    for x in domains[row][col]:
        sudoku_puzzle.board[row][col] = x
        constrict_domains(sudoku_puzzle, row, col, x, domains)

        if (not empty_domain(sudoku_puzzle, domains)):
        
            if forward_checking_rec(sudoku_puzzle, heuristic, domains):
                return True

            
        sudoku_puzzle.board[row][col] = 0
        repair_domains(sudoku_puzzle, row, col, x, domains)
        
    return False




###############################################################################
##                               Conflict Sets                               ##
###############################################################################
"""
update_conflictsets
Purpose:    Given a position and number in the board update the conflict sets
            it affects
Parameters: sudoku_puzzle   [SudokuBoard],  The Board
            row             [int],          The row index of the most recently 
                                            inserted number
            col             [int],          The column index of the most 
                                            recently inserted num    
            domains         [3D Array],     The values for each position      
Returns:    Nothings
Effects:    SudokuPuzzle.conflictset
Notes:      
"""
def update_conflictsets(sudoku_puzzle, row, col, num, domains):
    update_box_conflictsets(sudoku_puzzle, row, col, num, domains)
    constrict_box_domains(sudoku_puzzle, row, col, num, domains)

    update_row_conflictsets(sudoku_puzzle, row, col, num, domains) 
    constrict_row_domains(sudoku_puzzle, row, col, num, domains)

    update_col_conflictsets(sudoku_puzzle, row, col, num, domains)
    constrict_col_domains(sudoku_puzzle, row, col, num, domains)


"""
update_box_conflictsets
Purpose:    Given a position and number in the box update the conflict sets
            it affects
Parameters: sudoku_puzzle   [SudokuBoard],  The Board
            row             [int],          The row index of the most recently 
                                            inserted number
            col             [int],          The column index of the most 
                                            recently inserted num    
            domains         [3D Array],     The values for each position      
Returns:    Nothings
Effects:    SudokuPuzzle.conflictset
Notes:      If the value is in the same box and the value is zero, that 
            conflict set will be updated.
"""
def update_box_conflictsets(sudoku_puzzle, row, col, num, domains):
    box_x = col // 3
    box_y = row // 3

    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if (num in domains[i][j] and [i,j] != [row, col] 
                and sudoku_puzzle.board[i][j] == 0):
                sudoku_puzzle.conflict_stacks[i][j].append([row, col])
                

"""
update_row_conflictsets
Purpose:    Given a position and number in a row update the conflict sets
            it affects
Parameters: sudoku_puzzle   [SudokuBoard],  The Board
            row             [int],          The row index of the most recently 
                                            inserted number
            col             [int],          The column index of the most 
                                            recently inserted num    
            domains         [3D Array],     The values for each position      
Returns:    Nothings
Effects:    SudokuPuzzle.conflictset
Notes:      If the value is in the same row and the value is zero, that 
            conflict set will be updated
"""
def update_row_conflictsets(sudoku_puzzle, row, col, num, domains):
    for j in range(len(sudoku_puzzle.board[row])):
        if (num in domains[row][j] and col != j
            and sudoku_puzzle.board[row][j] == 0):
            sudoku_puzzle.conflict_stacks[row][j].append([row, col])


"""
update_col_conflictsets
Purpose:    Given a position and number in a col update the conflict sets
            it affects
Parameters: sudoku_puzzle   [SudokuBoard],  The Board
            row             [int],          The row index of the most recently 
                                            inserted number
            col             [int],          The column index of the most 
                                            recently inserted num    
            domains         [3D Array],     The values for each position      
Returns:    Nothings
Effects:    SudokuPuzzle.conflictset
Notes:      If the value is in the column and the value is zero and the
            inserted number is in the positions domain, the conflict
            set will be updated 
"""
def update_col_conflictsets(sudoku_puzzle, row, col, num, domains):
    for i in range(len(sudoku_puzzle.board)):
        if (num in domains[i][col] and row != i 
            and sudoku_puzzle.board[i][col] == 0):
            sudoku_puzzle.conflict_stacks[i][col].append([row, col])


"""
repair_conflictset
Purpose:    After removing a value from the table, update every conflict set
            that the position was a part of 
Parameters: sudoku_puzzle   [SudokuBoard],  The Board
            row             [int],          The row index of the most recently 
                                            inserted number
            col             [int],          The column index of the most 
                                            recently inserted num   
Returns:    Nothing
Effects:    conflict_stacks
Notes:      
"""
def repair_conflictset(sudoku_puzzle, row, col):
    # [row, col] should be removed from all conflict stacks since it is no longer assigned

    for i in range(len(sudoku_puzzle.board)):
        for j in range(len(sudoku_puzzle.board[i])):
            if ([row,col] in sudoku_puzzle.conflict_stacks[i][j]):
                sudoku_puzzle.conflict_stacks[i][j].remove([row, col])




###############################################################################
##                               Back  Jumping                               ##
###############################################################################
"""
conflict_backjumping
Purpose:    Sets the domains given a board and run a recursive conflict-directed
            backjumping algorithm
Parameters: sudoku_puzzle   [SudokuBoard],  The Board 
            heuristic       [function],     The search function to find the 
                                            next value
Returns:    Nothing
Effects:    domains
Notes:      
"""
def conflict_backjumping(sudoku_puzzle, heuristic):
    domains = set_domains(sudoku_puzzle)

    conflict_backjumping_rec(sudoku_puzzle, heuristic, domains)


"""
conflict_backjumping_rec
Purpose:    When a domain is emptied, jump from the top of that conflict 
            set 
Parameters: sudoku_puzzle   [SudokuBoard],  The Board 
            heuristic       [function],     The search function to find the 
                                            next value
            domains         [3D Array],     The values for each position
Returns:    [bool] True if board works false otherwise
Effects:    sudoku_puzzle and domains
Notes:      
"""
def conflict_backjumping_rec(sudoku_puzzle, heuristic, domains):
    next = heuristic(sudoku_puzzle, domains)
    if not next:
        return True
    else:
        sudoku_puzzle.unique_states += 1 

        row = next[0]
        col = next[1]

    for x in domains[row][col]:
        #Insert value and update accordingly
        sudoku_puzzle.board[row][col] = x
        update_conflictsets(sudoku_puzzle, row, col, x, domains)
        
        empties = empty_domain(sudoku_puzzle, domains)
        if (not empties): 
            if(conflict_backjumping_rec(sudoku_puzzle, heuristic, domains)):
                return True
        else:
            # This assignment emptied a domain at empties[0], empties[1]
            backjump_from(sudoku_puzzle, empties[0], empties[1], domains)
        
        sudoku_puzzle.board[row][col] = 0
        repair_domains(sudoku_puzzle, row, col, x, domains)
        repair_conflictset(sudoku_puzzle, row, col)

        # We only get here if we are jumping up
        # Reset Domains and ConfSets below h
        if([row, col] != sudoku_puzzle.backjump):
            return False
    # We jumped back to this position and exhausted all possibilities
    # Domain exhausted
    backjump_from(sudoku_puzzle, row, col, domains)
    return False 


"""
backjump_from
Purpose:    Given a position in the board, pop the top of it's 
            conflict set and jump back to its position
Parameters: sudoku_puzzle   [SudokuBoard],  The Board
            row             [int],          The row index of the most recently 
                                            inserted number
            col             [int],          The column index of the most 
                                            recently inserted num    
            domains         [3D Array],     The values for each position 
Returns:    Nothings
Effects:    sudoku_puzzle.backjump
Notes:      
"""
def backjump_from(sudoku_puzzle, row, col, domains):
    # Jump to deepest var h in ConfSet[i]
    confset    = sudoku_puzzle.conflict_stacks[row][col]

    landing    = confset.pop()
    # Update ConfSet[h] with ConfSet[i]/h
    land_set = sudoku_puzzle.conflict_stacks[landing[0]][landing[1]]
    sudoku_puzzle.combine_conflicts(confset, land_set)
    sudoku_puzzle.backjump = landing
    confset = []

    # Move Forward

"""
parse_arguments
Purpose:    Parses arguments of the form: sudoku.py <board name>
Parameters: N/A
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


###############################################################################
##                              Actual  Program                              ##
###############################################################################

if __name__ == '__main__':
    start_time = time.time()
    
    board_name = parse_arguments()

    with open(board_name, 'r') as boards_file:
        game = SudokuBoard(boards_file)
        
        forward_checking(game, find_empty_basic)

        print("Unique States: ", game.unique_states)

        game.print_board()

        print("--- %s seconds ---" % round((time.time() - start_time), 3)) 