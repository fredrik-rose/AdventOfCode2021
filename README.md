# Advent of Code 21

Solutions for the advent of code 2021 puzzles, implemented in Python. The
puzzles can be found here: https://adventofcode.com/2021

## Lessons Learned

### Algorithms

#### Dynamic Programming

Dynamic programming is basically brute force with memoization, it can be useful if a certain "state" occurs in
several of the "paths".
```
DP = {}
def fibonacci(n):
    if n in DP:
        return DP[n]
    elif n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        DP[n] = fibonacci(n - 1) + fibonacci(n - 2)
        return DP[n]
```

This can easily be implemented in Python using the @functools.lru_cache decorator. Then we do not have to manage
the dynamic programming logic ourselves.

#### A*

A* is basically Dijkstra's algorithm with an added heuristic that aids in the selection of the next node to visit.
One such heuristics might be the number of nodes between the current node and the end node. Note that the heuristic
should not over-estimate the actual distance. See day 15 and 23 for example implementations. Do however note that the
graph representation in day 15 is a bit awkward, it is not the typical dict of sets. Day 23 do not even create graph,
it operates on a state space and the neighbors of a particular state (i.e. node) is given by the neighbors function.

If the graph is a grid the number of nodes in between may not be a good heuristic.

#### State Space as Graph

A state space problem (e.g. states in a game) can be considered as a graph problem where each state is a node in the
graph. A path search algorithm (e.g. A\*) can then be used to find the shortest path from one state to another.

#### Sweep Line

Algorithm that can be used to process (typically overlapping) objects in an euclidean coordinate system. Could e.g.
be used to split overlapping rectangles (into non-overlapping rectangles):

1. Create two events for each rectangle: an 'on' event for the min x coordinate and an 'off' event for the max x
   coordinate. Each event shall contain a reference to the corresponding rectangle.
2. Sort the events on coordinates, for equal coordinates an 'off' event should come before an 'on' event.
3. Create an empty set of active rectangles.
4. Iterate over the sorted events, add the rectangle to the active set for an 'on' event, remove it for an 'off' event.
   Do step 1. and 2. for the active rectangles but this time with the y coordinates to create new events. Iterate over
   the new events, create a rectangle starting at the current x, y event and ending on the next x, y event.

An example of another application is to calculate the area of overlapping rectangles.

See day 22 for an example (splitting overlapping cuboids).

See these references for more information:

* https://tryalgo.org/en/geometry/2016/06/25/union-of-rectangles/
* https://leetcode.com/problems/rectangle-area-ii/solution/
* https://stackoverflow.com/questions/12769386/how-to-calculate-total-volume-of-multiple-overlapping-cuboids
* https://stackoverflow.com/questions/244452/what-is-an-efficient-algorithm-to-find-area-of-overlapping-rectangles

Another (not really related) alternative is to use coordinate compression.

#### Represent 2D Coordinate System with Imaginary Numbers

Imaginary numbers can be used to represent a 2D coordinate system.

#### Representation of 2D Board

A dict where the keys are 2D coordinates can be used to represent a 2D board as an alternative to a 2D matrix.

A board with on/off values can be represented as a set of coordinates, the positions in the set represents on values.

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

#### Point Correspondence

Linear regression could be used to find the rotation and translation from one set of points to another set of points.

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

#### Profiling

```
python -m cProfile -o data.prof my_script.py
snakeviz data.prof
```

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

Moving back and forth between Numpy and Python data structures seems really slow.

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
