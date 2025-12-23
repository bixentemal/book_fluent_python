# Python Data Model - Practical Memo

## What is the Data Model?

The Python Data Model defines **special methods** (dunder methods) that let your objects integrate with Python's built-in operations:
- `len(obj)` calls `obj.__len__()`
- `obj[key]` calls `obj.__getitem__(key)`
- `for x in obj` uses `obj.__iter__()` or `obj.__getitem__()`

**Key principle:** Implement special methods, don't call them directly. Let Python call them.

---

## Quick Reference: Special Methods by Category

### Core Object Methods

| Method | Triggered By | Purpose |
|--------|--------------|---------|
| `__init__(self, ...)` | `MyClass(...)` | Initialize instance |
| `__new__(cls, ...)` | `MyClass(...)` | Create instance (before `__init__`) |
| `__del__(self)` | Garbage collection | Destructor (rarely needed) |
| `__repr__(self)` | `repr(obj)`, console | Developer string (unambiguous) |
| `__str__(self)` | `str(obj)`, `print()` | User-friendly string |
| `__bytes__(self)` | `bytes(obj)` | Byte representation |
| `__format__(self, spec)` | `format(obj, spec)`, f-strings | Custom formatting |

### Boolean & Comparison

| Method | Triggered By | Purpose |
|--------|--------------|---------|
| `__bool__(self)` | `bool(obj)`, `if obj:` | Truth value |
| `__eq__(self, other)` | `obj == other` | Equality |
| `__ne__(self, other)` | `obj != other` | Inequality (defaults to `not __eq__`) |
| `__lt__(self, other)` | `obj < other` | Less than |
| `__le__(self, other)` | `obj <= other` | Less than or equal |
| `__gt__(self, other)` | `obj > other` | Greater than |
| `__ge__(self, other)` | `obj >= other` | Greater or equal |
| `__hash__(self)` | `hash(obj)`, dict key | Hash value |

### Container / Sequence

| Method | Triggered By | Purpose |
|--------|--------------|---------|
| `__len__(self)` | `len(obj)` | Length |
| `__getitem__(self, key)` | `obj[key]` | Get item |
| `__setitem__(self, key, val)` | `obj[key] = val` | Set item |
| `__delitem__(self, key)` | `del obj[key]` | Delete item |
| `__contains__(self, item)` | `item in obj` | Membership test |
| `__iter__(self)` | `for x in obj`, `iter(obj)` | Return iterator |
| `__reversed__(self)` | `reversed(obj)` | Reverse iterator |
| `__missing__(self, key)` | `obj[key]` (dict subclass) | Handle missing key |

### Attribute Access

| Method | Triggered By | Purpose |
|--------|--------------|---------|
| `__getattr__(self, name)` | `obj.x` (when not found) | Fallback attribute access |
| `__getattribute__(self, name)` | `obj.x` (always) | All attribute access |
| `__setattr__(self, name, val)` | `obj.x = val` | Set attribute |
| `__delattr__(self, name)` | `del obj.x` | Delete attribute |
| `__dir__(self)` | `dir(obj)` | List attributes |

### Callable & Context Manager

| Method | Triggered By | Purpose |
|--------|--------------|---------|
| `__call__(self, ...)` | `obj(...)` | Make object callable |
| `__enter__(self)` | `with obj as x:` | Context manager enter |
| `__exit__(self, exc_type, exc_val, tb)` | End of `with` block | Context manager exit |

### Numeric Operators

| Method | Triggered By | Reverse Method |
|--------|--------------|----------------|
| `__add__(self, other)` | `obj + other` | `__radd__` |
| `__sub__(self, other)` | `obj - other` | `__rsub__` |
| `__mul__(self, other)` | `obj * other` | `__rmul__` |
| `__truediv__(self, other)` | `obj / other` | `__rtruediv__` |
| `__floordiv__(self, other)` | `obj // other` | `__rfloordiv__` |
| `__mod__(self, other)` | `obj % other` | `__rmod__` |
| `__pow__(self, other)` | `obj ** other` | `__rpow__` |
| `__matmul__(self, other)` | `obj @ other` | `__rmatmul__` |

### Augmented Assignment

| Method | Triggered By |
|--------|--------------|
| `__iadd__(self, other)` | `obj += other` |
| `__isub__(self, other)` | `obj -= other` |
| `__imul__(self, other)` | `obj *= other` |

### Unary Operators

| Method | Triggered By |
|--------|--------------|
| `__neg__(self)` | `-obj` |
| `__pos__(self)` | `+obj` |
| `__abs__(self)` | `abs(obj)` |
| `__invert__(self)` | `~obj` |

---

## Common Implementations

### 1. Basic Class with `__repr__` and `__eq__`

```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        # Unambiguous, ideally valid Python to recreate object
        return f'Point({self.x!r}, {self.y!r})'

    def __eq__(self, other):
        if not isinstance(other, Point):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        # Required if __eq__ is defined and you want dict keys/sets
        return hash((self.x, self.y))

p = Point(1, 2)
repr(p)      # "Point(1, 2)"
p == Point(1, 2)  # True
{p: 'value'}      # Works as dict key
```

### 2. Sequence-like Object

```python
class Deck:
    def __init__(self):
        self._cards = [f'{r}{s}' for s in '♠♥♦♣' for r in 'A23456789TJQK']

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, position):
        return self._cards[position]

    # Optional: make it mutable
    def __setitem__(self, position, value):
        self._cards[position] = value

deck = Deck()
len(deck)           # 52
deck[0]             # 'A♠'
deck[-1]            # 'K♣'
deck[:3]            # ['A♠', '2♠', '3♠'] - slicing works!
'A♠' in deck        # True - __contains__ via __getitem__
for card in deck:   # Iteration works via __getitem__
    print(card)
random.choice(deck) # Works!
```

