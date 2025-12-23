# Special Methods for Sequences - Practical Memo

## Core Idea

You don't need to inherit from any special class to create a sequence in Python. Just implement the **sequence protocol**: `__len__` and `__getitem__`.

> "Don't check whether it is-a duck: check whether it quacks-like-a duck, walks-like-a duck..."
> — Alex Martelli

---

## The Sequence Protocol

### Basic Implementation

```python
class MySequence:
    def __init__(self, items):
        self._items = list(items)

    def __len__(self):
        return len(self._items)

    def __getitem__(self, index):
        return self._items[index]

# Now it behaves like a sequence!
seq = MySequence([1, 2, 3, 4, 5])
len(seq)           # 5
seq[0]             # 1
seq[-1]            # 5
seq[1:3]           # [2, 3] - slicing works!
for item in seq:   # iteration works!
    print(item)
3 in seq           # True - containment works!
```

**What you get for free by implementing `__getitem__`:**
- Iteration (`for item in seq`)
- Containment (`item in seq`)
- Indexing (`seq[0]`, `seq[-1]`)
- Slicing (`seq[1:3]`)

---

## Protocols and Duck Typing

A **protocol** is an informal interface defined by documentation, not code.

| Protocol | Methods Required | Enables |
|----------|------------------|---------|
| Sequence | `__len__`, `__getitem__` | Indexing, slicing, iteration, containment |
| Iterable | `__iter__` | Iteration with `for` |
| Sized | `__len__` | `len()` function |
| Container | `__contains__` | `in` operator (explicit) |

**Duck typing:** If it implements the right methods, it IS that type (for practical purposes).

---

## Proper Slicing Support

### How Slicing Works

```python
class MySeq:
    def __getitem__(self, index):
        return index  # Just return what we receive

s = MySeq()
s[1]        # 1 (integer)
s[1:4]      # slice(1, 4, None)
s[1:4:2]    # slice(1, 4, 2)
s[1:4, 9]   # (slice(1, 4, None), 9) - tuple!
```

When you use slice notation, Python creates a `slice` object and passes it to `__getitem__`.

### Slice-Aware `__getitem__`

```python
import operator

class Vector:
    def __init__(self, components):
        self._components = list(components)

    def __len__(self):
        return len(self._components)

    def __getitem__(self, key):
        if isinstance(key, slice):
            # Return new Vector from sliced components
            cls = type(self)
            return cls(self._components[key])
        # Use operator.index to convert key to int
        index = operator.index(key)
        return self._components[index]

v = Vector([0, 1, 2, 3, 4])
v[1:3]  # Vector([1, 2]) - returns Vector, not list!
v[0]    # 0.0
```

**Key points:**
- Use `isinstance(key, slice)` to detect slicing
- Use `type(self)` to get the class (works with subclasses)
- Use `operator.index(key)` instead of `int(key)` for proper error messages

### The `slice.indices()` Method

Normalizes slice parameters for a given length:

```python
s = slice(None, 10, 2)
s.indices(5)  # (0, 5, 2) - normalized for length 5

s = slice(-3, None, None)
s.indices(5)  # (2, 5, 1) - negative index converted
```

---

## Dynamic Attribute Access with `__getattr__`

Provide virtual attributes that don't exist in `__dict__`:

```python
class Vector:
    __match_args__ = ('x', 'y', 'z', 't')

    def __init__(self, components):
        self._components = list(components)

    def __getattr__(self, name):
        cls = type(self)
        try:
            pos = cls.__match_args__.index(name)
        except ValueError:
            pos = -1
        if 0 <= pos < len(self._components):
            return self._components[pos]
        raise AttributeError(f'{cls.__name__!r} has no attribute {name!r}')

v = Vector([1, 2, 3, 4, 5])
v.x  # 1 - accesses v._components[0]
v.y  # 2 - accesses v._components[1]
v.z  # 3
v.t  # 4
```

**How `__getattr__` works:**
1. Python looks for attribute in instance `__dict__`
2. If not found, looks in class and superclasses
3. If still not found, calls `__getattr__(self, name)`

---

## Blocking Attribute Setting with `__setattr__`

**Problem:** If you use `__getattr__`, users can accidentally create conflicting attributes:

```python
v = Vector([1, 2, 3])
v.x        # 1 (from __getattr__)
v.x = 10   # Creates instance attribute!
v.x        # 10 (from __dict__, __getattr__ not called!)
```

**Solution:** Implement `__setattr__` to block unwanted assignments:

```python
class Vector:
    __match_args__ = ('x', 'y', 'z', 't')

    def __setattr__(self, name, value):
        cls = type(self)
        if len(name) == 1:
            if name in cls.__match_args__:
                error = f'readonly attribute {name!r}'
            elif name.islower():
                error = f"can't set attributes 'a' to 'z' in {cls.__name__!r}"
            else:
                error = ''
            if error:
                raise AttributeError(error)
        super().__setattr__(name, value)  # Default behavior

v = Vector([1, 2, 3])
v.x = 10  # AttributeError: readonly attribute 'x'
```

**Important:** Always call `super().__setattr__()` for attributes you want to allow!

---

## Hashing with `functools.reduce`

### The Problem

For a multi-component object, building a tuple just to hash it is expensive:

```python
# Expensive for large vectors
def __hash__(self):
    return hash(tuple(self._components))
```

### Solution: XOR with reduce

```python
import functools
import operator

class Vector:
    def __hash__(self):
        hashes = (hash(x) for x in self._components)
        return functools.reduce(operator.xor, hashes, 0)
```

