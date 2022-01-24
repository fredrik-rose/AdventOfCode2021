import collections as coll
import heapq
import re


def bin_to_int(x):
    # Converts a string of bits to an integer.
    if not x:
        return 0
    return int(x, 2)


def hex_to_bin(x):
    # Converts a string of hexadecimal numbers to a string of bits (preserving leading zeros).
    return bin(int(x, 16))[2:].zfill(len(x) * 4)


def extract_ints(text):
    # Extracts all integers.
    return [int(x) for x in re.findall(r'-?\d+', text)]


def a_star(graph, start, end, neighbors, heuristic, start_cost=0):
    visited = set()
    costs = coll.defaultdict(lambda: 1e9)
    costs[start] = start_cost
    queue = []
    heapq.heappush(queue, (costs[start], start))
    while len(queue) > 0:
        _, current = heapq.heappop(queue)
        if current == end:
            return costs[current]
        for n, c in neighbors(graph, current):
            if n not in visited:
                cost = costs[current] + c
                if cost < costs[n]:
                    costs[n] = cost
                priority = cost + heuristic(graph, n)
                heapq.heappush(queue, (priority, n))
        visited.add(current)
    return None
