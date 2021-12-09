# Day 10: Syntax Scoring
import numpy as np


def parse(file_path):
    with open(file_path) as file:
        code = [list(line.rstrip()) for line in file]
    return code


def part_one(code):
    error_to_score = {')': 3, ']': 57, '}': 1197, '>': 25137}
    scores = []
    for line in code:
        try:
            autocomplete(line)
        except SyntaxError as error:
            scores.append(error_to_score[str(error)])
    answer = sum(scores)
    print(f"Part one: {answer}")


def part_two(code):
    char_to_score = {')': 1, ']': 2, '}': 3, '>': 4}
    scores = []
    for line in code:
        try:
            completion = autocomplete(line)
        except SyntaxError:
            continue
        score = 0
        for char in completion:
            score = score * 5 + char_to_score[char]
        scores.append(score)
    answer = int(np.median(scores))
    print(f"Part two: {answer}")


def autocomplete(line):
    openers = ('(', '[', '{', '<')
    closers = (')', ']', '}', '>')
    opener_to_closer = dict(zip(openers, closers))
    stack = []
    for char in line:
        if char in closers:
            expected = opener_to_closer[stack.pop()]
            if char != expected:
                raise SyntaxError(char)
        else:
            assert char in openers
            stack.append(char)
    completion = [opener_to_closer[char] for char in stack[::-1]]
    return completion


def main():
    code = parse('10.txt')
    part_one(code.copy())
    part_two(code.copy())


if __name__ == "__main__":
    main()
