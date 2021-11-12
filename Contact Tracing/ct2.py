# Etude 12: Contact Tracing
# Authors:
# Jada Mataroa 9474013
# Levi Schimanski 6923634
# Program that:
# 1. Finds all other persons who contacted a person (A) after a particular time (T)
# 2. Finds out all other persons who are likely to get a contagious magic power, from
# a given group of persons with the magic power with their times of empowerment.

import sys
import threading
import time
from astropy.table import Table
import numpy as np

traces = []  # list for contact traces


# For a particular person = A,
# after a particular time = T,
# find all other persons who contacted A
# > adds C[0] if person contacted A
# > adds C[1] if A contacted person
def contacts(A, T, contact, persons):
    for C in contact:
        if C[1] == A and C[2] > T:
            if C[0] not in persons:
                persons.append(C[0])
        if C[0] == A and C[2] > T:
            if C[1] not in persons:
                persons.append(C[1])


# Finds all persons at risk of getting 'magic power'
# Calculates their likelihood of being empowered
# empowered = list of persons with magic power and their time of empowerment
# traced = list of contact traces
# magiNum = list of id's of those with magic power
# returns double columned list where:
# first column = PID of at risk persons
# second column = probability of that person getting magic power
def likelihood(empowered, traced, magicNum):
    traced = sorted(traced, key=lambda x: x[2])  # sort by time
    persons = []  # list of those at risk of getting magic power
    probability = []  # list of probability those at risk have of getting 'magic power'

    for e in empowered:
        lh = 0.1

        degree = []
        z = 0
        for i in range(5):
            degree.append([z])

        contacted = []

        split = 0

        for t in traced:
            if t[2] >= e[1]:
                split = traced.index(t)
                break

        check = traced[split:].copy()  # shortens list to skip over data before empowered time

        for c in check:
            if c[0] in degree[4] or c[1] in degree[4]:  # skips if chain will be longer than 5
                continue

            if c[0] == e[0]:  # if direct contact found
                if c[1] in magicNum:
                    continue
                if c[1] not in contacted:
                    contacted.append(c[1])
                    degree[0].append(c[1])
                if c[1] not in persons:
                    persons.append(c[1])
                    probability.append(lh)
                    continue
                index = persons.index(c[1])
                probability[index] += lh
                continue

            if c[1] == e[0]:
                if c[0] in magicNum:
                    continue
                if c[0] not in contacted:
                    contacted.append(c[0])
                    degree[0].append(c[0])
                if c[0] not in persons:
                    persons.append(c[0])
                    probability.append(lh)
                    continue
                index = persons.index(c[0])
                probability[index] += lh
                continue

            if c[0] in magicNum or c[1] in magicNum:  # if contact already empowered skip as will be/has been considered
                continue

            if c[0] in contacted:  # if person has been contacted to some degree
                if c[1] not in contacted:
                    contacted.append(c[1])
                    for d in range(len(degree)-1):
                        if c[0] in degree[d]:
                            degree[d+1].append(c[1])
                            if c[1] not in persons:
                                persons.append(c[1])
                                probability.append(lh**(d+2))
                                continue
                            index = persons.index(c[1])
                            probability[index] += lh**(d+2)
                continue
            if c[1] in contacted:
                if c[0] not in contacted:
                    contacted.append(c[0])
                    for d in range(len(degree)-1):
                        if c[1] in degree[d]:
                            degree[d+1].append(c[0])
                            if c[0] not in persons:
                                persons.append(c[0])
                                probability.append(lh**(d+2))
                                continue
                            index = persons.index(c[0])
                            probability[index] += lh**(d+2)

    return list(zip(persons, probability))


if __name__ == "__main__":
    # reads lines from stdin into list
    for line in sys.stdin:
        data = []  # data in line

        for info in line.split():  # formats line into list
            data.append(int(info))

        traces.append(data)  # add person's contact trace to list

    personContacted = 0
    timeAfter = 0

    n = len(sys.argv)

    for i in range(1, n, n):
        personContacted = int(sys.argv[i])
        timeAfter = int(sys.argv[i+1])

    maxThreads = 4  # maximum amount of processes to run
    number = []
    times = []

    for i in range(1, maxThreads + 1):
        jobs = []
        results = []

        thread = threading.Thread(target=contacts(personContacted, timeAfter, traces, results))
        jobs.append(thread)

        start = time.process_time()
        for j in jobs:
            j.start()

        for j in jobs:
            j.join()
        end = time.process_time()
        timed = end - start

        number.append(i)  # adds number of processes to list
        times.append(timed)  # adds time taken for this number processes to complete task

    print('\033[1m' + f"Person(s) who contacted person with ID = {personContacted} "
                      f"after time of {timeAfter}:" + '\033[0m')

    print(results, "\n")  # prints results from contact method

    # writes time and process number data to table in  csv file
    data = Table()
    data['Number of threads'] = number
    data['Process time taken (s)'] = times
    data.write('values.csv', overwrite=True)

    contagious = []  # list of empowered individuals and their time of empowerment
    n = len(sys.argv)

    for i in range(3, n, 2):
        contagious.append([int(sys.argv[i]), int(sys.argv[i+1])])

    c = np.array(contagious.copy())
    magic = list(c[:, 0])

    atRisk = likelihood(contagious, traces, magic)

    print('\033[1m' + "Person(s) at risk and their probabilities of getting 'magic power'" + '\033[0m')
    for a in atRisk:
        print(f"PID: {a[0]}\t Probability: {a[1]}")  # prints people(s) at risk and their probabilities
