# Day 19: Beacon Scanner
import collections as coll
import os
import sys

import numpy as np

# pylint: disable=c-extension-no-member
sys.path.append(os.path.join(sys.path[0], '..', 'algorithms'))
import algorithms as algo  # # noqa: E402, pylint: disable=wrong-import-position


def parse(file_path):
    scanners = coll.defaultdict(list)
    with open(file_path) as file:
        for line in file:
            if line.startswith("---"):
                current_scanner = scanners[algo.extract_ints(line)[0]]
            elif not line.rstrip():
                continue
            else:
                current_scanner.append(algo.extract_ints(line))
    scanners = {scanner_id: np.array(coordinates) for scanner_id, coordinates in scanners.items()}
    return scanners


def part_one(beacon_map):
    answer = len(beacon_map)
    print(f"Part one: {answer}")


def part_two(scanner_positions):
    max_distance = 0
    for scanner_a in scanner_positions:
        for scanner_b in scanner_positions:
            distance = np.sum(np.abs(scanner_a - scanner_b))
            max_distance = max(distance, max_distance)
    answer = max_distance
    print(f"Part two: {answer}")


def create_map(scanners):
    # This can be done much smarter. A "Shazam"-like algorithm would probably be good, were we
    # create pairs of all points (the difference between them) belonging to a scanner. Then we can
    # efficiently count how many of the point pairs of a scanner may be part of the global beacon
    # map, if not many enough we can quickly discard that candidate. If it has enough matches then
    # we verify the translation coherence with a histogram of translations for matching point pairs.
    beacon_map = scanners[0]
    del scanners[0]
    scanner_positions = [np.array([0, 0, 0])]
    while len(scanners) > 0:
        for scanner_id, beacons in scanners.items():
            positive_match, beacons_rt, translation = match(beacons, beacon_map)
            if positive_match:
                beacon_map = add_beacons_to_beacon_map(beacons_rt, beacon_map)
                scanner_positions.append(translation)
                del scanners[scanner_id]
                break
    return scanner_positions, beacon_map


def match(beacons, beacon_map):
    for rotation_matrix in generate_all_rotations():
        beacons_r = np.transpose(rotation_matrix @ np.transpose(beacons))
        translation_counter = coll.Counter()
        for beacon_a in beacons_r:
            for beacon_b in beacon_map:
                translation = beacon_b - beacon_a
                translation_counter[tuple(translation)] += 1
        matches = translation_counter.most_common()[0]
        if matches[1] >= 12:
            translation = np.array(matches[0])
            beacons_rt = beacons_r + translation
            return True, beacons_rt, translation
    return False, None, None


def add_beacons_to_beacon_map(beacons, beacon_map):
    def array_to_sets(array):
        return set(tuple(e) for e in array)

    return np.array(list(array_to_sets(beacon_map).union(array_to_sets(beacons))))


def generate_all_rotations():
    def roation_array_to_matrix(array):
        return np.array(array).reshape((3, 3)).astype(np.int)

    # http://www.euclideanspace.com/maths/algebra/matrix/transforms/examples/index.htm
    yield roation_array_to_matrix([1, 0, 0, 0, 1, 0, 0, 0, 1])
    yield roation_array_to_matrix([1, 0, 0, 0, 0, -1, 0, 1, 0])
    yield roation_array_to_matrix([1, 0, 0, 0, -1, 0, 0, 0, -1])
    yield roation_array_to_matrix([1, 0, 0, 0, 0, 1, 0, -1, 0])
    yield roation_array_to_matrix([0, -1, 0, 1, 0, 0, 0, 0, 1])
    yield roation_array_to_matrix([0, 0, 1, 1, 0, 0, 0, 1, 0])
    yield roation_array_to_matrix([0, 1, 0, 1, 0, 0, 0, 0, -1])
    yield roation_array_to_matrix([0, 0, -1, 1, 0, 0, 0, -1, 0])
    yield roation_array_to_matrix([-1, 0, 0, 0, -1, 0, 0, 0, 1])
    yield roation_array_to_matrix([-1, 0, 0, 0, 0, -1, 0, -1, 0])
    yield roation_array_to_matrix([-1, 0, 0, 0, 1, 0, 0, 0, -1])
    yield roation_array_to_matrix([-1, 0, 0, 0, 0, 1, 0, 1, 0])
    yield roation_array_to_matrix([0, 1, 0, -1, 0, 0, 0, 0, 1])
    yield roation_array_to_matrix([0, 0, 1, -1, 0, 0, 0, -1, 0])
    yield roation_array_to_matrix([0, -1, 0, -1, 0, 0, 0, 0, -1])
    yield roation_array_to_matrix([0, 0, -1, -1, 0, 0, 0, 1, 0])
    yield roation_array_to_matrix([0, 0, -1, 0, 1, 0, 1, 0, 0])
    yield roation_array_to_matrix([0, 1, 0, 0, 0, 1, 1, 0, 0])
    yield roation_array_to_matrix([0, 0, 1, 0, -1, 0, 1, 0, 0])
    yield roation_array_to_matrix([0, -1, 0, 0, 0, -1, 1, 0, 0])
    yield roation_array_to_matrix([0, 0, -1, 0, -1, 0, -1, 0, 0])
    yield roation_array_to_matrix([0, -1, 0, 0, 0, 1, -1, 0, 0])
    yield roation_array_to_matrix([0, 0, 1, 0, 1, 0, -1, 0, 0])
    yield roation_array_to_matrix([0, 1, 0, 0, 0, -1, -1, 0, 0])


def main():
    scanners = parse('19.txt')
    scanner_positions, beacon_map = create_map(scanners)
    part_one(beacon_map)
    part_two(scanner_positions)


if __name__ == "__main__":
    main()
