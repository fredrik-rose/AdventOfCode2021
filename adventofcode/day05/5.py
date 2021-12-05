# Day 5: Hydrothermal Venture
import collections as coll

import numpy as np


class Line:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def is_vertical(self):
        return self.start.real == self.end.real

    def is_horizontal(self):
        return self.start.imag == self.end.imag

    def points(self):
        # Note: this only work for horizontal, vertical and diagonal (45 degrees) lines.
        direction = self.end - self.start
        normalized_direction = np.sign(direction.real) + np.sign(direction.imag) * 1j
        point = self.start
        while point != self.end:
            yield point
            point += normalized_direction
        yield point


def parse(file_path):
    def parse_line(text):
        start, end = text.strip().split('->')
        return Line(parse_coord(start), parse_coord(end))

    def parse_coord(text):
        x, y = text.strip().split(',')
        return int(x) + int(y) * 1j

    with open(file_path) as file:
        lines = [parse_line(line) for line in file]
    return lines


def part_one(lines):
    lines = [line for line in lines if line.is_horizontal() or line.is_vertical()]
    answer = count_overlaping_coordinates(lines)
    print(f"Part one: {answer}")


def count_overlaping_coordinates(lines):
    coords = coll.defaultdict(int)
    for line in lines:
        for point in line.points():
            coords[point] += 1
    number_of_overlaps = sum(1 for count in coords.values() if count > 1)
    return number_of_overlaps


def part_two(lines):
    answer = count_overlaping_coordinates(lines)
    print(f"Part two: {answer}")


def main():
    lines = parse('5.txt')
    part_one(lines.copy())
    part_two(lines.copy())


if __name__ == "__main__":
    main()
