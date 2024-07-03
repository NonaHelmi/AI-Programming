import numpy as np
import time
import copy

start_time = time.time()
end_time = 0
backtracks = 0
recursion_count = 0
peer_dict = {}
row_list = []
col_list = []
square_list = []
unit_list = []

# #easy
# sudoku = [['7', '9', '0', '4', '0', '2', '3', '8', '1'],
#           ['5', '0', '3', '0', '0', '0', '9', '0', '0'],
#           ['0', '0', '0', '0', '3', '0', '0', '7', '0'],
#           ['0', '0', '0', '0', '0', '5', '0', '0', '2'],
#           ['9', '2', '0', '8', '1', '0', '7', '0', '0'],
#           ['4', '6', '0', '0', '0', '0', '5', '1', '9'],
#           ['0', '1', '0', '0', '0', '0', '2', '3', '8'],
#           ['8', '0', '0', '0', '4', '1', '0', '0', '0'],
#           ['0', '0', '9', '0', '8', '0', '1', '0', '4']]
#hard
# sudoku = [['8', '0', '0', '0', '0', '0', '0', '0', '0'],
#           ['0', '0', '3', '6', '0', '0', '0', '0', '0'],
#           ['0', '7', '0', '0', '9', '0', '2', '0', '0'],
#           ['0', '5', '0', '0', '0', '7', '0', '0', '0'],
#           ['0', '0', '0', '0', '4', '5', '7', '0', '0'],
#           ['0', '0', '0', '1', '0', '0', '0', '3', '0'],
#           ['0', '0', '1', '0', '0', '0', '0', '6', '8'],
#           ['0', '0', '8', '5', '0', '0', '0', '1', '0'],
#           ['0', '9', '0', '0', '0', '0', '4', '0', '0']]
#super hard
sudoku = [['0', '6', '1', '0', '0', '7', '0', '0', '3'],
          ['0', '9', '2', '0', '0', '3', '0', '0', '0'],
          ['0', '0', '0', '0', '0', '0', '0', '0', '0'],
          ['0', '0', '8', '5', '3', '0', '0', '0', '0'],
          ['0', '0', '0', '0', '0', '0', '5', '0', '4'],
          ['5', '0', '0', '0', '0', '8', '0', '0', '0'],
          ['0', '4', '0', '0', '0', '0', '0', '0', '1'],
          ['0', '0', '0', '1', '6', '0', '8', '0', '0'],
          ['6', '0', '0', '0', '0', '0', '0', '0', '0']]

print(np.matrix(sudoku))


