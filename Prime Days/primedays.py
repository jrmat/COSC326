# Etude 05: Prime Days
# Author: Jada Mataroa
# Student ID: 9474013
# Program that computes all the truly prime days of a year given only the lengths of the months

import sys
import sympy as sp

month_lengths = []  # list to hold input month lengths
n = len(sys.argv)

for i in range(1, n):
    month_lengths.append(int(sys.argv[i]))  # appends input months as integers to list

day = 1  # counter for day of year

for month, ml in enumerate(month_lengths, start=1):
    if not sp.isprime(month):
        day += ml
        continue

    day_count = 1  # counter for day of month
    while day_count <= ml:  # iterates over days part of current month
        if sp.isprime(day) & sp.isprime(month) & sp.isprime(day_count):  # checks if day is truly prime
            print(f'{day}: {month} {day_count}')

        day_count += 1  # increment to next day of month
        day += 1  # increment to next day of year
