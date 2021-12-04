# Day 4: Giant Squid
import re

import numpy as np


def parse(file_path):
    def parse_board(board_text):
        return [extract_ints(line) for line in board_text.split('\n')]

    with open(file_path) as file:
        numbers = extract_ints(file.readline())
        file.readline()
        board_lines = file.read().split('\n\n')
    boards = np.array([parse_board(board.rstrip()) for board in board_lines])
    return numbers, boards


def extract_ints(line):
    return [int(x) for x in re.findall(r'-?\d+', line)]


def part_one(numbers, boards):
    for _, score in play_bingo(numbers, boards):
        print(f"Part one: {score}")
        break


def play_bingo(numbers, boards):
    marked_boards = np.zeros(boards.shape)
    for number in numbers:
        marked_boards[boards == number] = 1
        for i, marked in enumerate(marked_boards):
            if has_bingo(marked):
                score = calculate_score(number, boards[i], marked)
                yield i, score


def has_bingo(marked):
    row_bingo = np.any(np.all(marked, axis=0))
    col_bing = np.any(np.all(marked, axis=1))
    bingo = np.logical_or(row_bingo, col_bing)
    return bingo


def calculate_score(number, board, marked):
    unmarked_sum = np.sum(board[marked == 0])
    return unmarked_sum * number


def part_two(numbers, boards):
    winners = set()
    for index, score in play_bingo(numbers, boards):
        winners.add(index)
        if len(winners) == boards.shape[0]:
            print(f"Part two: {score}")
            break


def main():
    numbers, boards = parse('4.txt')
    part_one(numbers.copy(), boards.copy())
    part_two(numbers.copy(), boards.copy())


if __name__ == "__main__":
    main()
