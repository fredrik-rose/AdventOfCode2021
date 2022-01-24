# Day 23: Amphipod
import functools as ft
import os
import re
import sys

# pylint: disable=c-extension-no-member
sys.path.append(os.path.join(sys.path[0], '..', 'algorithms'))
import algorithms as algo  # # noqa: E402, pylint: disable=wrong-import-position


BUCKET_TO_HALLWAY = {'A': 2, 'B': 4, 'C': 6, 'D': 8}
BUCKET_TO_INDEX = {'A': 0, 'B': 1, 'C': 2, 'D': 3}
BUCKET_TO_COST = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}


def parse(file_path):
    with open(file_path) as file:
        file.readline()
        hallway = file.readline().rstrip()[1:-1]
        buckets = [''] * 4
        while True:
            letters = extract_letters(file.readline().rstrip())
            if letters:
                buckets = [b + e for b, e in zip(buckets, letters)]
            else:
                break
    state = tuple([hallway] + buckets)
    return state


def extract_letters(text):
    return ''.join(re.findall(r'[A-Z]', text))


def part_one(state):
    end = ('...........', 'AA', 'BB', 'CC', 'DD')
    answer = algo.a_star(None, state, end, neighbors, heuristic)
    print(f"Part one: {answer}")


def part_two(state):
    end = ('...........', 'AAAA', 'BBBB', 'CCCC', 'DDDD')
    answer = algo.a_star(None, state, end, neighbors, heuristic)
    print(f"Part two: {answer}")


@ft.lru_cache
def heuristic(_, state):
    cost = 0
    for i, e in enumerate(state[0]):
        if e != '.':
            cost += (abs(BUCKET_TO_HALLWAY[e] - i) + 1) * BUCKET_TO_COST[e]
    for bucket, letter in zip(state[1:], BUCKET_TO_INDEX.keys()):
        valid = True
        for i, e in enumerate(bucket[::-1]):
            if valid and e == letter:
                continue
            valid = False
            if e != '.':
                steps_out_of_bucket = len(bucket) - i
                steps_corridor_to_bucket = abs(BUCKET_TO_HALLWAY[letter] - BUCKET_TO_HALLWAY[e]) + 1
                cost += (steps_out_of_bucket + steps_corridor_to_bucket) * BUCKET_TO_COST[e]
    return cost


def neighbors(_, state):
    for e in handle_buckets(state[0], state[1:]):
        yield e
    for e in handle_hallway(state[0], state[1:]):
        yield e


def handle_buckets(hallway, buckets):
    buckets = list(buckets)
    for j, (bucket, index, letter) in enumerate(zip(buckets, BUCKET_TO_HALLWAY.values(), BUCKET_TO_HALLWAY.keys())):
        if is_bucket_invalid(bucket, letter):
            new_bucket, new_letter, steps = remove_from_bucket(bucket)
            for i in hallway_indexes(hallway, index):
                new_hallway = hallway[:i] + new_letter + hallway[i + 1:]
                new_buckets = buckets[:j] + [new_bucket] + buckets[j + 1:]
                cost = (steps + abs(index - i)) * BUCKET_TO_COST[new_letter]
                yield tuple([new_hallway] + new_buckets), cost


def is_bucket_invalid(bucket, letter):
    return not all(e in (letter, '.') for e in bucket)


def remove_from_bucket(bucket):
    index = [e == '.' for e in bucket].index(False)
    return bucket[:index] + '.' + bucket[index + 1:], bucket[index], index + 1


def hallway_indexes(hallway, start):
    index = start - 1
    while index >= 0:
        if hallway[index] != '.':
            break
        yield index
        index -= 2
    else:
        if hallway[0] == '.':
            yield 0
    index = start + 1
    while index < len(hallway):
        if hallway[index] != '.':
            break
        yield index
        index += 2
    else:
        index = len(hallway) - 1
        if hallway[index] == '.':
            yield index


def handle_hallway(hallway, buckets):
    buckets = list(buckets)
    for i, e in enumerate(hallway):
        if e != '.':
            if reachable(hallway, i, BUCKET_TO_HALLWAY[e]):
                index = BUCKET_TO_INDEX[e]
                bucket = buckets[index]
                if is_bucket_free(bucket, e):
                    new_hallway = hallway[:i] + '.' + hallway[i + 1:]
                    new_bucket, steps = add_to_bucket(bucket, e)
                    new_buckets = buckets[:index] + [new_bucket] + buckets[index + 1:]
                    cost = (steps + abs(BUCKET_TO_HALLWAY[e] - i)) * BUCKET_TO_COST[e]
                    yield tuple([new_hallway] + new_buckets), cost


def reachable(hallway, start, end):
    assert start != end
    if start > end:
        start -= 1
    else:
        start += 1
    return all(e == '.' for e in hallway[min(start, end):max(start, end) + 1])


def is_bucket_free(bucket, letter):
    return bucket[0] == '.' and all(e in (letter, '.') for e in bucket)


def add_to_bucket(bucket, letter):
    index = len(bucket) - bucket[::-1].index('.') - 1
    return bucket[:index] + letter + bucket[index + 1:], index + 1


def main():
    part_one(parse('23_a.txt'))
    part_two(parse('23_b.txt'))


if __name__ == "__main__":
    main()
