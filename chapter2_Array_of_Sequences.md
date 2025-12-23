# Python Sequences - Practical Memo

## Quick Comparison: Sequence Types

| Type | Mutable | Container | Homogeneous | Use Case |
|------|---------|-----------|-------------|----------|
| `list` | Yes | Yes | No | General-purpose mutable sequence |
| `tuple` | No | Yes | No | Immutable records, dict keys |
| `str` | No | Flat | Yes (chars) | Text |
| `bytes` | No | Flat | Yes | Binary data (immutable) |
| `bytearray` | Yes | Flat | Yes | Binary data (mutable) |
| `array.array` | Yes | Flat | Yes | Numeric data, memory-efficient |
| `collections.deque` | Yes | Yes | No | Fast append/pop both ends, queues |
| `memoryview` | - | Flat | Yes | Zero-copy slicing of arrays |

**Container vs Flat:**
- **Container:** Holds references to objects (any type) → `list`, `tuple`, `deque`
- **Flat:** Stores values directly in memory → `str`, `bytes`, `array` (more compact)

## When to Use Which

| Use Case | Best Choice |
|----------|-------------|
| General collection, need to modify | `list` |
| Fixed data, use as dict key/set element | `tuple` |
| Record with named fields | `namedtuple` or `@dataclass` |
| Large numeric arrays | `array.array` or `numpy.ndarray` |
| Queue (FIFO) | `collections.deque` |
| Stack (LIFO) | `list` (append/pop) or `deque` |
| Binary data processing | `bytes` / `bytearray` |
| Memory-efficient slice operations | `memoryview` |
| Text processing | `str` |

---

## 1. List Comprehensions

### Basic Syntax

```python
# Basic listcomp
squares = [x**2 for x in range(10)]
# [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]

# With condition (filter)
evens = [x for x in range(10) if x % 2 == 0]
# [0, 2, 4, 6, 8]

# Transform and filter
codes = [ord(c) for c in 'Hello' if c.isupper()]
# [72]
```

### Cartesian Product

```python
colors = ['black', 'white']
sizes = ['S', 'M', 'L']

# All combinations
tshirts = [(c, s) for c in colors for s in sizes]
# [('black', 'S'), ('black', 'M'), ('black', 'L'),
#  ('white', 'S'), ('white', 'M'), ('white', 'L')]

# Order matters: swap loops to change order
tshirts = [(c, s) for s in sizes for c in colors]
# [('black', 'S'), ('white', 'S'), ('black', 'M'), ...]
```

### Walrus Operator in Listcomps (Python 3.8+)

```python
# Compute once, use twice
results = [y for x in data if (y := expensive(x)) > threshold]

# y remains accessible after listcomp
```

### Nested Listcomps

```python
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

# Flatten
flat = [x for row in matrix for x in row]
# [1, 2, 3, 4, 5, 6, 7, 8, 9]

# Transpose
transposed = [[row[i] for row in matrix] for i in range(3)]
# [[1, 4, 7], [2, 5, 8], [3, 6, 9]]
```

---

## 2. Generator Expressions

**Use genexp when you don't need the full list in memory.**

```python
# Genexp syntax: parentheses instead of brackets
symbols = '$¢£¥€¤'

# Build tuple
t = tuple(ord(s) for s in symbols)

# Build array
import array
a = array.array('I', (ord(s) for s in symbols))

# Sum without building list
total = sum(x**2 for x in range(1000000))

# Single argument: no extra parens needed
''.join(str(x) for x in range(5))  # '01234'
```

---

## 3. Tuple Unpacking

### Basic Unpacking

```python
# Parallel assignment
coords = (33.94, -118.40)
lat, lon = coords

# Swap values (no temp variable)
a, b = b, a

# Unpack in function call
t = (20, 8)
quotient, remainder = divmod(*t)

# Ignore values with _
_, filename = os.path.split('/path/to/file.txt')
```

### Star `*` for Excess Items

```python
a, b, *rest = range(5)
# a=0, b=1, rest=[2, 3, 4]

a, *middle, z = range(5)
# a=0, middle=[1, 2, 3], z=4

*head, last = range(5)
# head=[0, 1, 2, 3], last=4

# Rest can be empty
a, b, *rest = [1, 2]
# a=1, b=2, rest=[]
```

### Nested Unpacking

```python
metro = ('Tokyo', 'JP', 36.9, (35.68, 139.69))
name, country, pop, (lat, lon) = metro

# In loops
data = [('Alice', (95, 88)), ('Bob', (78, 92))]
for name, (score1, score2) in data:
    print(f'{name}: {score1}, {score2}')
```

