# Etude 04: Pentominoes
# Authors:
# Jada Mataroa 9474013
# Levi Schimanski 6923634
# Harry Pittar 602423
# Trent Lim 5884658
# Part B: Solver for Pentominoes

import numpy as np
import sys
from Pentomino import Pentomino

grid = []
pieces = []
repeat = False


# Finds all possible orientations of a Pentomino = P
def possible_orientations(P):
    ori = []
    for P in (P.shape, P.shape.T):
        for P in (P, np.fliplr(P)):
            for P in (P, np.flipud(P)):
                s = str(P)
                if s not in ori:
                    yield P
                    ori.append(s)


# Recursively solves board for no repeat shape puzzle
# board = puzzle board so far
# inPieces = letters of pieces left to be used
def solve(board, inPieces):
    if (board == ".").sum() == 0:
        return board

    start = np.argwhere(board == ".")
    x = start[0][0]
    y = start[0][1]

    for index in range(len(inPieces)):
        p = inPieces[index]
        for o in possible_orientations(p):
            combined = combine(board, o, p.letter, x, y)
            if combined is not None:
                left = inPieces.copy()
                left.remove(p)
                solved = solve(combined, left)
                if solved is not None:
                    return solved
    return None


# Recursively solves board for no repeat shape puzzle
# board = puzzle board so far
# inPieces = letters of pieces left to be used
def repeatSolve(board, inPieces):
    if (board == ".").sum() == 0:
        return board

    start = np.argwhere(board == ".")
    x = start[0][0]
    y = start[0][1]

    for index in range(len(inPieces)):
        p = inPieces[index]
        for o in possible_orientations(p):
            combined = combine(board, o, p.letter, x, y)
            if combined is not None:
                left = inPieces.copy()
                solved = repeatSolve(combined, left)
                if solved is not None:
                    return solved
    return None


# Returns board if given piece fits and doesn't create hole,
# else returns None
def combine(board, arr, letter, x, y):
    cross = np.argwhere(arr == letter)
    start = cross[0]
    offset = start[1]
    b = board.copy()

    for c in cross:
        row = x + c[0]
        col = y + c[1] - offset

        if row >= len(b) or col >= len(b[0]) or col < 0:
            return None

        if b[row, col] != ".":
            return None

        b[row, col] = arr[c[0], c[1]]  # pieces not attaching correctly

    dot = np.argwhere(b == ".")

    for d in dot:
        neighbours = ""
        if d[0] - 1 >= 0:
            neighbours += b[d[0] - 1][d[1]]
        if d[0] + 1 < len(b):
            neighbours += b[d[0] + 1][d[1]]
        if d[1] - 1 >= 0:
            neighbours += b[d[0]][d[1] - 1]
        if d[1] + 1 < len(b[0]):
            neighbours += b[d[0]][d[1] + 1]
        if neighbours.count(".") == 0:
            return None

    return b


if __name__ == "__main__":
    # Read file to grid
    for line in sys.stdin:
        grid.append(line.split()[0])

    # Get pieces and repeat boolean from first line of input
    pieces_to_use = grid.pop(0)
    echo1 = pieces_to_use

    pieces_to_use = list(pieces_to_use)
    if pieces_to_use[len(pieces_to_use) - 1] == "*":
        repeat = True
        pieces_to_use.remove("*")

    order = ["X", "O", "Z", "V", "W", "T", "U", "R", "Q", "S", "P", "Y"]
    ordered_pieces = []  # pieces to use in order of least to most orientations

    for o in order:
        if o in pieces_to_use:
            for i in range(pieces_to_use.count(o)):
                ordered_pieces.append(o)

    # Add shapes to list of pieces
    for i in ordered_pieces:
        piece = Pentomino(i)
        pieces.append(piece)

    # Convert grid into numpy array
    grid = [list(i) for i in grid]
    grid = np.array(grid)
    echo2 = grid.copy()

    # Remove O shape from pieces if the grid is smaller than 4x4 as it won't fit
    if len(grid) < 5 and len(grid[0]) < 5:
        pieces = [piece for piece in pieces if piece.letter != "O"]

    if repeat:
        solution = repeatSolve(grid, pieces)
    else:
        solution = solve(grid, pieces)

    if solution is None:
        print(echo1, "\n")
        for i in echo2:
            for j in i:
                print(j, end=" ")
            print()
        print()
        print("Impossible")  # prints if no solution found
        exit()

    print(echo1, "\n")
    for i in solution:
        for j in i:
            print(j, end=" ")
        print()
