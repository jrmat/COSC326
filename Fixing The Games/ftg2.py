# Etude 02: Fixing the Games
# Author: Jada Mataroa
# ID: 9474013
# Finds and prints the results of a compressed single series of games between
# a number of players, where each player has a bye in a single round

import sys
import numpy as np


# Pushes double up number down in array
def push(arr, i):
    pushed = []
    listed = arr[i].tolist()
    double = []
    indexes = []
    [double.append(x) for x in listed if listed.count(x) == 2 and x not in double]  # double up number(s) in row i

    for d in double:
        indexes.append(np.where(arr[i] == d))  # indexes where double up occurs

    if len(double) != 1:
        if i == len(arr) - 1:
            ind = np.where(arr[i] == '')
            arr[i, ind[0]] = "_"
            return [arr]
        else:
            return pushed

    for item in indexes:
        for idx in range(2):
            ind = item[0][idx]  # index of double up

            ch = arr.copy()  # copies parent array to make child

            if "_" in ch[:, ind]:  # skips if player has already had a bye
                continue

            ch[i:, ind] = np.roll(ch[i:, ind], 1, axis=0)
            ch[i, ind] = "_"
            pushed.append(ch)

    return pushed


# checks stdin file has correct format
try:
    array = np.loadtxt(sys.stdin, dtype=int)  # loads stdin as integers into 2d numpy array
    cl = len(array)  # length of columns in array
    rl = len(array[0])  # length of rows
    if cl != rl - 1:
        print("Bad format")  # prints if column lengths aren't one more than row lengths
        sys.exit(1)
except ValueError:
    print("Bad format")  # prints if not all rows are the same length or non integer is read
    sys.exit(1)

# checks stdin file for bad values
if np.amax(array) != cl or np.amin(array) < 1 or len(set(array[0])) != rl-1:
    print("Bad values")
    sys.exit(1)

solutions = []  # list to contain solutions

array = array.astype(str)  # converts array to strings if correct format and values

row = np.full(rl, '', dtype=str)
array = np.vstack([array, row])  # adds extra empty row for double ups to be pushed down

solutions = [array]

for i in range(0, rl):
    a = []
    for sol in solutions:
        p = push(sol, i)
        if len(p) > 0:
            for q in p:
                a.append(q)

    solutions = a

if len(solutions) == 0:  # if no solutions found
    print("Inconsistent results")
    exit()


for sol in solutions:  # print all possible results
    for i in sol:
        for j in i:
            print(j, end=" ")
        print()
    print()

uniques = []

for sol in solutions:  # removes non unique solutions and adds them to uniques list
    if not any(np.array_equal(sol[np.argsort(sol[:, len(sol)-1])], u) for u in uniques):
        uniques.append(sol[np.argsort(sol[:, len(sol)-1])])


n = len(uniques)
print(f'Different results: {n}')
