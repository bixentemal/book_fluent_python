# A Pythonic Object - Practical Memo

## Core Idea

A "Pythonic" object behaves like built-in types. Users can use familiar operations (`repr()`, `len()`, `format()`, iteration, etc.) without learning special methods.

Achieve this by implementing the right **special methods** (dunder methods).

---

## Object Representations

### `__repr__` vs `__str__`

```python
class Vector2d:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)

    def __repr__(self):
        # For developers - unambiguous, ideally valid Python
        class_name = type(self).__name__
        return f'{class_name}({self.x!r}, {self.y!r})'

    def __str__(self):
        # For users - readable
        return f'({self.x}, {self.y})'
```

| Method | Called by | Purpose |
|--------|-----------|---------|
| `__repr__` | `repr()`, debugger, console | Developer view, should be unambiguous |
| `__str__` | `str()`, `print()` | User-friendly view |

**Rule:** Always implement `__repr__`. Implement `__str__` only if you need different output.

### `__bytes__`

```python
from array import array

class Vector2d:
    typecode = 'd'  # 8-byte double float

    def __bytes__(self):
        return (bytes([ord(self.typecode)]) +
                bytes(array(self.typecode, [self.x, self.y])))
```

---

## Alternative Constructors with `@classmethod`

```python
class Vector2d:
    typecode = 'd'

    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)

    @classmethod
    def frombytes(cls, octets):
        """Alternative constructor from bytes."""
        typecode = chr(octets[0])
        memv = memoryview(octets[1:]).cast(typecode)
        return cls(*memv)  # cls, not Vector2d - works with subclasses!

# Usage
v = Vector2d(3, 4)
v_bytes = bytes(v)
v_copy = Vector2d.frombytes(v_bytes)
```

**Key points:**
- First argument is the class itself (`cls`), not an instance
- Use `cls(...)` to construct, enabling subclass compatibility
- Common pattern: `frombytes`, `fromstring`, `fromjson`, etc.

---

## `@classmethod` vs `@staticmethod`

```python
class Demo:
    @classmethod
    def class_method(cls, *args):
        return f'cls={cls}, args={args}'

    @staticmethod
    def static_method(*args):
        return f'args={args}'

Demo.class_method('a')     # cls=<class 'Demo'>, args=('a',)
Demo.static_method('a')    # args=('a',)
```

| Decorator | First Argument | Use Case |
|-----------|----------------|----------|
| `@classmethod` | `cls` (the class) | Alternative constructors, class-level operations |
| `@staticmethod` | None | Utility functions (rare - often better as module functions) |

**Advice:** `@staticmethod` is rarely needed. If a function doesn't need `self` or `cls`, consider making it a module-level function instead.

---

## Formatted Displays with `__format__`

```python
class Vector2d:
    def __format__(self, fmt_spec=''):
        # Apply format spec to each component
        components = (format(c, fmt_spec) for c in (self.x, self.y))
        return '({}, {})'.format(*components)

v = Vector2d(3, 4)
format(v)           # '(3.0, 4.0)'
format(v, '.2f')    # '(3.00, 4.00)'
f'{v:.3e}'          # '(3.000e+00, 4.000e+00)'
```

### Custom Format Codes

```python
import math

class Vector2d:
    def angle(self):
        return math.atan2(self.y, self.x)

    def __format__(self, fmt_spec=''):
        if fmt_spec.endswith('p'):  # Polar coordinates
            fmt_spec = fmt_spec[:-1]
            coords = (abs(self), self.angle())
            outer_fmt = '<{}, {}>'
        else:  # Cartesian coordinates
            coords = (self.x, self.y)
            outer_fmt = '({}, {})'
        components = (format(c, fmt_spec) for c in coords)
        return outer_fmt.format(*components)

v = Vector2d(1, 1)
format(v, 'p')       # '<1.4142135623730951, 0.7853981633974483>'
format(v, '.3fp')    # '<1.414, 0.785>'
```

---

## Making Objects Hashable

To use objects as dict keys or in sets, implement `__hash__` and `__eq__`:

```python
class Vector2d:
    def __init__(self, x, y):
        self.__x = float(x)  # Private (immutable)
        self.__y = float(y)

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    def __eq__(self, other):
        return tuple(self) == tuple(other)

    def __hash__(self):
        return hash((self.x, self.y))

v1 = Vector2d(3, 4)
v2 = Vector2d(3, 4)
hash(v1) == hash(v2)  # True
{v1, v2}              # Works! Set with one element
{v1: 'vector'}        # Works as dict key
```

**Requirements for hashable objects:**
1. Implement `__hash__` returning an `int`
2. Implement `__eq__`
3. If `a == b`, then `hash(a) == hash(b)`
4. Object should be immutable (or at least hash-relevant attributes)

---

## Read-Only Properties with `@property`

```python
class Vector2d:
    def __init__(self, x, y):
        self.__x = float(x)  # Private attribute
        self.__y = float(y)

    @property
    def x(self):
        """Read-only x component."""
        return self.__x

    @property
    def y(self):
        """Read-only y component."""
        return self.__y

v = Vector2d(3, 4)
v.x          # 3.0 - works
v.x = 10     # AttributeError: can't set attribute
```

---

## Private and "Protected" Attributes

### Single Underscore: "Protected" (Convention)

```python
class MyClass:
    def __init__(self):
        self._internal = 42  # "Protected" - don't touch from outside
```

