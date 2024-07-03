#  Tufts University COMP 131, Summer 2020
#  SudokuUI.py    
#  By:          Sawyer Bailey Paccione
#  Completed:   6/30/2020
#              
#  Description: The Graphical User Interface (GUI) representation of a Sudoku
#               Board. It can be played simply or it can be solved with a 
#               combination of Algorithms and Search Heuristics
#  Purpose:     The Tkinter UI, responsible for drawing the board and accepting 
#               user input.


from tkinter import Tk, Canvas, Frame, Button, BOTH, TOP, BOTTOM, Checkbutton, X, LEFT, RIGHT, IntVar

from RadioBar import RadioBar
import time
import solver

MARGIN = 20  # Pixels around the board
SIDE = 50  # Width of every board cell.
WIDTH = HEIGHT = MARGIN * 2 + SIDE * 9  # Width and height of the whole board

class SudokuUI(Frame):
    """
    __init__
    Purpose:    Initialize the Sudoku User Interface
    Parameters: parent  [tk.Frame],     The frame that the board should be 
                                        printed into 
                game    [SudokuBoard],  The sudokuboard
    Returns:    Nothings
    Effects:    Opens a window
    Notes:      
    """    
    def __init__(self, parent, game):
        self.game = game
        Frame.__init__(self, parent)
        self.parent = parent

        self.row, self.col = -1, -1

        self.__initUI()

    """
    __initUI
    Purpose:    Initialize the visual aspects of the UI
    Parameters: Nothing
    Returns:    Nothing
    Effects:    The Tkinter window
    Notes:      
    """
    def __initUI(self):
        self.parent.title("Sudoku")
        self.pack(fill=BOTH)
        self.canvas = Canvas(self,
                             width = WIDTH,
                             height = HEIGHT)
        self.canvas.pack(fill = BOTH, side = TOP)
        
        clear_button = Button(self,
                              text = "Clear answers",
                              command = self.__clear_answers)
        clear_button.pack(fill = BOTH, side = BOTTOM)

        self.__initSolvers()

        quit_button = Button(self, text = 'Quit', command = self.quit)
        quit_button.pack(fill = BOTH, side = BOTTOM)
        # Button(self, text='Show', command=var_states).pack()

        self.__draw_grid()
        self.__draw_puzzle()

        self.canvas.bind("<Button-1>", self.__cell_clicked)
        self.canvas.bind("<Key>", self.__key_pressed)

    """
    __initSolvers
    Purpose:    Initialize the algorithms, and heuristics radio bars and the
                solve button
    Parameters: Nothing
    Returns:    Nothing
    Effects:    The Tk UI of the sudoku window
    Notes:      
    """
    def __initSolvers(self):
        self.algo = RadioBar(self.parent, [('Back Tracking', 1), 
                                      ('Forward Checking', 2), 
                                      ('Back Jumping', 3)], "Algorithms:")
        self.heur = RadioBar(self.parent, [('Basic', 1), 
                                      ('Minimum Remaining Values', 2)], 
                                      "Search Heuristics:")

        self.algo.pack(side = TOP,  fill=X)
        self.heur.pack(side = BOTTOM)
        solve_button = Button(self.heur, text = 'Solve', 
                              command = self.__run_algorithm)
        solve_button.pack(side = BOTTOM)
        
        self.steps = IntVar()
        self.show_steps = Checkbutton(self.parent, 
                                 text = 'Show Steps',
                                 variable = self.steps)
        self.show_steps.pack(side = TOP)

    """
    __run_algorithm
    Purpose:    Given the input from the radio bar, run the appropriate
                algorithm/heuristic combinations
    Parameters: Nothing
    Returns:    Nothing
    Effects:    The board and window
    Notes:      
    """
    def __run_algorithm(self):
        self.__clear_answers()

        if (self.heur.v.get() == 1):
            heuristic = solver.find_empty_basic
        elif (self.heur.v.get() == 2):
            heuristic = solver.minimum_remaining_values

        domains = solver.set_domains(self.game)

        if (self.algo.v.get() == 1):
            if(self.__backtrackingUI(heuristic, domains)):
                self.__draw_solved()
        elif (self.algo.v.get() == 2):
            if(self.__forwardcheckingUI(heuristic, domains)):
                self.__draw_solved()
        elif (self.algo.v.get() == 3):
            if(self.__backjumpingUI(heuristic, domains)):
                self.__draw_solved()

    """
    __backtrackingUI
    Purpose:    Runs a simple backtracking algorithm
    Parameters: heuristic   [function], The search heuristic dictated by the 
                                        radio bar
                domains     [3D Array], The possible values of each positions 
                                        of the board given the constraints
    Returns:    [bool]  The success of values in the board
    Effects:    The sudoku board
    Notes:      
    """
    def __backtrackingUI(self, heuristic, domains):
        next = heuristic(self.game, domains)
        if not next:
            return True
        else:
            self.game.unique_states += 1 

            row = next[0]
            col = next[1]

        for i in range(1,10):
            self.game.board[row][col] = i
            
            if (self.steps.get() == 1):
                self.__draw_puzzle()
                self.update()
            if self.game.valid_input(row, col, i):
                if self.__backtrackingUI(heuristic, domains):
                    return True

            self.game.board[row][col] = 0
            if (self.steps.get() == 1):
                self.__draw_puzzle()
                self.update()

        return False

    """
    __forwardcheckingUI
    Purpose:    Runs the forwardchecking algorithm
    Parameters: heuristic   [function], The search heuristic dictated by the 
                                        radio bar
                domains     [3D Array], The possible values of each positions 
                                        of the board given the constraints
    Returns:    [bool]  The success of values in the board
    Effects:    The sudoku board
    Notes:      
    """
    def __forwardcheckingUI(self, heuristic, domains):
        next = heuristic(self.game, domains)
        if (not next):
            return True
        else:
            self.game.unique_states += 1 

            row = next[0]
            col = next[1]

            # print("Domain of ", row, col, domains[row][col])
    
        for x in domains[row][col]:
            solver.constrict_domains(self.game, row, col, x, domains)
            self.game.board[row][col] = x
            
            if (self.steps.get() == 1):
                self.__draw_puzzle()
                self.update()

            if (not solver.empty_domain(self.game, domains)):
                if self.__forwardcheckingUI(heuristic, domains):
                    return True

                
            self.game.board[row][col] = 0
            solver.repair_domains(self.game, row, col, x, domains)

            if (self.steps.get() == 1):
                self.__draw_puzzle()
                self.update()

        return False

    """
    __backjumpingUI
    Purpose:    Runs the conflicted backjumping algorithm
    Parameters: heuristic   [function], The search heuristic dictated by the 
                                        radio bar
                domains     [3D Array], The possible values of each positions 
                                        of the board given the constraints
    Returns:    [bool]  The success of values in the board
    Effects:    The sudoku board
    Notes:      
    """
    def __backjumpingUI(self, heuristic, domains):
        next = heuristic(self.game, domains)
        if not next:
            return True
        else:
            self.game.unique_states += 1 

            row = next[0]
            col = next[1]

        for x in domains[row][col]:
            #Insert value and update accordingly
            self.game.board[row][col] = x
            solver.update_conflictsets(self.game, row, col, x, domains)
            
            if (self.steps.get() == 1):
                self.__draw_puzzle()
                self.update()

            empties = solver.empty_domain(self.game, domains)
            if (not empties): 
                if(self.__backjumpingUI(heuristic, domains)):
                    return True
            else:
                # This assignment emptied a domain at empties[0], empties[1]
                solver.backjump_from(self.game, empties[0], empties[1], domains)
            
            self.game.board[row][col] = 0
            solver.repair_domains(self.game, row, col, x, domains)
            solver.repair_conflictset(self.game, row, col)

            if (self.steps.get() == 1):
                self.__draw_puzzle()
                self.update()

            # We only get here if we are jumping up
            # Reset Domains and ConfSets below h
            if([row, col] != self.game.backjump):
                return False
        # We jumped back to this position and exhausted all possibilities
        # Domain exhausted
        solver.backjump_from(self.game, row, col, domains)
        return False 

    """
    __draw_grid
    Purpose:    Draws grid divided with blue lines into 3x3 squares
    Parameters: Nothing
    Returns:    Nothing
    Effects:    The tkinter window
    Notes:      
    """
    def __draw_grid(self):
        for i in range(10):
            color = "blue" if i % 3 == 0 else "gray"

            x0 = MARGIN + i * SIDE
            y0 = MARGIN
            x1 = MARGIN + i * SIDE
            y1 = HEIGHT - MARGIN
            self.canvas.create_line(x0, y0, x1, y1, fill=color)

            x0 = MARGIN
            y0 = MARGIN + i * SIDE
            x1 = WIDTH - MARGIN
            y1 = MARGIN + i * SIDE
            self.canvas.create_line(x0, y0, x1, y1, fill=color)

    """
    __draw_puzzle
    Purpose:    Draws the values in the board 
    Parameters: Nothing
    Returns:    Nothing
    Effects:    The Tkinter Window
    Notes:      
    """
    def __draw_puzzle(self):
        self.canvas.delete("numbers")
        for i in range(9):
            for j in range(9):
                answer = self.game.board[i][j]
                if answer != 0:
                    x = MARGIN + j * SIDE + SIDE / 2
                    y = MARGIN + i * SIDE + SIDE / 2
                    original = self.game.start_board[i][j]
                    color = "black" if answer == original else "sea green"
                    self.canvas.create_text(
                        x, y, text=answer, tags="numbers", fill=color
                    )

    """
    __draw_cursor
    Purpose:    Draws red lines around the box that you selected
    Parameters: Nothing
    Returns:    Nothing
    Effects:    The Tkinter Window
    Notes:      
    """
    def __draw_cursor(self):
        self.canvas.delete("cursor")
        if self.row >= 0 and self.col >= 0:
            x0 = MARGIN + self.col * SIDE + 1
            y0 = MARGIN + self.row * SIDE + 1
            x1 = MARGIN + (self.col + 1) * SIDE - 1
            y1 = MARGIN + (self.row + 1) * SIDE - 1
            self.canvas.create_rectangle(
                x0, y0, x1, y1,
                outline="red", tags="cursor"
            )

    """
    __draw_victory
    Purpose:    Draws an orange circle that says victory
    Parameters: Nothing
    Returns:    Nothing
    Effects:    The Tkinter Window
    Notes:      
    """
    def __draw_victory(self):
        # create a oval (which will be a circle)
        x0 = y0 = MARGIN + SIDE * 2
        x1 = y1 = MARGIN + SIDE * 7
        self.canvas.create_oval(
            x0, y0, x1, y1,
            tags="victory", fill="dark orange", outline="orange"
        )
        # create text
        x = y = MARGIN + 4 * SIDE + SIDE / 2
        self.canvas.create_text(
            x, y,
            text="You win!", tags="victory",
            fill="white", font=("Arial", 32)
        )

    """
    __draw_solved
    Purpose:    Draws an orange circle that says victory
    Parameters: Nothing
    Returns:    Nothing
    Effects:    The Tkinter Window
    Notes:      
    """
    def __draw_solved(self):
        # create a oval (which will be a circle)
        self.__draw_puzzle()
        # x0 = y0 = MARGIN + SIDE * 2
        # x1 = y1 = MARGIN + SIDE * 7
        # self.canvas.create_oval(
        #     x0, y0, x1, y1,
        #     tags="victory", fill="DodgerBlue2", outline="navy"
        # )
        # # create text
        # x = y = MARGIN + 4 * SIDE + SIDE / 2
        # solved = "Solved: " + str(self.game.unique_states)
        # self.canvas.create_text(
        #     x, y,
        #     text= solved, tags="victory",
        #     fill="white", font=("Helvetica", 30)
        # )
        
        self.game.unique_states = 1

    """
    __cell_clicked
    Purpose:    Click the cell and represent it as clicked
    Parameters: event [x, y]    the X & Y coordinates of where exactly the user 
                                clicked
    Returns:    Nothing
    Effects:    Tkinter window, the current row and col
    Notes:      
    """
    def __cell_clicked(self, event):
        # if self.game.game_over:
        #     return
        x, y = event.x, event.y
        if (MARGIN < x < WIDTH - MARGIN and MARGIN < y < HEIGHT - MARGIN):
            self.canvas.focus_set()

            # get row and col numbers from x,y coordinates
            row, col = (y - MARGIN) // SIDE, (x - MARGIN) // SIDE

            # if cell was selected already - deselect it
            if (row, col) == (self.row, self.col):
                self.row, self.col = -1, -1
            elif self.game.board[row][col] == 0:
                self.row, self.col = row, col
        else:
            self.row, self.col = -1, -1

        self.__draw_cursor()

    """
    __key_pressed
    Purpose:    In the event a key is pressed, the value is inserted into the
                current cell if it is a digit
    Parameters: event [tk.event]
    Returns:    Nothing
    Effects:    The window
    Notes:      
    """
    def __key_pressed(self, event):
        # if self.game.game_over:
        #     return
        if self.row >= 0 and self.col >= 0 and event.char in "1234567890":
            self.game.board[self.row][self.col] = int(event.char)
            self.col, self.row = -1, -1
            self.__draw_puzzle()
            self.__draw_cursor()
            if self.game.check_win():
                self.__draw_victory()

    """
    __clear_answers
    Purpose:    Clear the values inserted to the board
    Parameters: Nothing
    Returns:    Nothing
    Effects:    tk Window
    Notes:      
    """
    def __clear_answers(self):
        self.game.start_over()
        self.canvas.delete("victory")
        self.__draw_puzzle()
