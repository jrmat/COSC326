# Etude 06: What's your preference?
# Author: Jada Mataroa
# Student ID: 9474013
# Program that determines a winner/'president' from a voting pool.

import sys
from collections import Counter


# Returns list of candidate names in order of votes received in round,
# lowest voted candidate name, results to be archived for tiebreaks,
# and whether there's a tie this round.
def v_count(poll, inAll, round_num):
    vf = []  # list of names voted for
    zero = []  # list of candidates with 0 votes this round
    tied = False  # boolean as to whether a tie has occurred or not
    order = []  # list of voted names in order

    for p in poll:
        vf.append(p[0])

    vf = sorted(vf)  # sorts list in alphabetical order

    count = Counter(vf)

    print("\nRound " + str(round_num))  # print round number

    for n, c in count.most_common():  # print results
        order.append(n)
        print(n.ljust(FORM) + f'{c}')

    for cand in inAll:
        if cand not in count:  # print 0 vote results
            print(cand.ljust(FORM) + "0")
            zero.append(cand)

    total_votes = sum(count.values())

    for n, c in count.most_common(1):  # if the highest voted as over 50% of votes declare outright winner
        if c > total_votes / 2:
            print(f'Winner: {n}\n')
            exit()

    if len(zero) > 0:  # if at least one candidate received zero votes
        if len(zero) == 1:  # if one candidate received zero votes, return them as lowest voted
            return zero[0], vf, False
        else:
            print("Unbreakable tie\n")  # if more than one, declare unbreakable tie
            exit()

    if count.most_common()[-1][1] == count.most_common()[-2][1]:  # check for tie
        tied = True

    lowest = count.most_common()[-1][0]  # set lowest to lowest voted candidate of round

    return order, lowest, vf, tied


# Finds candidate to eliminate given a tie or declares unbreakable tie.
def tiebreak(poll, cand, candidates):
    r_no = len(poll) - 1  # round number
    if r_no == 0:  # if first round, tie is unbreakable
        print("Unbreakable tie\n")
        exit()
    current = poll[r_no]  # votes from current round
    lowest = current.count(cand)  # lowest vote count of the round
    tied = []  # list of names that are tied

    for c in reversed(candidates):  # find names with tied lowest vote count
        if current.count(c) == lowest:
            tied.append(c)
        else:
            break

    high = 0  # placeholder for highest vote count in round
    h = []  # list of highest vote values in each round
    name = ""  # placeholder for tied candidate names

    while len(tied) > 1:  # while tie still exists
        current = poll[r_no - 1]  # set list to votes of a previous round

        for _ in tied:  # find highest voted for candidate in previous round
            if current.count(_) >= high:
                name = _
                high = current.count(name)
                h.append(high)  # keep track of each highest vote

        if h.count(high) == len(tied):
            if r_no == 1:  # if tie is unbreakable
                print("Unbreakable tie\n")
                exit()
            else:  # if still more rounds to check
                name = ""

        tied = list(filter(name.__ne__, tied))  # remove highest voted from elimination list
        r_no -= 1  # decrease round number by one
        high = 0
        h = []

    return tied[0]


pool = []  # list of voting preferences pool
all = []  # list of all candidate names

# reads lines from stdin into list
for line in sys.stdin:
    v_pref = []  # list of voting preferences for current voter
    if not line.strip():  # ignores empty lines
        continue
    for word in line.split():  # formats line into list
        v_pref.append(word)
        if all.count(word) == 0:
            all.append(word)
    pool.append(v_pref)  # add this voters preferences to voting pool

all = sorted(all)  # puts all candidate names in order
longest = max(all, key=len)
FORM = len(longest) + 3

r_num = 1  # round number
archive = []  # full list of round votes

while True:
    names, low, arc, tie = v_count(pool, all, r_num)  # returns results from round
    archive.append(arc)  # add this rounds votes to archive

    if tie:  # if there's a tie, tiebreak to find candidate to eliminate
        low = tiebreak(archive, low, names)

    print(f'Eliminated: {low}')  # print name of eliminated candidate
    r_num += 1  # increment round number

    for i in range(len(pool)):  # removes lowest voted name from voting pool
        pool[i] = list(filter(low.__ne__, pool[i]))

    all = list(filter(low.__ne__, all))  # removes eliminated candidates name from list of eligible candidates

    pool = list(filter(None, pool))  # removes empty lines from voting pool list
