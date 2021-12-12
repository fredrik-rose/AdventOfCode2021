# Day 12:  Passage Pathing
import collections as coll


def parse(file_path):
    graph = coll.defaultdict(set)
    with open(file_path) as file:
        for line in file:
            a, b = line.rstrip().split('-')
            graph[a].add(b)
            graph[b].add(a)
    return graph


def part_one(graph):
    answer = count_all_paths(graph, 'start', 1)
    print(f"Part one: {answer}")


def part_two(graph):
    for neighbors in graph.values():
        neighbors.discard('start')  # We are not allowed to enter the start node again.
    answer = count_all_paths(graph, 'start', 2)
    print(f"Part two: {answer}")


def count_all_paths(graph, node, max_small_visit, visited=coll.defaultdict(int)):
    # pylint: disable=dangerous-default-value
    visited = visited.copy()
    if node == 'end':
        return 1
    if node.islower():
        visited[node] += 1
        if visited[node] > max_small_visit:
            return 0
        if sum(count > 1 for count in visited.values()) > 1:
            # We are only allowed to visit one small cave twice.
            return 0
    return sum(count_all_paths(graph, neighbor, max_small_visit, visited) for neighbor in graph[node])


def main():
    graph = parse('12.txt')
    part_one(graph.copy())
    part_two(graph.copy())


if __name__ == "__main__":
    main()
