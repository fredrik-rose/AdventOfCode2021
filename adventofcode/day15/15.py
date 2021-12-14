# Day 15: Chiton
import heapq
import numpy as np


def parse(file_path):
    with open(file_path) as file:
        graph = np.array([list(line.rstrip()) for line in file]).astype(np.int)
    return graph


def part_one(graph):
    answer = a_star(graph)
    print(f"Part one: {answer}")


def part_two(graph):
    def extend_graph(g, n):
        extended = [g]
        for _ in range(n):
            tile = extended[-1] + 1
            tile[tile > 9] = 1
            extended.append(tile)
        return extended

    extended_graph = np.concatenate(extend_graph(graph, 4), axis=1)
    extended_graph = np.concatenate(extend_graph(extended_graph, 4), axis=0)
    answer = a_star(extended_graph)
    print(f"Part two: {answer}")


def a_star(graph):
    # The graph is a grid represented as a matrix. Each element in the matrix represents a node, the value of an
    # element represents the cost of getting to that particular node from all each neighbors.
    # The start node is the top left corner (0, 0), the end node is the bottom right corner.
    start = (0, 0)
    goal = (graph.shape[0] - 1, graph.shape[1] - 1)
    C = np.full(graph.shape, np.inf)  # The costs to get to a particular node.
    C[start] = 0
    H = heuristic(graph)
    visited = set()
    Q = []
    heapq.heappush(Q, (0, (0, 0)))
    while len(Q) > 0:
        _, u = heapq.heappop(Q)
        visited.add(u)
        if u == goal:
            break
        for n in neighbors(graph, u):
            if n not in visited:
                cost = C[u] + graph[n]
                if cost < C[n]:
                    C[n] = cost
                    priority = cost + H[n]  # If H[n] = 0 for all n, then this is equal to Dijkstra's.
                    heapq.heappush(Q, (priority, n))
    cost = int(C[goal])
    return cost


def neighbors(graph, v):
    if v[0] > 0:
        yield (v[0] - 1, v[1])
    if v[0] < graph.shape[0] - 1:
        yield (v[0] + 1, v[1])
    if v[1] > 0:
        yield (v[0], v[1] - 1)
    if v[1] < graph.shape[1] - 1:
        yield (v[0], v[1] + 1)


def heuristic(graph):
    H = np.zeros(graph.shape)
    for y in range(graph.shape[0]):
        for x in range(graph.shape[1]):
            H[y, x] = abs((graph.shape[0] - 1) - y) + abs((graph.shape[1] - 1) - x)
    return H


def main():
    graph = parse('15.txt')
    part_one(graph.copy())
    part_two(graph.copy())


if __name__ == "__main__":
    main()
