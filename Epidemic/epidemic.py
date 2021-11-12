# Etude 10: Epidemic
# Author: Jada Mataroa
# Student ID: 9474013
# Program that works out the final state of an epidemic in a grid-based universe.

import sys
import numpy as np


# Formats line of text into an array and calls functions
# on this array to find its final state.
def format(text):
    row = text.count("\n") + 1
    if row > 1:  # if grid is 2D
        col = text.index("\n")
        arr = np.empty([row, col], dtype=str)

        text = text.replace("\n", "")
        char = 0

        for i in range(row):  # formats text form into array
            for j in range(col):
                arr[i][j] = text[char]
                char += 1

        arr = state_2D(arr, row, col)  # calls function to find final state of 2D array

    else:
        col = len(text)
        arr = np.zeros(col, dtype=str)

        for _ in range(col):  # formats text form into array
            arr[_] = text[_]

        arr = state_1D(arr, col)  # calls function to find final state of 1D array

    return arr  # returns final state of input grid as an array


# Finds final state of 1D array grid.
def state_1D(arr, length):
    while True:  # loops until final state is found
        sick = 0
        for i in range(length):
            neighbours = ""
            if arr[i] == ".":  # check vulnerable individuals immediate neighbours for sickness
                if i - 1 >= 0:
                    neighbours += arr[i - 1]
                if i + 1 < len(arr):
                    neighbours += arr[i + 1]
                if neighbours.count("S") == 2:  # checks if two immediate neighbours are sick
                    arr[i] = "S"  # if so, change individual's status to sick
                    sick += 1
        if sick == 0:  # if no new individuals are sick breaks the loop as final state is found
            break

    return arr  # returns array in final state


# Finds final state of 2D array grid.
def state_2D(arr, row, col):
    while True:  # loops until final state is found
        sick = 0
        for i in range(row):
            for j in range(col):
                neighbours = ""
                if arr[i][j] == ".":  # check vulnerable individuals immediate neighbours for sickness
                    if i - 1 >= 0:
                        neighbours += arr[i - 1][j]
                    if i + 1 < row:
                        neighbours += arr[i + 1][j]
                    if j - 1 >= 0:
                        neighbours += arr[i][j - 1]
                    if j + 1 < col:
                        neighbours += arr[i][j + 1]
                    if neighbours.count("S") >= 2:  # checks if more two or more immediate neighbours are sick
                        arr[i][j] = "S"  # if so, change individual's status to sick
                        sick += 1
        if sick == 0:  # if no new individuals are sick breaks the loop as final state is found
            break

    return arr  # returns array in final state


# Reformat array back into text for correct output format
def reformat(arr):
    fin = ""
    if len(arr.shape) == 1:
        for _ in arr:
            fin += _
    else:
        row = len(arr)
        col = len(arr[0])

        for i in range(row):
            for j in range(col):
                fin += arr[i][j]
                if j+1 == col:
                    fin += "\n"

    return fin


results = []  # list of final states
grid = ""

# reads lines from stdin into grids
for line in sys.stdin:
    if line == "\n":  # if all lines of grid found
        grid = grid.strip()  # removes redundant newline
        array = format(grid)  # returns final state of universe as an array
        final = reformat(array)  # reformat array for correct output
        results.append(final)  # add final state to list
        grid = ""
    else:
        grid += line  # adds line of text to current grid


# repeats steps for last grid
grid = grid.strip()
array = format(grid)
final = reformat(array)
results.append(final)

print(*results, sep="\n\n")  # prints final states of each grid
