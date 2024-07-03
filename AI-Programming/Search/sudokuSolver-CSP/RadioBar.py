#  Tufts University COMP 131, Summer 2020
#  RadioBar.py    
#  By:          Sawyer Bailey Paccione
#  Completed:   6/30/2020
#              
#  Description: A collection of Radio Buttons all indicating various options
#               for the same value
#  Purpose:     Combine Multiple Radio Buttons together 

from tkinter import RADIOBUTTON, Frame, LEFT, W, IntVar, YES, Radiobutton, Label

class RadioBar(Frame):
    """
    __init__
    Purpose:    Initialize the values in the RadioBar
    Parameters: parent  [Tk.Frame], The Frame the Radio Bar should be a part of
                picks   [list[]],   A list of text, mode values 
                group   [string],   Title of the RadioBar
                side    [Tk.side],  Determines which side of the parent widget 
                                    packs against: TOP (default), BOTTOM, LEFT, 
                                    or RIGHT.
                anchor  [Tk.anchor],Anchors are used to define where text is 
                                    positioned relative to a reference point.

    Returns:    Nothings
    Effects:    The parent Frame
    Notes:      
    """
    def __init__(self, parent = None, picks = [], group = "Title:", 
                 side = LEFT, anchor = W):
        Frame.__init__(self, parent)
        Label(self, text = group).pack()
      
        self.v = IntVar()
        self.v.set(1)

        for text, mode in picks:
            rad = Radiobutton(self, text = text, variable = self.v, value = mode)
            rad.pack(side = side, anchor = anchor, expand = YES)
