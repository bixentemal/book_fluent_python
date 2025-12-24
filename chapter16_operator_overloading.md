# Operator Overloading - Practical Memo

## Overview

Operator overloading allows user-defined types to work with infix operators like `+`, `*`, `@`, and comparison operators. Python strikes a balance between flexibility and safety with sensible restrictions.

---

## Python's Operator Overloading Rules

**Limitations:**
- Cannot change operators for built-in types
- Cannot create new operators, only overload existing ones
- Some operators can't be overloaded: `is`, `and`, `or`, `not`
- Bitwise operators (`&`, `|`, `~`) CAN be overloaded

**Best Practice:**
- Operators should return NEW objects, never modify operands
- Only augmented assignment operators (`+=`, `*=`) may modify `self`

---

## Unary Operators

### The Three Unary Operators

| Operator | Method | Description |
|----------|--------|-------------|
| `-x` | `__neg__` | Arithmetic negation |
| `+x` | `__pos__` | Arithmetic plus (usually returns copy) |
| `~x` | `__invert__` | Bitwise NOT (for integers: `~x == -(x+1)`) |
| `abs(x)` | `__abs__` | Absolute value |

### Implementation Example

```python
import math

class Vector:
    def __init__(self, components):
        self._components = list(components)

    def __neg__(self):
        # Return new Vector with negated components
        return Vector(-x for x in self._components)

    def __pos__(self):
        # Return copy of self
        return Vector(self._components)

    def __abs__(self):
        # Return magnitude (scalar)
        return math.hypot(*self._components)
```

**Key Rule:** Unary operators should return a NEW object of appropriate type.

---

## Infix Operators: The Dispatch Mechanism

### How Python Handles `a + b`

1. Call `a.__add__(b)` - return result unless `NotImplemented`
2. If `a.__add__` missing or returns `NotImplemented`, call `b.__radd__(a)`
3. If `b.__radd__` missing or returns `NotImplemented`, raise `TypeError`

```
a + b
  │
  ▼
a.__add__(b)
  │
  ├─ Returns value → Done!
  │
  └─ Returns NotImplemented
      │
      ▼
    b.__radd__(a)
      │
      ├─ Returns value → Done!
      │
      └─ Returns NotImplemented → TypeError
```

### NotImplemented vs NotImplementedError

```python
# NotImplemented - a SINGLETON VALUE to return from operators
def __add__(self, other):
    if not isinstance(other, MyType):
        return NotImplemented  # Let Python try __radd__
    return MyType(self.value + other.value)

# NotImplementedError - an EXCEPTION for abstract methods
def abstract_method(self):
    raise NotImplementedError("Subclasses must implement this")
```

---

## Implementing + and *

### Addition with __add__ and __radd__

```python
import itertools

class Vector:
    def __init__(self, components):
        self._components = list(components)

    def __add__(self, other):
        try:
            # zip_longest pads shorter sequence with 0
            pairs = itertools.zip_longest(
                self._components, other, fillvalue=0
            )
            return Vector(a + b for a, b in pairs)
        except TypeError:
            return NotImplemented

    def __radd__(self, other):
        # Addition is commutative, so just delegate
        return self + other
```

### Multiplication with __mul__ and __rmul__

```python
class Vector:
    def __mul__(self, scalar):
        try:
            factor = float(scalar)
        except TypeError:
            return NotImplemented
        return Vector(n * factor for n in self._components)

    def __rmul__(self, scalar):
        # Scalar multiplication is commutative
        return self * scalar
```

### Usage

```python
v1 = Vector([1, 2, 3])
v2 = Vector([4, 5, 6])

# Vector + Vector
v1 + v2  # Vector([5, 7, 9])

# Vector + tuple (works via duck typing)
v1 + (10, 20, 30)  # Vector([11, 22, 33])

# tuple + Vector (uses __radd__)
(10, 20, 30) + v1  # Vector([11, 22, 33])

# Scalar multiplication
v1 * 10  # Vector([10, 20, 30])
10 * v1  # Vector([10, 20, 30]) - uses __rmul__
```

---

## The @ Matrix Multiplication Operator

Since Python 3.5, `@` is the infix operator for matrix multiplication (dot product).

### Implementation

```python
from collections import abc

class Vector:
    def __matmul__(self, other):
        if isinstance(other, abc.Sized) and isinstance(other, abc.Iterable):
            if len(self) == len(other):
                return sum(a * b for a, b in zip(self, other))
            else:
                raise ValueError("@ requires vectors of equal length")
        return NotImplemented

    def __rmatmul__(self, other):
        return self @ other
```

### Usage

```python
v1 = Vector([1, 2, 3])
v2 = Vector([4, 5, 6])

v1 @ v2  # 1*4 + 2*5 + 3*6 = 32
[1, 2, 3] @ v2  # Also works: 32
```

---

## Rich Comparison Operators

### Special Handling

Comparison operators have different dispatch rules:

| Operator | Forward | Reverse |
|----------|---------|---------|
| `==` | `__eq__` | `__eq__` (swapped args) |
| `!=` | `__ne__` | `__ne__` (swapped args) |
| `<` | `__lt__` | `__gt__` |
| `>` | `__gt__` | `__lt__` |
| `<=` | `__le__` | `__ge__` |
| `>=` | `__ge__` | `__le__` |