def get_unit_list():
    global unit_list
    global row_list
    global col_list
    global square_list
    for y in range(0, 9):
        row_list_tmp = []
        col_list_tmp = []

        for x in range(0, 9):
            rowpos = [y, x]
            colpos = [x, y]
            row_list_tmp.append(tuple(rowpos))
            col_list_tmp.append(tuple(colpos))

        row_list.append(row_list_tmp)
        col_list.append(col_list_tmp)

    for x in range(0, 9, 3):
        for y in range(0, 9, 3):
            square_list_tmp = []
            x0 = (x // 3) * 3  # top left position in box
            y0 = (y // 3) * 3
            for i in range(3):
                for j in range(3):
                    grid = [y0 + i, x0 + j]
                    square_list_tmp.append(tuple(grid))
            square_list.append(square_list_tmp)
    unit_list = row_list + col_list + square_list


# sudoku[linha][coluna]
def fill_matrix():
    for i in range(0, 9):
        for j in range(0, 9):
            if sudoku[i][j] == '0':
                sudoku[i][j] = '123456789'


def find_peers():
    global peer_dict
    for y in range(0, 9):
        for x in range(0, 9):
            pos = [y, x]
            peer_list = []
            for peer_pos in range(0, 9):
                row = [peer_pos, x]
                col = [y, peer_pos]
                if row != pos:
                    peer_list.append(row)
                if col != pos:
                    peer_list.append(col)

            x0 = (x // 3) * 3  # top left position in box
            y0 = (y // 3) * 3
            for i in range(3):
                for j in range(3):
                    grid = [y0 + i, x0 + j]
                    if grid != pos:
                        peer_list.append(grid)

            i = 0
            peer_set = set(tuple(i) for i in peer_list)
            peer_list = list(peer_set)
            peer_dict[tuple(pos)] = peer_list
    print("Finished Peer List")


def eliminate(matrix_sudoku):
    solved_list = []
    # iterate through solved values and keep position in a list
    for position_key in peer_dict:
        y = position_key[0]
        x = position_key[1]
        if len(matrix_sudoku[y][x]) == 1:
            position = [y, x]
            solved_list.append(position)

    for solved_pos in solved_list:
        y = solved_pos[0]
        x = solved_pos[1]
        digit = matrix_sudoku[y][x]

        for peer in peer_dict[tuple(solved_pos)]:
            y = peer[0]
            x = peer[1]
            matrix_sudoku[y][x] = matrix_sudoku[y][x].replace(digit, '')
    return matrix_sudoku


def hidden_single(matrix_sudoku):
    for unit in unit_list:
        for digit in '123456789':
            boxes_with_digit = []
            for box in unit:
                y = box[0]
                x = box[1]
                if digit in matrix_sudoku[y][x]:
                    position = [y, x]
                    boxes_with_digit.append(tuple(position))
            if len(boxes_with_digit) == 1:
                y, x = boxes_with_digit[0]
                matrix_sudoku[y][x] = digit
    return matrix_sudoku


def reduce_sudoku(matrix_sudoku):
    global peer_dict
    global backtracks
    stalled = False
    while not stalled:
        # need to count how many values are already solved
        solved_values_before = 0
        for position_key in peer_dict:
            y = position_key[0]
            x = position_key[1]
            if len(matrix_sudoku[y][x]) == 1:
                solved_values_before = solved_values_before + 1

        # use eliminate strategy
        matrix_sudoku = eliminate(matrix_sudoku)
        # use hidden single strategy
        matrix_sudoku = hidden_single(matrix_sudoku)
        # count how many boxes have been solved after trying the two strategies
        solved_values_after = 0
        for position_key in peer_dict:
            y = position_key[0]
            x = position_key[1]
            if len(matrix_sudoku[y][x]) == 1:
                solved_values_after = solved_values_after + 1

        stalled = solved_values_before == solved_values_after
        # check if there are any boxes with zero possibilities (sanity check)
        # if there is an error backtracking is applied
        for position_key in peer_dict:
            y = position_key[0]
            x = position_key[1]
            if len(matrix_sudoku[y][x]) == 0:
                backtracks = backtracks + 1
                return False
    return matrix_sudoku


def search(matrix_sudoku):  # bruteforce search
    global recursion_count
    global backtracks
    global peer_dict
    matrix_sudoku = reduce_sudoku(matrix_sudoku)
    if matrix_sudoku is False:
        return False  # Failed earlier

    list_of_lenghts = []
    for position_key in peer_dict:
        y = position_key[0]
        x = position_key[1]
        list_of_lenghts.append(len(sudoku[y][x]))

    if all(list_of_lenghts[i] == 1 for i in range(len(list_of_lenghts))):
        print(np.matrix(matrix_sudoku))
        return matrix_sudoku ## Solved

    ##find unfilled squares with the fewest possibilities
    unfilled_squares = {}
    for position_key in peer_dict:
        y = position_key[0]
        x = position_key[1]
        if len(matrix_sudoku[y][x]) > 1:
            position = [y, x]
            unfilled_squares[tuple(position)] = len(matrix_sudoku[y][x])
    min = 99
    for key, value in unfilled_squares.items():
        if value < min:
            min = value
            pos_min = key
            # y = pos_min[0]
            # x = pos_min[1]
    print(np.matrix(matrix_sudoku))
    print("Backtracks {}".format(backtracks))
    print("Recursions {}".format(recursion_count))
    end_time = time.time()
    print("Solve time:{} ms ".format((end_time - start_time) * 1000))

    # recursion to solve sudoku when the other strategies dont find any new boxes
    y = pos_min[0]
    x = pos_min[1]

    for possibility in matrix_sudoku[y][x]:
        new_matrix = copy.deepcopy(matrix_sudoku)
        new_matrix[y][x] = possibility
        recursion_count = recursion_count + 1
        attempt = search(new_matrix)
        if attempt:
            return attempt


def start_solving(sudoku):
    global end_time
    global start_time
    global backtracks
    global recursion_count
    get_unit_list()
    find_peers()
    fill_matrix()
    solved_sudoku = search(sudoku)
    print(np.matrix(solved_sudoku))
    print("Backtracks {}".format(backtracks))
    print("Recursions {}".format(recursion_count))
    end_time = time.time()
    print("Solve time:{} ms ".format((end_time - start_time) * 1000))


start_solving(sudoku)
