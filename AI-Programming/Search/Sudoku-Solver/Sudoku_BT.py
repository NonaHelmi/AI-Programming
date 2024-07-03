import numpy as np
import time
import sys

start_time = time.time()
end_time = 0
backtrack = 0
recursions = 0
# easy
# sudoku = [[7, 9, 0, 4, 0, 2, 3, 8, 1],
#           [5, 0, 3, 0, 0, 0, 9, 0, 0],
#           [0, 0, 0, 0, 3, 0, 0, 7, 0],
#           [0, 0, 0, 0, 0, 5, 0, 0, 2],
#           [9, 2, 0, 8, 1, 0, 7, 0, 0],
#           [4, 6, 0, 0, 0, 0, 5, 1, 9],
#           [0, 1, 0, 0, 0, 0, 2, 3, 8],
#           [8, 0, 0, 0, 4, 1, 0, 0, 0],
#           [0, 0, 9, 0, 8, 0, 1, 0, 4]]
##hard
# sudoku = [[8, 0, 0, 0, 0, 0, 0, 0, 0],
#           [0, 0, 3, 6, 0, 0, 0, 0, 0],
#           [0, 7, 0, 0, 9, 0, 2, 0, 0],
#           [0, 5, 0, 0, 0, 7, 0, 0, 0],
#           [0, 0, 0, 0, 4, 5, 7, 0, 0],
#           [0, 0, 0, 1, 0, 0, 0, 3, 0],
#           [0, 0, 1, 0, 0, 0, 0, 6, 8],
#           [0, 0, 8, 5, 0, 0, 0, 1, 0],
#           [0, 9, 0, 0, 0, 0, 4, 0, 0]]


# super hard
# sudoku = [[0, 6, 1, 0, 0, 7, 0, 0, 3],
#           [0, 9, 2, 0, 0, 3, 0, 0, 0],
#           [0, 0, 0, 0, 0, 0, 0, 0, 0],
#           [0, 0, 8, 5, 3, 0, 0, 0, 0],
#           [0, 0, 0, 0, 0, 0, 5, 0, 4],
#           [5, 0, 0, 0, 0, 8, 0, 0, 0],
#           [0, 4, 0, 0, 0, 0, 0, 0, 1],
#           [0, 0, 0, 1, 6, 0, 8, 0, 0],
#           [6, 0, 0, 0, 0, 0, 0, 0, 0]]





def valid(y, x, n):
    global sudoku
    for i in range(9):
        if n == sudoku[y][i]:
            return False
    for i in range(9):
        if n == sudoku[i][x]:
            return False
    x0 = (x // 3) * 3
    y0 = (y // 3) * 3
    for i in range(3):
        for j in range(3):
            if sudoku[y0 + i][x0 + j] == n:
                return False
    return True


def solve():
    global sudoku
    global backtrack
    global recursions
    for y in range(0, 9):
        for x in range(0, 9):  # for the first
            if sudoku[y][x] == 0:  # empty slot found:
                for n in range(1, 10):  # try 1..9
                    if valid(y, x, n):
                        sudoku[y][x] = n
                        recursions = recursions + 1
                        solve()  # and recurse
                sudoku[y][x] = 0
                backtrack = backtrack + 1  # restore
                return  # and return
    # no empty slots were found:
    #   we're at the deepest level of recursion and
    #   there are no more slots to fill:
    print("Solved!")
    print(np.matrix(sudoku))
    global end_time
    end_time = time.time()
    print("Solve time:{} ms ".format((end_time - start_time) * 1000))
    print("backtracks: {}".format(backtrack))
    print("recursions:{}".format(recursions))
    sys.exit()
    return


solve()
# //////////////////////////////////////////////////
