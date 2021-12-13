# Day 14: Extended Polymerization
import collections as coll


def parse(file_path):
    with open(file_path) as file:
        template = list(file.readline().rstrip())
        file.readline()
        rules = {}
        for line in file:
            pair, result = line.rstrip().split(' -> ')
            rules[tuple(pair)] = result
    return template, rules


def part_one(template, rules):
    answer = simulate(template, rules, 10)
    print(f"Part one: {answer}")


def part_two(template, rules):
    answer = simulate(template, rules, 40)
    print(f"Part two: {answer}")


def simulate(template, rules, steps):
    pairs = coll.Counter((a, b) for a, b in zip(template[:-1], template[1:]))
    for _ in range(steps):
        new_pairs = coll.Counter()
        for (a, b), count in pairs.items():
            c = rules[(a, b)]
            new_pairs[(a, c)] += count
            new_pairs[(c, b)] += count
        pairs = new_pairs
    element_count = count_elements_in_pairs(pairs, template[-1])
    return max(element_count.values()) - min(element_count.values())


def count_elements_in_pairs(pairs, last_element):
    element_count = coll.Counter(last_element)  # We need to add the last element manually as it is not counted.
    for (a, _), count in pairs.items():
        element_count[a] += count
    return element_count


def main():
    template, rules = parse('14.txt')
    part_one(template.copy(), rules.copy())
    part_two(template.copy(), rules.copy())


if __name__ == "__main__":
    main()
