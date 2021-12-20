# Day 20: Trench Map
import numpy as np
import scipy.ndimage as ndi


def parse(file_path):
    def decode_line(text):
        return [1 if c == '#' else 0 for c in text.rstrip()]

    with open(file_path) as file:
        lut = decode_line(file.readline())
        file.readline()
        image = []
        for line in file:
            image.append(decode_line(line))
    return np.array(image).astype(np.int), lut


def part_one(image, lut):
    image = enhance(image, lut, 2)
    answer = np.count_nonzero(image)
    print(f"Part one: {answer}")


def part_two(image, lut):
    image = enhance(image, lut, 50)
    answer = np.count_nonzero(image)
    print(f"Part two: {answer}")


def enhance(image, lut, steps):
    def kernel(data):
        return lut[int(''.join(str(e) for e in data.astype(np.int)), 2)]

    image = np.pad(image, 2)
    for _ in range(steps):
        image = np.pad(image, 1, mode='reflect')
        image = ndi.generic_filter(image, function=kernel, size=3, mode='reflect')
    return image


def main():
    image, lut = parse('20.txt')
    part_one(image.copy(), lut.copy())
    part_two(image.copy(), lut.copy())


if __name__ == "__main__":
    main()
