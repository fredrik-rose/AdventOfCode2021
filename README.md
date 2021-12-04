# Advent of Code 21

Solutions for the advent of code 2021 puzzles, implemented in Python. The
puzzles can be found here: https://adventofcode.com/2021

## Lessons Learned

### Algorithms

Imaginary numbers can be used to represent a 2D coordinate system.

A generator can be used if one wants to iterate over a sequence with multiple stop conditions:
```
def variant_a(data):
    for e in generator(data):
        if e:
            return e


def variant_b(data):
    seen = set()
    for e in generator(data):
        seen.add(e)
        if len(seen) == 3:
            break
    return seen


def generator(data):
    for e in data:
        yield e

```

### Python

Extracts all integers in a line:
```
def extract_ints(line):
    return [int(x) for x in re.findall(r'-?\d+', line)]
```

### Numpy

Numpy convolve can be used to implement a custom moving average:

```
np.convolve(signal, np.ones(N), mode='valid')
```