- Just a convention, not enforced
- Signals "internal use only"
- Not imported by `from module import *`

### Double Underscore: Name Mangling

```python
class MyClass:
    def __init__(self):
        self.__private = 42  # Mangled to _MyClass__private

obj = MyClass()
obj.__private         # AttributeError
obj._MyClass__private # 42 - still accessible if you know the name!
```

**Purpose:** Prevent accidental overriding in subclasses, not security.

```python
class Parent:
    def __init__(self):
        self.__x = 1  # Becomes _Parent__x

class Child(Parent):
    def __init__(self):
        super().__init__()
        self.__x = 2  # Becomes _Child__x - different attribute!
```

---

## Positional Pattern Matching with `__match_args__`

```python
class Vector2d:
    __match_args__ = ('x', 'y')  # Enable positional patterns

    def __init__(self, x, y):
        self.x = x
        self.y = y

# Now you can use positional patterns:
def describe(v):
    match v:
        case Vector2d(0, 0):
            return 'null vector'
        case Vector2d(0, _):
            return 'vertical'
        case Vector2d(_, 0):
            return 'horizontal'
        case Vector2d(x, y) if x == y:
            return 'diagonal'
        case _:
            return 'other'
```

---

## Saving Memory with `__slots__`

```python
class Vector2d:
    __slots__ = ('__x', '__y')  # Only these attributes allowed

    def __init__(self, x, y):
        self.__x = float(x)
        self.__y = float(y)
```

**Benefits:**
- Significant memory savings (no `__dict__` per instance)
- Faster attribute access

**Trade-offs:**
- Cannot add new attributes dynamically
- Cannot use `__dict__` for introspection
- Must redeclare `__slots__` in subclasses
- Instances cannot be weakly referenced (unless `'__weakref__'` in `__slots__`)

**When to use:** Classes with many instances (millions) where memory matters.

---

## Making Objects Iterable

```python
class Vector2d:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __iter__(self):
        return iter((self.x, self.y))
        # Or: yield self.x; yield self.y

v = Vector2d(3, 4)
x, y = v              # Unpacking works
list(v)               # [3.0, 4.0]
tuple(v)              # (3.0, 4.0)
```

---

## Absolute Value and Boolean

```python
import math

class Vector2d:
    def __abs__(self):
        """Return magnitude (length) of vector."""
        return math.hypot(self.x, self.y)

    def __bool__(self):
        """Vector is falsy if magnitude is zero."""
        return bool(abs(self))

v1 = Vector2d(3, 4)
abs(v1)              # 5.0
bool(v1)             # True

v0 = Vector2d(0, 0)
abs(v0)              # 0.0
bool(v0)             # False
```

---

## Complete Example: Pythonic Vector2d

```python
from array import array
import math

class Vector2d:
    __match_args__ = ('x', 'y')
    __slots__ = ('__x', '__y')
    typecode = 'd'

    def __init__(self, x, y):
        self.__x = float(x)
        self.__y = float(y)

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    def __iter__(self):
        return iter((self.x, self.y))

    def __repr__(self):
        class_name = type(self).__name__
        return f'{class_name}({self.x!r}, {self.y!r})'

    def __str__(self):
        return str(tuple(self))

    def __bytes__(self):
        return (bytes([ord(self.typecode)]) +
                bytes(array(self.typecode, self)))

    def __eq__(self, other):
        return tuple(self) == tuple(other)

    def __hash__(self):
        return hash((self.x, self.y))

    def __abs__(self):
        return math.hypot(self.x, self.y)

    def __bool__(self):
        return bool(abs(self))

    def __format__(self, fmt_spec=''):
        if fmt_spec.endswith('p'):
            fmt_spec = fmt_spec[:-1]
            coords = (abs(self), self.angle())
            outer_fmt = '<{}, {}>'
        else:
            coords = self
            outer_fmt = '({}, {})'
        components = (format(c, fmt_spec) for c in coords)
        return outer_fmt.format(*components)

    def angle(self):
        return math.atan2(self.y, self.x)

    @classmethod
    def frombytes(cls, octets):
        typecode = chr(octets[0])
        memv = memoryview(octets[1:]).cast(typecode)
        return cls(*memv)
```

---

## Quick Reference: Essential Special Methods

| Method | Triggered By | Purpose |
|--------|--------------|---------|
| `__repr__` | `repr(obj)` | Developer string |
| `__str__` | `str(obj)`, `print()` | User string |
| `__bytes__` | `bytes(obj)` | Byte representation |
| `__format__` | `format(obj, spec)`, f-strings | Formatted output |
| `__hash__` | `hash(obj)`, dict key, set | Hash value |
| `__eq__` | `obj == other` | Equality |
| `__bool__` | `bool(obj)`, `if obj:` | Truth value |
| `__abs__` | `abs(obj)` | Magnitude |
| `__iter__` | `for x in obj`, unpacking | Make iterable |

---

## Checklist: When to Implement What

| Goal | Implement |
|------|-----------|
| Pretty printing for debugging | `__repr__` |
| User-friendly display | `__str__` |
| Use as dict key / in set | `__hash__` + `__eq__` + immutability |
| Support `format()` and f-strings | `__format__` |
| Support unpacking (`x, y = obj`) | `__iter__` |
| Support `abs()` | `__abs__` |
| Control truthiness | `__bool__` |
| Alternative constructor | `@classmethod` |
| Positional pattern matching | `__match_args__` |
| Memory optimization | `__slots__` |
