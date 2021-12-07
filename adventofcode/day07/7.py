# Day 7: The Treachery of Whales
import numpy as np


def parse(file_path):
    with open(file_path) as file:
        crabs = [int(n) for n in file.readline().rstrip().split(',')]
    return np.array(crabs)


def part_one(crabs):
    answer = sum(np.abs(crabs - np.median(crabs)))
    print(f"Part one: {int(answer)}")


def part_two(crabs):
    min_cost = np.inf
    for i in range(min(crabs), max(crabs)):
        diff = np.abs(crabs - i)
        cost = np.sum(diff * (diff + 1) // 2)
        min_cost = min(min_cost, cost)
    print(f"Part two: {min_cost}")


def main():
    crabs = parse('7.txt')
    part_one(crabs.copy())
    part_two(crabs.copy())


if __name__ == "__main__":
    main()
