# Day 3: Binary Diagnostic
import numpy as np


def parse(file_path):
    with open(file_path) as file:
        report = np.array([list(line.rstrip()) for line in file]).astype(np.int)
    report[report == 0] = -1  # Set 0 to -1 to make it easier to find the majority/minority bits.
    return report


def part_one(report):
    col_sums = sum_cols(report)
    gamma = col_sums > 0
    epsilon = np.logical_not(gamma)
    gamma = convert_binary_list_to_int(gamma)
    epsilon = convert_binary_list_to_int(epsilon)
    answer = gamma * epsilon
    print(f"Part one: {answer}")


def sum_cols(matrix):
    return np.sum(matrix, axis=0)


def convert_binary_list_to_int(binary_list):
    bits = [1 if e > 0 else 0 for e in binary_list]
    return int(''.join(map(str, bits)), 2)


def part_two(report):
    oxygen = filter_report(report.copy(), lambda x: 1 if x >= 0 else -1)
    co2 = filter_report(report.copy(), lambda x: -1 if x >= 0 else 1)
    answer = oxygen * co2
    print(f"Part two: {answer}")


def filter_report(report, get_bit_to_keep):
    for col in range(report.shape[1]):
        bit_to_keep = get_bit_to_keep(sum_cols(report[:, col]))
        report_filter = report[:, col] == bit_to_keep
        report = report[report_filter]
        if len(report) == 1:
            break
    return convert_binary_list_to_int(report[0])


def main():
    report = parse('3.txt')
    part_one(report.copy())
    part_two(report.copy())


if __name__ == "__main__":
    main()