**Special case for `==` and `!=`:** If both methods return `NotImplemented`, Python compares object IDs instead of raising `TypeError`.

### Implementation Example

```python
class Vector:
    def __eq__(self, other):
        if isinstance(other, Vector):
            return (len(self) == len(other) and
                    all(a == b for a, b in zip(self, other)))
        return NotImplemented  # Let Python try other.__eq__

    # __ne__ inherited from object works correctly:
    # It calls __eq__ and negates the result
```

### Be Conservative with Equality

```python
# Should Vector([1, 2]) == (1, 2)?
# Probably not! Be explicit about types.

>>> [1, 2] == (1, 2)
False  # Python is conservative here too

class Vector:
    def __eq__(self, other):
        # Only equal to other Vectors
        if isinstance(other, Vector):
            return list(self) == list(other)
        return NotImplemented
```

---

## Augmented Assignment Operators

### For Immutable Types

If you don't implement `__iadd__`, Python evaluates `a += b` as `a = a + b`:

```python
# Immutable Vector - no __iadd__ needed
v1 = Vector([1, 2, 3])
v1 += Vector([4, 5, 6])  # Creates new Vector, rebinds v1
```

### For Mutable Types

Implement `__iadd__` to modify in place:

```python
class MutableContainer:
    def __init__(self, items):
        self._items = list(items)

    def __iadd__(self, other):
        # Modify self in place
        if isinstance(other, MutableContainer):
            self._items.extend(other._items)
        else:
            try:
                self._items.extend(iter(other))
            except TypeError:
                return NotImplemented
        return self  # MUST return self!

    def __add__(self, other):
        # Return NEW object
        if isinstance(other, MutableContainer):
            return MutableContainer(self._items + other._items)
        return NotImplemented
```

**Critical Rule:** `__iadd__` must return `self` after modification!

### Difference Between + and +=

| Operator | Behavior | Strictness |
|----------|----------|------------|
| `+` | Returns new object | Usually strict on types |
| `+=` | Modifies in place | Can be more flexible |

```python
# list example
my_list + other  # other must be a list
my_list += other  # other can be any iterable
```

---

## Complete Operator Method Table

### Arithmetic Operators

| Operator | Forward | Reverse | In-place |
|----------|---------|---------|----------|
| `+` | `__add__` | `__radd__` | `__iadd__` |
| `-` | `__sub__` | `__rsub__` | `__isub__` |
| `*` | `__mul__` | `__rmul__` | `__imul__` |
| `/` | `__truediv__` | `__rtruediv__` | `__itruediv__` |
| `//` | `__floordiv__` | `__rfloordiv__` | `__ifloordiv__` |
| `%` | `__mod__` | `__rmod__` | `__imod__` |
| `**` | `__pow__` | `__rpow__` | `__ipow__` |
| `@` | `__matmul__` | `__rmatmul__` | `__imatmul__` |

### Bitwise Operators

| Operator | Forward | Reverse | In-place |
|----------|---------|---------|----------|
| `&` | `__and__` | `__rand__` | `__iand__` |
| `\|` | `__or__` | `__ror__` | `__ior__` |
| `^` | `__xor__` | `__rxor__` | `__ixor__` |
| `<<` | `__lshift__` | `__rlshift__` | `__ilshift__` |
| `>>` | `__rshift__` | `__rrshift__` | `__irshift__` |

---

## Best Practices

### DO:
1. **Return `NotImplemented`** for unsupported operand types (not `NotImplementedError`)
2. **Return new objects** from operators (don't modify operands)
3. **Return `self`** from augmented assignment operators
4. **Use duck typing** or `isinstance` with ABCs for flexible type checking
5. **Make `__radd__` delegate to `__add__`** for commutative operations

### DON'T:
1. **Don't raise `TypeError`** directly - return `NotImplemented` instead
2. **Don't modify operands** in regular operators
3. **Don't implement `__radd__`** if `__add__` only handles same-type operands
4. **Don't forget to handle `NotImplemented`** from nested operations

---

## Quick Reference

```python
class MyNumber:
    def __init__(self, value):
        self.value = value

    # Unary operators
    def __neg__(self): return MyNumber(-self.value)
    def __pos__(self): return MyNumber(self.value)
    def __abs__(self): return abs(self.value)

    # Binary operators
    def __add__(self, other):
        if isinstance(other, MyNumber):
            return MyNumber(self.value + other.value)
        try:
            return MyNumber(self.value + other)
        except TypeError:
            return NotImplemented

    def __radd__(self, other):
        return self + other  # Commutative

    # Comparison
    def __eq__(self, other):
        if isinstance(other, MyNumber):
            return self.value == other.value
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, MyNumber):
            return self.value < other.value
        return NotImplemented

    # Augmented assignment (for mutable types)
    def __iadd__(self, other):
        if isinstance(other, MyNumber):
            self.value += other.value
        else:
            self.value += other
        return self  # Must return self!
```

---

## Summary

1. **Unary operators** (`-`, `+`, `~`, `abs`): Return new objects
2. **Infix operators**: Implement forward (`__add__`) and reverse (`__radd__`)
3. **Return `NotImplemented`**: To let Python try the reverse method
4. **Rich comparison**: Same method handles forward and reverse (with swapped args)
5. **Augmented assignment**: Modify `self` in place and return `self`
6. **`@` operator**: Matrix multiplication, added in Python 3.5
