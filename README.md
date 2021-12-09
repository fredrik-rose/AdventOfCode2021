# Advent of Code 21

Solutions for the advent of code 2021 puzzles, implemented in Python. The
puzzles can be found here: https://adventofcode.com/2021

## Lessons Learned

### Algorithms

#### Represent 2D Coordinate System with Imaginary Numbers

Imaginary numbers can be used to represent a 2D coordinate system.

#### Representation of 2D Board

A dict where the keys are 2D coordinates can be used to represent a 2D board as an alternative to a 2D matrix.

#### Iterating over Sequence with Multiple Stop Conditions

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

#### Line Representation

Vertical lines can be problematic to represent with the usual line equation `y = kx+m`. There are several other ways
to represent lines.

##### General Equation
```
a * x + b * y - c = 0
```
```
a = (y1 - y2)
b = (x2 - x1)
c = (x2 * y1 - x1 * y2)
```

##### Parametric Approach

```
Base = P1
Direction = P2 - P1 (may be normalized)
```

Any point at the line might be described using parameter t
```
x(t) = x1 + t * Direction.X
y(t) = y1 + t * Direction.Y
```

#### Change of Representation

Sometimes it might be a good idea to collect all things of a certain type and perform operation on all of them at
once, instead of treating them individually. Math is not always the solution. See day 6 as an example.

#### Minimum Distance

The position that has the minimum total distance to a collections of positions is the median position.

#### Flood Fill

See day 09.

### Python

Extracts all integers in a line:
```
def extract_ints(line):
    return [int(x) for x in re.findall(r'-?\d+', line)]
```

A stack can easily be implemented using a list.

### Numpy

Numpy convolve can be used to implement a custom moving average:

```
np.convolve(signal, np.ones(N), mode='valid')
```

### SciPy

scipy.ndimage.generic_filter can be really useful for various filter-like operations. An example that find (strict)
valleys:
```
footprint = np.array([[0, 1, 0],
                     [1, 1, 1],
                     [0, 1, 0]])
vallies = ndi.generic_filter(heightmap,
                             function=lambda x: all(x[2] < e for i, e in enumerate(x) if i != 2),
                             footprint=footprint,
                             mode='constant',
                             cval=np.max(heightmap) + 1).astype(bool)
```
