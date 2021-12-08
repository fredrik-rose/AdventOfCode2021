# Day 8: Seven Segment Search
import itertools as it


def parse(file_path):
    def parse_signal(text):
        signal_patterns_text, output_text = text.rstrip().split(' | ')
        signal_patterns = signal_patterns_text.split(' ')
        output = output_text.split(' ')
        return signal_patterns, output

    with open(file_path) as file:
        signals = [parse_signal(line) for line in file]
    return signals


def part_one(signals):
    unique_numbers = set((2, 4, 3, 7))
    counter = 0
    for _, output in signals:
        counter += sum(1 for digit in output if len(digit) in unique_numbers)
    print(f"Part one: {counter}")


def part_two(signals):
    def translate(translator, display):
        return ''.join(sorted(translator[letter] for letter in display))

    segments = ('a', 'b', 'c', 'd', 'e', 'f', 'g')
    valid_displays = {'abcefg': 0,
                      'cf': 1,
                      'acdeg': 2,
                      'acdfg': 3,
                      'bcdf': 4,
                      'abdfg': 5,
                      'abdefg': 6,
                      'acf': 7,
                      'abcdefg': 8,
                      'abcdfg': 9}
    answer = 0
    for patterns, output in signals:
        for connections in it.permutations(segments):
            translator = dict(zip(segments, connections))
            for display in patterns:
                translation = translate(translator, display)
                if translation not in valid_displays.keys():
                    break
            else:
                digits = [valid_displays[translate(translator, display)] for display in output]
                number = ''.join(str(digit) for digit in digits)
                answer += int(number)
                break
    print(f"Part two: {answer}")


def main():
    signals = parse('8.txt')
    part_one(signals.copy())
    part_two(signals.copy())


if __name__ == "__main__":
    main()
