# Etude 04: Pentominoes
# Authors:
# Jada Mataroa 9474013
# Levi Schimanski 6923634
# Harry Pittar 602423
# Trent Lim 5884658
# Part A: Class for our Pentomino structures


import numpy as np

# Pentomino shapes
O = np.array(
    [["O", "O", "O", "O", "O"]]
)

P = np.array(
    [
        ["P", "P"],
        ["P", "P"],
        ["P", "."]
    ]
)

Q = np.array(
    [
        ["Q", "Q"], 
        [".", "Q"],
        [".", "Q"],
        [".", "Q"],
    ]
)

R = np.array(
    [
        [".", "R", "R"],
        ["R", "R", "."],
        [".", "R", "."]
    ]
)

S = np.array(
    [
        [".", ".", "S", "S"],
        ["S", "S", "S", "."]
    ]
)

T = np.array(
    [
        ["T", "T", "T"],
        [".", "T", "."],
        [".", "T", "."]
    ]
)

U = np.array(
    [
        ["U", ".", "U"],
        ["U", "U", "U"],
    ]
)

V = np.array(
    [
         ["V", ".", "."],
         ["V", ".", "."],
         ["V", "V", "V"] 
        
    ]
)

W = np.array(
    [
        ["W", ".", "."],
        ["W", "W", "."],
        [".", "W", "W"]
    ]
)

X = np.array(
    [
        [".", "X", "."],
        ["X", "X", "X"],
        [".", "X", "."]
    ]
)

Y = np.array(
    [
        [".", "Y"],
        ["Y", "Y"],
        [".", "Y"],
        [".", "Y"]
    ]
)

Z = np.array(
    [
        ["Z", "Z", "."],
        [".", "Z", "."],
        [".", "Z", "Z"]
    ]
)

# Dictionary of letters to shapes
shapes = {
    "O": O,
    "P": P,
    "Q": Q,
    "R": R,
    "S": S,
    "T": T,
    "U": U,
    "V": V,
    "W": W,
    "X": X,
    "Y": Y,
    "Z": Z,
}


class Pentomino(object):
    def __init__(self, letter):
        self.letter = letter

    @property
    def shape(self):
        self._shape = shapes[self.letter]
        return self._shape
