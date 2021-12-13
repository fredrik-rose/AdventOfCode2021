# Day 13: Transparent Origami
import matplotlib.pyplot as plt
import numpy as np


def parse(file_path):
    def parse_dots(text):
        dots = set()
        for line in text:
            x, y = line.split(',')
            dots.add((int(x), int(y)))
        return dots

    def parse_folds(text):
        folds = []
        for line in text:
            fold, value = line.rstrip().split('=')
            if 'x' in fold:
                folds.append((int(value), 1e9))
            else:
                assert 'y' in fold
                folds.append((1e9, int(value)))
        return folds

    with open(file_path) as file:
        dots_text, folds_text = file.read().rstrip().split('\n\n')
    dots = parse_dots(dots_text.split('\n'))
    folds = parse_folds(folds_text.split('\n'))
    return dots, folds


def part_one(dots, folds):
    folded_dots = fold_dots(dots, folds[0])
    answer = len(folded_dots)
    print(f"Part one: {answer}")


def part_two(dots, folds):
    for item in folds:
        dots = fold_dots(dots, item)
    visualize(dots)


def fold_dots(dots, fold):
    def fold_coord(coord, fold):
        if coord > fold:
            return fold - (coord - fold)
        return coord

    folded_dots = set((fold_coord(dot[0], fold[0]), fold_coord(dot[1], fold[1])) for dot in dots)
    return folded_dots


def visualize(dots):
    x, y = zip(*dots)
    image = np.zeros((max(y) + 1, max(x) + 1))
    image[y, x] = 1
    plt.imshow(image)
    plt.title("Part two")
    plt.show()


def main():
    dots, folds = parse('13.txt')
    part_one(dots.copy(), folds.copy())
    part_two(dots.copy(), folds.copy())


if __name__ == "__main__":
    main()
