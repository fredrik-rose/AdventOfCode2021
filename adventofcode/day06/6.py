# Day 6: Lanternfish
import collections as coll


def parse(file_path):
    with open(file_path) as file:
        fishes = [int(n) for n in file.readline().rstrip().split(',')]
    return fishes


def part_one(fishes):
    answer = simulate(fishes, 80)
    print(f"Part one: {answer}")


def part_two(fishes):
    answer = simulate(fishes, 256)
    print(f"Part two: {answer}")


def simulate(fishes, n):
    counts = {i: 0 for i in range(9)}
    counts.update(coll.Counter(fishes))
    counts = coll.deque(counts.values())
    for _ in range(n):
        counts.rotate(-1)
        counts[6] += counts[8]
    return sum(counts)


def main():
    fishes = parse('6.txt')
    part_one(fishes.copy())
    part_two(fishes.copy())


if __name__ == "__main__":
    main()