### Star in Literals and Calls

```python
# In function calls
def f(a, b, c, d):
    return a + b + c + d

f(*[1, 2], 3, *[4])  # 10

# In sequence literals
[*range(3), 3, 4]     # [0, 1, 2, 3, 4]
(*range(3), 3, 4)     # (0, 1, 2, 3, 4)
{*range(3), 3, *[4]}  # {0, 1, 2, 3, 4}
```

---

## 4. Slicing

### Basic Slicing

```python
s = 'bicycle'

s[::3]    # 'bye' - every 3rd char
s[::-1]   # 'elcycib' - reverse
s[::-2]   # 'eccb' - reverse, every 2nd

# Slice object
SEQ = slice(1, 4)
s[SEQ]    # 'icy'
```

### Multi-dimensional Slicing (NumPy)

```python
import numpy as np
a = np.arange(12).reshape(3, 4)
# [[ 0,  1,  2,  3],
#  [ 4,  5,  6,  7],
#  [ 8,  9, 10, 11]]

a[1, 2]      # 6 (row 1, col 2)
a[1:, :2]    # rows 1+, cols 0-1
a[:, 1]      # column 1: [1, 5, 9]
```

### Slice Assignment (Mutable Sequences)

```python
l = list(range(10))

# Replace slice
l[2:5] = [20, 30]
# [0, 1, 20, 30, 5, 6, 7, 8, 9]

# Delete slice
del l[5:7]
# [0, 1, 20, 30, 5, 8, 9]

# Insert (replace empty slice)
l[3:3] = [100, 200]
# [0, 1, 20, 100, 200, 30, 5, 8, 9]

# Replace with different length
l[2:5] = [0]
# [0, 1, 0, 30, 5, 8, 9]
```

---

## 5. Sequence Operations

### Building with `+` and `*`

```python
# Concatenation
[1, 2] + [3, 4]  # [1, 2, 3, 4]

# Repetition
[0] * 3  # [0, 0, 0]

# DANGER: Mutable objects are shared!
board = [[' '] * 3] * 3  # WRONG - all rows are same list!
board = [[' '] * 3 for _ in range(3)]  # CORRECT
```

### Augmented Assignment

```python
# += creates new object for immutable, modifies for mutable
t = (1, 2)
t += (3, 4)  # New tuple created

l = [1, 2]
l += [3, 4]  # Same list extended (uses __iadd__)

# Equivalent to:
l.extend([3, 4])
```

### Sorting

```python
# list.sort() - in place, returns None
fruits = ['banana', 'apple', 'cherry']
fruits.sort()  # Modifies fruits

# sorted() - returns new list, works on any iterable
sorted(fruits)
sorted(fruits, reverse=True)
sorted(fruits, key=len)
sorted(fruits, key=str.lower)

# Multiple keys
data = [('alice', 25), ('bob', 20), ('carol', 25)]
sorted(data, key=lambda x: (x[1], x[0]))  # By age, then name
```

### Searching

```python
# index() - raises ValueError if not found
l = [1, 2, 3, 2, 1]
l.index(2)        # 1 (first occurrence)
l.index(2, 2)     # 3 (start from index 2)

# count()
l.count(2)        # 2

# in operator (O(n) for list)
2 in l            # True
```

---

## 6. `array.array`

**Best for:** Large sequences of numbers. Memory-efficient (no object overhead).

```python
from array import array

# Type codes: 'b'=signed char, 'B'=unsigned char, 'h'=short,
# 'i'=int, 'l'=long, 'f'=float, 'd'=double

# Create array of floats
floats = array('d', (random() for _ in range(10**7)))

# Fast binary I/O
with open('floats.bin', 'wb') as f:
    floats.tofile(f)

with open('floats.bin', 'rb') as f:
    floats2 = array('d')
    floats2.fromfile(f, 10**7)

# Convert to/from bytes
floats.tobytes()
floats.frombytes(data)
```

---

## 7. `collections.deque`

**Best for:** Queues, stacks, or when you need fast append/pop from both ends.

```python
from collections import deque

# Create with maxlen (oldest items dropped when full)
dq = deque(range(5), maxlen=5)
# deque([0, 1, 2, 3, 4], maxlen=5)

# Append/pop both ends (O(1))
dq.append(5)       # Right: [1, 2, 3, 4, 5]
dq.appendleft(-1)  # Left: [-1, 1, 2, 3, 4]
dq.pop()           # 4
dq.popleft()       # -1

# Rotate (positive = right)
dq = deque([1, 2, 3, 4, 5])
dq.rotate(2)   # [4, 5, 1, 2, 3]
dq.rotate(-2)  # [1, 2, 3, 4, 5]

# Extend both ends
dq.extend([6, 7])        # Right
dq.extendleft([-2, -1])  # Left (note: reversed order)
```

