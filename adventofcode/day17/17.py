# Day 17: Trick Shot
import os
import sys

# pylint: disable=c-extension-no-member
sys.path.append(os.path.join(sys.path[0], '..', 'algorithms'))
import algorithms as algo  # # noqa: E402, pylint: disable=wrong-import-position


class Rectangle:
    def __init__(self, left, right, bottom, top):
        self.left = left
        self.right = right
        self.bottom = bottom
        self.top = top

    def inside(self, x, y):
        return self.left <= x <= self.right and self.bottom <= y <= self.top


def parse(file_path):
    with open(file_path) as file:
        line = file.readline().rstrip()
        x0, x1, y0, y1 = algo.extract_ints(line)
    return Rectangle(x0, x1, y0, y1)


def part_one_and_two(rectangle):
    assert rectangle.left > 0 and rectangle.right > 0  # The target is to the right of the start position.
    assert rectangle.bottom < 0 and rectangle.top < 0  # The target is to the below the start position.
    max_height = 0
    hits = 0
    for vy in range(rectangle.bottom - 1, abs(rectangle.bottom) + 1):
        # No matter the initial velocity (positive or negative), the projectile will have the initial velocity
        # (downwards) when it passes the start position (0, 0). Thus an initial velocity larger than the max y
        # coordinate will overshoot the target (assuming the target is located below the start position).
        for vx in range(0, rectangle.right + 1):
            # An initial velocity larger than the max x coordinate will overshoot the target and an initial
            # velocity less than 0 will never pass the target (assuming the target is located to the right of
            # the start position).
            hit, max_height_candidate = simulate_projectile(rectangle, vx, vy)
            if hit:
                max_height = int(max(max_height, max_height_candidate))
                hits += 1
    answer_one = max_height
    answer_two = hits
    print(f"Part one: {answer_one}")
    print(f"Part two: {answer_two}")


def simulate_projectile(rectangle, velocity_x, velocity_y):
    position = 0 + 0j
    velocity = velocity_x + velocity_y * 1j
    max_height = 0
    while True:
        position += velocity
        max_height = max(max_height, position.imag)
        if rectangle.inside(position.real, position.imag):
            # Hit.
            return True, max_height
        if position.real > rectangle.right or position.imag < rectangle.bottom:
            # Miss.
            return False, None
        vx = max(velocity.real - 1, 0)
        vy = velocity.imag - 1
        velocity = vx + vy*1j


def main():
    rectangle = parse('17.txt')
    part_one_and_two(rectangle)


if __name__ == "__main__":
    main()
