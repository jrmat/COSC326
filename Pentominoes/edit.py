import numpy as np
import sys
from Pentomino import Pentomino
import multiprocessing as mp

grid = []
pieces = []


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


def all_pos(P, board):
    bRow = len(board)
    bCol = len(board[0])
    ind = np.where(board == "*")

    if ind[0].size == 0:
        for p in possible_orientations(P):
            rows = len(p)
            cols = len(p[0])

            for r in range(bRow + 1 - rows):
                for c in range(bCol + 1 - cols):
                    b = board.copy()
                    b[r:r + rows, c:c + cols] = p
                    yield b

    else:
        letter = P.letter
        for p in possible_orientations(P):
            rows = len(p)
            cols = len(p[0])

            for r in range(bRow + 1 - rows):
                for c in range(bCol + 1 - cols):
                    b = board.copy()
                    b[r:r + rows, c:c + cols] = p
                    if b[ind[0], ind[1]] == letter:  # skips over invalid pieces
                        continue
                    b[ind[0], ind[1]] = "*"
                    yield b


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
                print(combined, "\n")
                solved = solve(combined, left)
                if solved is not None:
                    return solved
    return None


# Returns board if given piece fits,
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

        b[row, col] = arr[c[0], c[1]]

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
    # Open file and read to grid
    file_name = sys.argv[-1]
    f = open(file_name, "r")
    grid = f.read().splitlines()

    # Get pieces and repeat boolean from first line of input
    pieces_to_use = grid.pop(0)
    pieces_to_use = list(pieces_to_use)
    if pieces_to_use[len(pieces_to_use) - 1] == "*":
        repeat = True
        pieces_to_use.remove("*")

    # Add shapes to list of pieces
    for i in pieces_to_use:
        piece = Pentomino(i)
        pieces.append(piece)

    # Convert grid into numpy array
    grid = [list(i) for i in grid]
    grid = np.array(grid)

    # Remove O shape from pieces if the grid is smaller than 4x4 as it won't fit
    if len(grid) < 5 and len(grid[0]) < 5:
        pieces = [piece for piece in pieces if piece.letter != "O"]

    perm = []
    P = pieces[3]
    pieces.remove(P)
    for a in all_pos(P, grid):
        perm.append(a)

    pool = mp.Pool(mp.cpu_count())
    results = pool.starmap(solve, [(p, pieces) for p in perm])

    pool.close()

    solution = [r for r in results if results is not None]

    if solution is None:
        print("No solution")
        exit()

    for i in solution[0]:
        for j in i:
            print(j, end=" ")
        print()
