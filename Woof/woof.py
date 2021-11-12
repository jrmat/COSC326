# Etude 08: Woof
# Author: Jada Mataroa
# Student ID: 9474013
# Program that reads a line of text and prints "woof" or "not woof",
# depending on whether or not the line typed was woof.
import sys
import re

for inp in sys.stdin:
    inp = inp.rstrip()  # removes blank line from input

    # recursively replaces all woof or leader conditions with <w> or <l> respectively
    while True:
        recur = re.sub(r"[CAKE]", "<l>", inp)  # replaces <leader> condition with <l>
        recur = re.sub(r"[pqrs]", "<w>", recur)  # replaces <woof> condition with <w>
        recur = re.sub(r"N*<w>", "<w>", recur)  # replaces N<woof> condition with <w>
        recur = re.sub("<l><w><w>", "<w>", recur)  # replaces <leader><woof><woof> condition with <w>
        if recur == inp:
            break
        inp = recur

    # prints whether line typed is woof or not
    if re.fullmatch("<w>", inp):
        print("woof")
    else:
        print("not woof")
