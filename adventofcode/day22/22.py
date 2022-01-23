# Day 22: Reactor Reboot
import os
import sys

# pylint: disable=c-extension-no-member
sys.path.append(os.path.join(sys.path[0], '..', 'algorithms'))
import algorithms as algo  # # noqa: E402, pylint: disable=wrong-import-position


class Cuboid:
    def __init__(self, x0, x1, y0, y1, z0, z1):
        self.x = (x0, x1)
        self.y = (y0, y1)
        self.z = (z0, z1)

    def __repr__(self):
        return f"Cuboid(x={self.x}, y={self.y}, z={self.z})"


class Event:
    def __init__(self, coord, status, cuboid):
        self.coord = coord
        self.status = status
        self.cuboid = cuboid

    def __repr__(self):
        return f"Event({self.coord}, {self.status}, {self.cuboid})"

    def __eq__(self, other):
        return (self.coord, self.status) == (other.coord, other.status)

    def __lt__(self, other):
        return (self.coord, not self.status) < (other.coord, not other.status)


def parse(file_path):
    with open(file_path) as file:
        cuboids = []
        for line in file:
            status = line.startswith('on')
            x0, x1, y0, y1, z0, z1 = algo.extract_ints(line)
            cuboids.append((Cuboid(x0, x1 + 1, y0, y1 + 1, z0, z1 + 1), status))
    return cuboids


def part_one(cuboids):
    reactor = set()
    for cuboid, status in cuboids:
        coordinates = set()
        for x in range(max(cuboid.x[0], -50), min(cuboid.x[1], 51)):
            for y in range(max(cuboid.y[0], -50), min(cuboid.y[1], 51)):
                for z in range(max(cuboid.z[0], -50), min(cuboid.z[1], 51)):
                    coordinates.add((x, y, z))
        if status:
            reactor |= coordinates
        else:
            reactor -= coordinates
    answer = len(reactor)
    print(f"Part one: {answer}")


def part_two(cuboids):
    actives = []
    for cuboid, status in cuboids:
        if status:
            actives = add_cubiod(actives, cuboid)
        else:
            actives = remove_cubiod(actives, cuboid)
    answer = volume_of_cubiods(actives)
    print(f"Part two: {answer}")


def add_cubiod(cuboids, element):
    splited_element = [element]
    for cubiod in cuboids:
        updated = []
        for part in splited_element:
            if check_overlap(part, cubiod):
                splitted = split_overlapping_cuboids((cubiod, part))
                for new in splitted:
                    if not check_overlap(new, cubiod):
                        updated.append(new)
            else:
                updated.append(part)
        splited_element = updated
    return cuboids + splited_element


def remove_cubiod(cuboids, element):
    new_cuboids = []
    for cubiod in cuboids:
        if check_overlap(cubiod, element):
            splited = split_overlapping_cuboids((cubiod, element))
            for new in splited:
                if not check_overlap(new, element):
                    new_cuboids.append(new)
        else:
            new_cuboids.append(cubiod)
    return new_cuboids


def check_overlap(a, b):
    def overlap(x, y):
        return x[1] > y[0] and x[0] < y[1]

    return overlap(a.x, b.x) and overlap(a.y, b.y) and overlap(a.z, b.z)


def split_overlapping_cuboids(cuboids):
    # NOTE: Could be optimized by adding and removing objects from a sorted event container instead
    # of creating a new event container every time as the current implementation.
    splitted = []
    for x0, x1, x_actives in sweep_line(cuboids, lambda cuboid: cuboid.x):
        for y0, y1, y_actives in sweep_line(x_actives, lambda cuboid: cuboid.y):
            for z0, z1, _ in sweep_line(y_actives, lambda cuboid: cuboid.z):
                splitted.append(Cuboid(x0, x1, y0, y1, z0, z1))
    return splitted


def sweep_line(cuboids, coordinate_getter):
    events = create_events(cuboids, coordinate_getter)
    actives = set()
    for x0, x1 in zip(events[:-1], events[1:]):
        assert x1.coord >= x0.coord
        if x0.status:
            actives.add(x0.cuboid)
        else:
            actives.remove(x0.cuboid)
        if x0.coord == x1.coord:
            continue
        if len(actives) == 0:
            continue
        yield x0.coord, x1.coord, actives


def create_events(cuboids, coordinate_getter):
    events = []
    for cuboid in cuboids:
        c0, c1 = coordinate_getter(cuboid)
        events.append(Event(c0, True, cuboid))
        events.append(Event(c1, False, cuboid))
    events.sort()
    return events


def volume_of_cubiods(cuboids):
    return sum((c.x[1] - c.x[0]) * (c.y[1] - c.y[0]) * (c.z[1] - c.z[0]) for c in cuboids)


def main():
    cuboids = parse('22.txt')
    part_one(cuboids.copy())
    part_two(cuboids.copy())


if __name__ == "__main__":
    main()