**How `reduce` works:**
```python
# reduce(fn, [a, b, c, d]) computes:
# fn(fn(fn(a, b), c), d)

# Example: XOR of [1, 2, 3]
# 1 ^ 2 = 3
# 3 ^ 3 = 0
functools.reduce(operator.xor, [1, 2, 3])  # 0
```

The third argument (`0`) is the initial value (identity for XOR).

---

## Faster Equality with `zip`

### Naive Approach (Slow)

```python
def __eq__(self, other):
    return tuple(self) == tuple(other)  # Creates two tuples!
```

### Optimized Approach

```python
def __eq__(self, other):
    # Quick length check first
    if len(self) != len(other):
        return False
    # Compare element by element
    for a, b in zip(self, other):
        if a != b:
            return False
    return True
```

### Most Pythonic (using `all`)

```python
def __eq__(self, other):
    return len(self) == len(other) and all(a == b for a, b in zip(self, other))
```

**Why this is faster:**
- No tuple creation
- Short-circuits on first difference
- Uses generator expression (lazy evaluation)

---

## Safe Representation with `reprlib`

For sequences that may have many elements:

```python
import reprlib

class Vector:
    def __repr__(self):
        # reprlib.repr limits output length
        components = reprlib.repr(self._components)
        # Remove 'array('d', ' prefix if using array
        components = components[components.find('['):-1]
        return f'Vector({components})'

v = Vector(range(100))
repr(v)  # Vector([0.0, 1.0, 2.0, 3.0, 4.0, ...])
```

**Why use `reprlib.repr`:**
- Limits output to reasonable length
- Adds `...` to indicate truncation
- Prevents huge outputs in logs/debugger

---

## Custom Formatting with `__format__`

```python
import math
import itertools

class Vector:
    def __format__(self, fmt_spec=''):
        if fmt_spec.endswith('h'):  # Hyperspherical coordinates
            fmt_spec = fmt_spec[:-1]
            coords = itertools.chain([abs(self)], self.angles())
            outer_fmt = '<{}>'
        else:  # Cartesian coordinates
            coords = self
            outer_fmt = '({})'
        components = (format(c, fmt_spec) for c in coords)
        return outer_fmt.format(', '.join(components))

v = Vector([1, 1, 1])
format(v, '.2f')   # '(1.00, 1.00, 1.00)'
format(v, '.3fh')  # '<1.732, 0.955, 0.785>' (magnitude, angles)
```

---

## Complete Example: Vector Class

```python
from array import array
import reprlib
import math
import functools
import operator

class Vector:
    typecode = 'd'
    __match_args__ = ('x', 'y', 'z', 't')

    def __init__(self, components):
        self._components = array(self.typecode, components)

    def __iter__(self):
        return iter(self._components)

    def __repr__(self):
        components = reprlib.repr(self._components)
        components = components[components.find('['):-1]
        return f'Vector({components})'

    def __str__(self):
        return str(tuple(self))

    def __bytes__(self):
        return bytes([ord(self.typecode)]) + bytes(self._components)

    def __len__(self):
        return len(self._components)

    def __getitem__(self, key):
        if isinstance(key, slice):
            cls = type(self)
            return cls(self._components[key])
        index = operator.index(key)
        return self._components[index]

    def __getattr__(self, name):
        cls = type(self)
        try:
            pos = cls.__match_args__.index(name)
        except ValueError:
            pos = -1
        if 0 <= pos < len(self._components):
            return self._components[pos]
        raise AttributeError(f'{cls.__name__!r} has no attribute {name!r}')

    def __setattr__(self, name, value):
        cls = type(self)
        if len(name) == 1 and name.islower():
            if name in cls.__match_args__:
                error = f'readonly attribute {name!r}'
            else:
                error = f"can't set single letter attribute in {cls.__name__!r}"
            raise AttributeError(error)
        super().__setattr__(name, value)

    def __eq__(self, other):
        return len(self) == len(other) and all(a == b for a, b in zip(self, other))

    def __hash__(self):
        hashes = (hash(x) for x in self._components)
        return functools.reduce(operator.xor, hashes, 0)

    def __abs__(self):
        return math.hypot(*self)

    def __bool__(self):
        return bool(abs(self))

    @classmethod
    def frombytes(cls, octets):
        typecode = chr(octets[0])
        memv = memoryview(octets[1:]).cast(typecode)
        return cls(memv)
```

---

## Quick Reference

| Goal | Method | Notes |
|------|--------|-------|
| Length | `__len__` | Return `int` |
| Indexing | `__getitem__` | Handle both `int` and `slice` |
| Iteration | `__iter__` | Or just `__getitem__` |
| Containment | `__contains__` | Or falls back to iteration |
| Virtual attributes | `__getattr__` | Called when attribute not found |
| Block attribute setting | `__setattr__` | Call `super().__setattr__` for allowed attrs |
| Hashing | `__hash__` | Use `reduce` with `xor` for components |
| Safe repr | `reprlib.repr` | Limits output length |

---

## Key Takeaways

1. **Implement `__len__` and `__getitem__`** to make any class behave like a sequence

2. **Handle slices in `__getitem__`** by checking `isinstance(key, slice)`

3. **Return same type from slicing** using `type(self)(sliced_data)`

4. **Use `operator.index()`** instead of `int()` for index conversion

5. **Pair `__getattr__` with `__setattr__`** to prevent inconsistencies

6. **Use `functools.reduce` with `operator.xor`** for efficient hashing

7. **Use `zip` and `all`** for efficient equality comparison

8. **Use `reprlib.repr`** for safe representation of large collections
