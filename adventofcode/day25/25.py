# Day 25: Sea Cucumber
import functools as ft
import numpy as np
import scipy.ndimage as ndi


EMPTY = 0
EAST = 1
SOUTH = 2


def parse(file_path):
    with open(file_path) as file:
        translator = {'.': EMPTY, '>': EAST, 'v': SOUTH}
        world = [[translator[c] for c in line.rstrip()] for line in file]
    return np.array(world)


def part_one(world):
    step = 0
    while True:
        new_world = simulate(world)
        step += 1
        if (new_world == world).all():
            break
        world = new_world
    print(f"Part one: {step}")


def simulate(world):
    def kernel(data, cucumber):
        assert len(data) == 3
        if data[1] == cucumber and data[2] == EMPTY:
            return EMPTY
        elif data[1] == EMPTY and data[0] == cucumber:
            return cucumber
        else:
            return data[1]

    east_items = np.array([[1, 1, 1]])
    south_items = np.array([[1], [1], [1]])
    world = ndi.generic_filter(world, function=ft.partial(kernel, cucumber=EAST), footprint=east_items, mode='wrap')
    world = ndi.generic_filter(world, function=ft.partial(kernel, cucumber=SOUTH), footprint=south_items, mode='wrap')
    return world


def main():
    world = parse('25.txt')
    part_one(world.copy())


if __name__ == "__main__":
    main()
