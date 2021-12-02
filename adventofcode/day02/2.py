# Day 2: Dive!


def parse(file_path):
    instructions = []
    with open(file_path) as file:
        for line in file:
            command, distance = line.split(' ')
            instructions.append((command, int(distance)))
    return instructions


def part_one(instructions):
    position = apply_instructions_1(instructions)
    answer = int(position.real * abs(position.imag))
    print(f"Part one: {answer}")


def apply_instructions_1(instructions):
    position = 0 + 0j
    for command, distance in instructions:
        if command == 'forward':
            position += distance
        elif command == 'up':
            position += 1j * distance
        elif command == 'down':
            position += -1j * distance
    return position


def part_two(instructions):
    position = apply_instructions_2(instructions)
    answer = int(position.real * abs(position.imag))
    print(f"Part two: {answer}")


def apply_instructions_2(instructions):
    position = 0 + 0j
    aim = 1 + 0j
    for command, distance in instructions:
        if command == 'down':
            aim += -1j * distance
        elif command == 'up':
            aim += 1j * distance
        elif command == 'forward':
            position += aim * distance
    return position


def main():
    instructions = parse('2.txt')
    part_one(instructions.copy())
    part_two(instructions.copy())


if __name__ == "__main__":
    main()
