# Etude 03: Finding Anagrams
# Authors:
# Jada Mataroa 9474013
# Levi Schimanski 6923634
# Program that finds best anagrams given a dictionary and a string.
import itertools
import sys
from collections import Counter


# Reduces dictionary down to words that are able to
# make an anagram of the input word.
def reduce(inWord, dict):
    reduced = []
    counterList = []
    wCount = Counter(inWord[0])

    w = "".join(set(inWord[0]))  # remove duplicate letters for checking against anagram
    dict.sort()  # sorts dictionary into alphabetical order

    for d in dict:
        for item in d:
            if Counter(item) & wCount == Counter(item) and Counter(item) not in counterList:
                counterList.append(Counter(item))
                reduced.append(item)
    return reduced


# Finds best anagram for given word
# w = given word
# dict = dictionary for potential anagrams
# a = alphabet string
# p = prime number string
def find(w, dict):
    target = Counter(w[0])

    if target == Counter(dict[0]):
        anagram = [dict[0]]
        return anagram

    for i in range(len(dict)):
        t = target - Counter(dict[i])
        anagram = check(t, dict, i)
        if anagram is not None:
            anagram.insert(0, dict[i])
            return anagram

    anagram = []  # returns empty list if no anagram found
    return anagram


# Recursively checks for multiples that reach target number
def check(target, d, i):
    for j in range(i+1, len(d)):
        c = Counter(d[j])
        if c == target:
            a = [d[j]]
            return a
        if c & target == c:
            rest = target - c
            a = check(rest, d, j)
            if a is not None:
                a.insert(0, d[j])
                return a
    return None


words = []  # list of words to find anagrams
dictionary = []  # list of dictionary words

# reads lines from stdin into list
for line in sys.stdin:
    if not line.strip():
        words = dictionary.copy()
        dictionary = []
        continue
    dictionary.append(line.split())

pot = []  # list for potential words as anagrams for a given word

for word in words:
    pot = reduce(word, dictionary)  # find list of potential words for anagram
    pot.sort(key=len, reverse=True)  # sorts list by word length
    if len(pot) > 0:
        anagrams = find(word, pot)
    else:
        anagrams = []
    s1 = "".join(word)  # formats word for printing
    s2 = " ".join([str(item) for item in anagrams])  # formats anagram words for printing
    print(f'{s1}: {s2}')  # print word and its anagram if found
