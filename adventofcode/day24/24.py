# Day 24: Arithmetic Logic Unit
import functools as ft
import numpy as np


def parse(file_path):
    with open(file_path) as file:
        code = [line.rstrip().split(' ') for line in file]
        for line in code:
            if line[0] == 'inp':
                line.append(0)
    return code


def part_one_and_two(code):
    a = extract_parameters(code, 5)[::-1]
    b = extract_parameters(code, 15)[::-1]
    c = extract_parameters(code, 4)[::-1]
    low, high = generate(a, b, c, [0])
    print(f"Part one: {high}")
    print(f"Part two: {low}")


def extract_parameters(code, instruction_offset, base_instruction='inp', operand_offset=2):
    items = []
    for i, line in enumerate(code):
        if line[0] == base_instruction:
            items.append(int(code[i + instruction_offset][operand_offset]))
    return items


def generate(A, B, C, zs, res=''):
    if len(A) == 0:
        x = int(res)
        return x, x
    else:
        high = 0
        low = np.inf
        for w in range(1, 10):
            for z in zs:
                new_zs = backward(A[0], B[0], C[0], w, z)
                if len(new_zs) == 0:
                    continue
                l, h = generate(A[1:], B[1:], C[1:], new_zs, str(w) + res)
                high = max(high, h)
                low = min(low, l)
        return low, high


@ft.lru_cache()
def backward(A, B, C, w, z):
    # The input is a program divided into functional blocks that are parameterized by A, B and C.
    # The input is w and z, each block produces a new value of z. This function performs a reverse
    # pass of such block, producing all input zs what would produce a certain z (the input to this
    # function).
    zs = []
    z0 = z - w - B
    if (z0 % 26) == 0:
        zs.append(z0 // 26 * C)
    if 0 <= w - A < 26:
        zs.append((z * C) + (w - A))
    return zs


def main():
    code = parse('24.txt')
    part_one_and_two(code.copy())


if __name__ == "__main__":
    main()
