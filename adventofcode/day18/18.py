# Day 18: Snailfish
import functools as ft
import json


def parse(file_path):
    with open(file_path) as file:
        numbers = [json.loads(line.rstrip()) for line in file]
    return numbers


def part_one(numbers):
    total_sum = ft.reduce(add, numbers)
    answer = get_magnitude(total_sum)
    print(f"Part one: {answer}")


def part_two(numbers):
    max_mag = 0
    for i, n in enumerate(numbers):
        for j, m in enumerate(numbers):
            if i == j:
                continue
            number = add(n, m)
            max_mag = max(max_mag, get_magnitude(number))
    answer = max_mag
    print(f"Part two: {answer}")


def add(a, b):
    return reduce([a, b])


def reduce(number):
    number = list_to_text(number)
    while explode(number) or split(number):
        pass
    number = text_to_list(number)
    return number


def list_to_text(number):
    if isinstance(number, int):
        return [number]
    else:
        assert isinstance(number, list)
        a, b = number
        text = ['[']
        text += list_to_text(a)
        text.append(',')
        text += list_to_text(b)
        text.append(']')
        return text


def text_to_list(text):
    return json.loads(''.join(str(e) for e in text))


def explode(text):
    indexes = get_index_of_integers(text)
    level = 0
    int_index = -1
    for i, element in enumerate(text):
        if element == '[':
            level += 1
        elif element == ']':
            level -= 1
        elif isinstance(element, int):
            int_index += 1
            assert int_index < len(indexes)
        assert level >= 0
        if level == 5:
            if int_index >= 0:
                text[indexes[int_index]] += text[indexes[int_index + 1]]
            if int_index + 3 < len(indexes):
                text[indexes[int_index + 3]] += text[indexes[int_index + 2]]
            text[i:i+5] = [0]
            return True
    return False


def split(text):
    for i, element in enumerate(text):
        if isinstance(element, int) and element >= 10:
            a = element // 2  # Round down.
            b = -(-element // 2)  # Round up.
            text[i:i + 1] = ['[', a, ',', b, ']']
            return True
    return False


def get_index_of_integers(values):
    return [i for i, e in enumerate(values) if isinstance(e, int)]


def get_magnitude(number):
    if isinstance(number, int):
        return number
    else:
        assert isinstance(number, list)
        a, b = number
        return 3 * get_magnitude(a) + 2 * get_magnitude(b)


def main():
    numbers = parse('18.txt')
    part_one(numbers.copy())
    part_two(numbers.copy())


if __name__ == "__main__":
    main()
