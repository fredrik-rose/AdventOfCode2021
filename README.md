# Advent of Code 21

Solutions for the advent of code 2021 puzzles, implemented in Python. The
puzzles can be found here: https://adventofcode.com/2021

## Lessons Learned

### Algorithms

Imaginary numbers can be used to represent a 2D coordinate system.

### Numpy

Numpy convolve can be used to implement a custom moving average:

```
np.convolve(signal, np.ones(N), mode='valid')
```
