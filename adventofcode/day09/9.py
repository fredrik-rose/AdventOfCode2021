# Day 9: Smoke Basin
import collections as coll
import numpy as np
import scipy.ndimage as ndi


def parse(file_path):
    with open(file_path) as file:
        heightmap = np.array([list(line.rstrip()) for line in file]).astype(np.int)
    return heightmap


def part_one(heightmap):
    valleys = find_vallies(heightmap)
    answer = np.sum(heightmap[valleys] + 1)
    print(f"Part one: {answer}")


def part_two(heightmap):
    heightmap = np.pad(heightmap, pad_width=1, mode='constant', constant_values=9)
    valleys = find_vallies(heightmap)
    vally_indexes = zip(*np.where(valleys))
    sizes = [flood_fill(heightmap, index) for index in vally_indexes]
    sizes.sort()
    answer = sizes[-1] * sizes[-2] * sizes[-3]
    print(f"Part two: {answer}")


def find_vallies(heightmap):
    footprint = np.array([[0, 1, 0],
                          [1, 1, 1],
                          [0, 1, 0]])
    valleys = ndi.generic_filter(heightmap,
                                 function=lambda x: all(x[2] < e for i, e in enumerate(x) if i != 2),
                                 footprint=footprint,
                                 mode='constant',
                                 cval=np.max(heightmap) + 1).astype(bool)
    return valleys


def flood_fill(heightmap, source_position):
    dx = [0, 1, 0, -1]
    dy = [-1, 0, 1, 0]
    filled = set()
    Q = coll.deque()
    Q.append(source_position)
    while len(Q) > 0:
        position = Q.popleft()
        if position not in filled and heightmap[position] != 9:
            filled.add(position)
            for y, x in zip(dy, dx):
                Q.append((position[0] + y, position[1] + x))
    return len(filled)


def main():
    heightmap = parse('9.txt')
    part_one(heightmap.copy())
    part_two(heightmap.copy())


if __name__ == "__main__":
    main()
