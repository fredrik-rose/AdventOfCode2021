# Advent of Code 21

Solutions for the advent of code 2021 puzzles, implemented in Python. The
puzzles can be found here: https://adventofcode.com/2021

## Lessons Learned

### Algorithms

#### A*

A* is basically Dijkstra's algorithm with an added heuristic that aids in the selection of the next node to visit.
One such heuristics might be the number of nodes between the current node and the end node. See day 15 for an
implementation. Do however note that the graph representation is a bit awkward, it is not the typical dict of sets.

If the graph is a grid the number of nodes in between may not be a good heuristic.

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
once, instead of treating them individually. E.g. frequency counting. Math is not always the solution.
See day 6 and 14 as examples.

#### Minimum Distance

The position that has the minimum total distance to a collections of positions is the median position.

#### Flood Fill

See day 09.

#### Graph Representation

A graph can be represented as a dict of sets, where the keys are the nodes and the values are the connections.

### Python

Extracts all integers in a line:
```
def extract_ints(line):
    return [int(x) for x in re.findall(r'-?\d+', line)]
```

A stack can easily be implemented using a list.

Be careful with dangerous default function parameters (e.g. lists and dicts). If altered in the function the values
will be kept top next function call. Avoid if possible otherwise it may be a good practice to make a copy of it
at the start of the function.

Unpack a list of tuples to two lists:
```
x, y = zip(*coordinates)
```

heapq can be used to implement a priority queue.

Use itertools.islice to extract the first n elements of a generator.

Python 3.10 introduce switch-statements.

#### Integer Rounding

Round down:
```
x // 2
```

Round up:
```
-(-x // 2)
```

#### Insert in Place

```
>>> a = [1,2,3,4,5]
>>> a[2:4] = [9]
>>> a
[1, 2, 9, 5]
```

### Numpy

Numpy convolve can be used to implement a custom moving average:

```
np.convolve(signal, np.ones(N), mode='valid')
```

Visualize a numpy array as an image (created from a list of coordinates):
```
image = np.zeros((max(y) + 1, max(x) + 1))
image[y, x] = 1
plt.imshow(image)
plt.show()
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