### 3. Numeric Type with Operators

```python
import math

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f'Vector({self.x}, {self.y})'

    def __abs__(self):
        return math.hypot(self.x, self.y)

    def __bool__(self):
        return bool(abs(self))  # False if zero vector

    def __add__(self, other):
        if not isinstance(other, Vector):
            return NotImplemented
        return Vector(self.x + other.x, self.y + other.y)

    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar):
        return self * scalar  # Handle 3 * vector

v1 = Vector(2, 4)
v2 = Vector(2, 1)
v1 + v2         # Vector(4, 5)
v1 * 3          # Vector(6, 12)
3 * v1          # Vector(6, 12) - needs __rmul__
abs(v1)         # 4.47...
bool(Vector(0, 0))  # False
```

### 4. Context Manager

```python
class Timer:
    def __enter__(self):
        self.start = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, traceback):
        self.elapsed = time.perf_counter() - self.start
        return False  # Don't suppress exceptions

with Timer() as t:
    # do something
    time.sleep(0.1)
print(f'Elapsed: {t.elapsed:.3f}s')
```

### 5. Callable Object

```python
class Averager:
    def __init__(self):
        self._series = []

    def __call__(self, value):
        self._series.append(value)
        return sum(self._series) / len(self._series)

avg = Averager()
avg(10)  # 10.0
avg(11)  # 10.5
avg(12)  # 11.0
```

### 6. Custom Attribute Access

```python
class DynamicAttrs:
    def __init__(self, **kwargs):
        self._data = kwargs

    def __getattr__(self, name):
        # Called only when attribute not found normally
        try:
            return self._data[name]
        except KeyError:
            raise AttributeError(f"'{type(self).__name__}' has no attribute '{name}'")

    def __setattr__(self, name, value):
        if name.startswith('_'):
            super().__setattr__(name, value)
        else:
            self._data[name] = value

obj = DynamicAttrs(x=1, y=2)
obj.x       # 1
obj.z = 3   # Stored in _data
```

---

## Best Practices

### `__repr__` vs `__str__`

```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __repr__(self):
        # For developers - unambiguous, ideally valid Python
        return f"Person({self.name!r}, {self.age!r})"

    def __str__(self):
        # For users - readable
        return f"{self.name}, {self.age} years old"

p = Person("Alice", 30)
repr(p)  # "Person('Alice', 30)"
str(p)   # "Alice, 30 years old"
print(p) # "Alice, 30 years old" (uses __str__)

# In containers, __repr__ is used:
[p]      # [Person('Alice', 30)]
```

**Rule:** Always implement `__repr__`. Implement `__str__` only if you need different user output.

### Return `NotImplemented` for Type Mismatches

```python
def __eq__(self, other):
    if not isinstance(other, MyClass):
        return NotImplemented  # NOT raise NotImplementedError!
    return self.value == other.value

def __add__(self, other):
    if not isinstance(other, MyClass):
        return NotImplemented  # Allows Python to try other.__radd__
    return MyClass(self.value + other.value)
```

### `__hash__` Rules

```python
# If __eq__ is defined:
# - Mutable objects: set __hash__ = None (unhashable)
# - Immutable objects: implement __hash__ using same fields as __eq__

class Immutable:
    def __init__(self, x, y):
        self._x = x
        self._y = y

    def __eq__(self, other):
        return (self._x, self._y) == (other._x, other._y)

    def __hash__(self):
        return hash((self._x, self._y))

class Mutable:
    def __eq__(self, other):
        return self.data == other.data

    __hash__ = None  # Explicitly unhashable
```

### Comparison Methods - Use `@total_ordering`

```python
from functools import total_ordering

@total_ordering
class Version:
    def __init__(self, major, minor):
        self.major = major
        self.minor = minor

    def __eq__(self, other):
        return (self.major, self.minor) == (other.major, other.minor)

    def __lt__(self, other):
        return (self.major, self.minor) < (other.major, other.minor)

    # @total_ordering provides __le__, __gt__, __ge__ automatically!

Version(1, 0) < Version(2, 0)   # True
Version(1, 0) >= Version(1, 0)  # True (auto-generated)
```

---

## Collection ABCs Quick Reference

```
Iterable ──────► __iter__
Sized ─────────► __len__
Container ─────► __contains__
      │
      ▼
Collection (combines above three)
      │
      ├──► Sequence ──► __getitem__, __len__ (+ __contains__, __iter__, __reversed__, index, count)
      │
      ├──► Mapping ───► __getitem__, __len__, __iter__ (+ keys, values, items, get, __contains__, __eq__)
      │
      └──► Set ───────► __contains__, __len__, __iter__ (+ __le__, __lt__, __eq__, __ne__, __gt__, __ge__, __and__, __or__, __sub__, __xor__)
```

---

## Summary: What to Implement When

| You Want To... | Implement |
|----------------|-----------|
| Print nicely for debugging | `__repr__` |
| Use as dict key or in set | `__hash__` + `__eq__` |
| Support `len()` | `__len__` |
| Support indexing `obj[i]` | `__getitem__` |
| Support iteration | `__iter__` (or just `__getitem__`) |
| Support `in` operator | `__contains__` (or just `__getitem__`) |
| Support `+`, `-`, `*`, etc. | `__add__`, `__sub__`, `__mul__`, etc. |
| Support `obj(...)` calls | `__call__` |
| Use with `with` statement | `__enter__` + `__exit__` |
| Support `if obj:` truth testing | `__bool__` (or `__len__`) |
| Sort instances | `__lt__` (+ `@total_ordering` for full set) |
