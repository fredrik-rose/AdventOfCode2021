# Day 1: Sonar Sweep
import numpy as np


def count_poss_diffs(signal):
    diffs = np.diff(signal)
    return sum(e > 0 for e in diffs)


def part_one(depths):
    num_positive_diffs = count_poss_diffs(depths)
    print(f"Part one: {num_positive_diffs}")


def part_two(depths):
    filter_size = 3
    filtered_depths = np.convolve(depths, np.ones(filter_size), mode='valid')
    num_positive_diffs = count_poss_diffs(filtered_depths)
    print(f"Part one: {num_positive_diffs}")


def main():
    with open('1.txt') as file:
        depths = [int(line) for line in file]
    part_one(depths.copy())
    part_two(depths.copy())


if __name__ == "__main__":
    main()
