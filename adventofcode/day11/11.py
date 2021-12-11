# Day 11: Dumbo Octopus
import numpy as np
import scipy.ndimage as ndi


def parse(file_path):
    with open(file_path) as file:
        octos = [list(line.rstrip()) for line in file]
    return np.array(octos).astype(np.int)


def part_one(octos):
    flashes = 0
    for _ in range(100):
        octos = simulate_step(octos)
        flashes += len(octos[octos == 0])
    print(f"Part one: {flashes}")


def part_two(octos):
    for i in range(1000000):
        octos = simulate_step(octos)
        if np.all(octos == 0):
            answer = i + 1
            break
    print(f"Part two: {answer}")


def simulate_step(octos):
    octos += 1
    while np.any(octos > 9):
        octos = ndi.generic_filter(octos, function=flash_kernel, size=3, mode='constant', cval=0)
    return octos


def flash_kernel(octos):
    assert len(octos) == 9
    me = octos[4]
    if me == 0 or me > 9:
        return 0
    return me + (octos > 9).sum()


def main():
    octos = parse('11.txt')
    part_one(octos.copy())
    part_two(octos.copy())


if __name__ == "__main__":
    main()
