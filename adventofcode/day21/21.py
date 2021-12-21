# Day 21: Dirac Dice
import collections as coll
import itertools as it
import os
import sys

# pylint: disable=c-extension-no-member
sys.path.append(os.path.join(sys.path[0], '..', 'algorithms'))
import algorithms as algo  # # noqa: E402, pylint: disable=wrong-import-position


def parse(file_path):
    with open(file_path) as file:
        p1 = algo.extract_ints(file.readline())[1]
        p2 = algo.extract_ints(file.readline())[1]
    return p1 - 1, p2 - 1


def part_one(p1, p2):
    score, rolls = play_game(p1, p2)
    answer = score * rolls
    print(f"Part one: {answer}")


def part_two(p1, p2):
    w1, w2 = count_winners(p1, p2)
    answer = max(w1, w2)
    print(f"Part two: {answer}")


def play_game(p1, p2):
    def step(player, score):
        player = (player + sum(it.islice(dice, 3))) % 10
        score = score + player + 1
        return player, score

    s1 = 0
    s2 = 0
    dice = roll_dice()
    rolls = 0
    while True:
        p1, s1 = step(p1, s1)
        rolls += 3
        if s1 >= 1000:
            return s2, rolls
        p2, s2 = step(p2, s2)
        rolls += 3
        if s2 >= 1000:
            return s1, rolls


def roll_dice():
    value = 1
    while True:
        if value > 100:
            value = 1
        yield value
        value += 1


DP = {}  # Dynamic programming cache.
def count_winners(p1, p2, s1=0, s2=0):
    if (p1, p2, s1, s2) in DP:
        return DP[(p1, p2, s1, s2)]
    if s1 >= 21:
        return (1, 0)
    elif s2 >= 21:
        return (0, 1)
    else:
        tot_w1 = 0
        tot_w2 = 0
        for value, frequency in three_dice_probabilities().items():
            new_p1 = (p1 + value) % 10
            new_s1 = s1 + new_p1 + 1
            w2, w1 = count_winners(p2, new_p1, s2, new_s1)  # Note the swap!
            tot_w1 += w1 * frequency
            tot_w2 += w2 * frequency
        DP[(p1, p2, s1, s2)] = (tot_w1, tot_w2)
        return (tot_w1, tot_w2)


def three_dice_probabilities():
    prob = coll.Counter()
    for a in range(1, 4):
        for b in range(1, 4):
            for c in range(1, 4):
                prob[sum((a, b, c))] += 1
    return prob


def main():
    p1, p2 = parse('21.txt')
    part_one(p1, p2)
    part_two(p1, p2)


if __name__ == "__main__":
    main()