### Queue Pattern (FIFO)

```python
from collections import deque

queue = deque()
queue.append('task1')   # Enqueue
queue.append('task2')
task = queue.popleft()  # Dequeue: 'task1'
```

### Stack Pattern (LIFO)

```python
# Using list (simpler for stacks)
stack = []
stack.append('a')  # Push
stack.append('b')
item = stack.pop() # Pop: 'b'

# Or use deque
stack = deque()
stack.append('a')
item = stack.pop()
```

---

## 8. `memoryview`

**Best for:** Zero-copy slicing of binary data (arrays, bytes).

```python
from array import array

# Create array
numbers = array('h', [-2, -1, 0, 1, 2])  # signed short

# Create memoryview (no copy)
mv = memoryview(numbers)

# Slice creates new memoryview (still no copy)
mv_slice = mv[2:4]

# Modify through memoryview affects original
mv_slice[0] = 99
# numbers is now array('h', [-2, -1, 99, 1, 2])

# Cast to different type
mv_bytes = mv.cast('B')  # View as bytes
len(mv_bytes)  # 10 (5 shorts × 2 bytes)
```

---

## 9. Pattern Matching with Sequences (Python 3.10+)

```python
def handle(command):
    match command:
        case ['quit']:
            return 'Goodbye'
        case ['move', direction]:
            return f'Moving {direction}'
        case ['move', direction, distance]:
            return f'Moving {direction} by {distance}'
        case ['color', r, g, b]:
            return f'RGB({r}, {g}, {b})'
        case [cmd, *args]:
            return f'Unknown: {cmd} with {args}'
        case _:
            return 'Invalid command'

handle(['move', 'north'])       # 'Moving north'
handle(['color', 255, 128, 0])  # 'RGB(255, 128, 0)'
handle(['foo', 1, 2, 3])        # 'Unknown: foo with [1, 2, 3]'
```

### Type Matching in Patterns

```python
match point:
    case [int(x), int(y)]:      # Match only if both are int
        print(f'Integer point: {x}, {y}')
    case [float(x), float(y)]:  # Match only if both are float
        print(f'Float point: {x}, {y}')
```

---

## Common Patterns

### Safe Index Access

```python
# Get with default (no IndexError)
def get(seq, index, default=None):
    try:
        return seq[index]
    except IndexError:
        return default

# Or use slicing (returns empty, not error)
seq[5:6]  # [] if seq has 5 or fewer items
```

### Chunk Iteration

```python
def chunks(seq, size):
    for i in range(0, len(seq), size):
        yield seq[i:i+size]

list(chunks([1,2,3,4,5,6,7], 3))
# [[1, 2, 3], [4, 5, 6], [7]]
```

### Sliding Window

```python
from collections import deque

def sliding_window(seq, n):
    it = iter(seq)
    win = deque(maxlen=n)
    for _ in range(n):
        win.append(next(it))
    yield tuple(win)
    for item in it:
        win.append(item)
        yield tuple(win)

list(sliding_window([1,2,3,4,5], 3))
# [(1, 2, 3), (2, 3, 4), (3, 4, 5)]
```

### Flatten Nested Lists

```python
from itertools import chain

nested = [[1, 2], [3, 4], [5]]
flat = list(chain.from_iterable(nested))
# [1, 2, 3, 4, 5]

# Or with listcomp (one level)
flat = [x for sublist in nested for x in sublist]
```

---

## Performance Notes

| Operation | list | tuple | deque | array |
|-----------|------|-------|-------|-------|
| Index access | O(1) | O(1) | O(n) | O(1) |
| Append right | O(1)* | N/A | O(1) | O(1)* |
| Append left | O(n) | N/A | O(1) | O(n) |
| Pop right | O(1) | N/A | O(1) | O(1) |
| Pop left | O(n) | N/A | O(1) | O(n) |
| Insert middle | O(n) | N/A | O(n) | O(n) |
| Memory | Higher | Lower | Higher | Lowest |

*Amortized O(1)

- **list:** Best all-rounder, use by default
- **tuple:** ~20% faster creation, less memory, hashable
- **deque:** Use when you need fast operations on both ends
- **array:** Use for large numeric data (10x less memory than list of floats)
