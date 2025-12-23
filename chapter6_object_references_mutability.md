# Chapter 6: Object References, Mutability, and Recycling

## Quick Reference: Comparison Table

| Concept | Use Case | Pitfall | Solution |
|---------|----------|---------|----------|
| `=` assignment | Create alias to same object | Both names modify same object | Use `copy()` or `deepcopy()` if independence needed |
| `==` equality | Compare values | Doesn't check identity | Use `is` for identity checks |
| `is` identity | Check if same object (singletons, `None`) | Confusing with `==` | Only use for `None`, `True`, `False` |
| Shallow copy | Copy container, keep refs to items | Nested mutables still shared | Use `deepcopy()` for nested structures |
| Deep copy | Fully independent copy | Slower, may fail on some objects | Only when truly needed |
| Mutable default `[]` | **NEVER** | Shared across all calls | Use `None` + create inside function |
| Immutable default | Safe for defaults | N/A | Preferred approach |

---

## 1. Variables Are Labels, Not Boxes

```python
# Variables are references (labels), not containers
a = [1, 2, 3]
b = a          # b is an ALIAS, not a copy
b.append(4)
print(a)       # [1, 2, 3, 4] - a is also modified!

# To verify: same object
print(a is b)  # True
print(id(a) == id(b))  # True
```

---

## 2. Identity vs Equality

```python
# == checks VALUE equality
# is checks IDENTITY (same object in memory)

a = [1, 2, 3]
b = [1, 2, 3]
c = a

print(a == b)  # True  - same values
print(a is b)  # False - different objects
print(a is c)  # True  - same object

# RULE: Use `is` only for singletons
x = None
if x is None:      # Correct
    pass
if x == None:      # Works but not Pythonic
    pass
```

---

## 3. Shallow vs Deep Copy

```python
from copy import copy, deepcopy

# SHALLOW COPY: new container, same inner objects
original = [[1, 2], [3, 4]]
shallow = copy(original)        # or list(original) or original[:]

shallow.append([5, 6])          # Only affects shallow
print(original)                 # [[1, 2], [3, 4]]

shallow[0][0] = 'X'             # Affects BOTH!
print(original)                 # [['X', 2], [3, 4]]

# DEEP COPY: fully independent
original = [[1, 2], [3, 4]]
deep = deepcopy(original)

deep[0][0] = 'X'
print(original)                 # [[1, 2], [3, 4]] - unchanged
```

### Copy Methods Summary

```python
# Ways to make SHALLOW copies
list_copy = list(original)      # constructor
list_copy = original[:]         # slice
list_copy = original.copy()     # method
list_copy = copy(original)      # copy module

dict_copy = dict(original)
dict_copy = original.copy()
dict_copy = {**original}        # unpacking

set_copy = set(original)
set_copy = original.copy()
```

---

## 4. Mutable Types as Parameter Defaults: BAD IDEA

### The Problem

```python
# WRONG - Classic bug!
def add_item(item, items=[]):
    items.append(item)
    return items

# First call works as expected
print(add_item('a'))  # ['a']

# BUT the default list is SHARED across all calls!
print(add_item('b'))  # ['a', 'b']  <- UNEXPECTED!
print(add_item('c'))  # ['a', 'b', 'c']  <- BUG!

# The default [] is created ONCE at function definition
# and reused for every call that doesn't provide items
```

### Why This Happens

```python
def add_item(item, items=[]):
    items.append(item)
    return items

# Proof: the default is stored in the function object
print(add_item.__defaults__)  # ([],)

add_item('x')
print(add_item.__defaults__)  # (['x'],)  <- it mutated!

add_item('y')
print(add_item.__defaults__)  # (['x', 'y'],)  <- keeps growing!
```

### The Solution: Use None as Default

```python
# CORRECT - Use None sentinel pattern
def add_item(item, items=None):
    if items is None:
        items = []      # Fresh list created at EACH call
    items.append(item)
    return items

print(add_item('a'))  # ['a']
print(add_item('b'))  # ['b']  <- Correct!
print(add_item('c'))  # ['c']  <- Correct!

# With existing list
my_list = [1, 2]
print(add_item(3, my_list))  # [1, 2, 3]
```

### Real-World Examples

```python
# WRONG - Bug in class
class Bus:
    def __init__(self, passengers=[]):
        self.passengers = passengers

bus1 = Bus()
bus1.passengers.append('Alice')
bus2 = Bus()
print(bus2.passengers)  # ['Alice'] <- Ghost passenger!

# CORRECT
class Bus:
    def __init__(self, passengers=None):
        self.passengers = passengers if passengers is not None else []
        # Or more concise:
        # self.passengers = list(passengers) if passengers else []
```

---

## 5. Defensive Programming with Mutable Parameters

### The Problem: Aliasing External Objects

```python
# DANGEROUS - Storing reference to external mutable
class Bus:
    def __init__(self, passengers=None):
        if passengers is None:
            self.passengers = []
        else:
            self.passengers = passengers  # ALIAS to external list!

team = ['Alice', 'Bob']
bus = Bus(team)
bus.passengers.append('Charlie')
print(team)  # ['Alice', 'Bob', 'Charlie'] <- External list modified!
```

### Solution: Defensive Copy

```python
# SAFE - Make a copy of incoming mutable
class Bus:
    def __init__(self, passengers=None):
        if passengers is None:
            self.passengers = []
        else:
            self.passengers = list(passengers)  # COPY!

team = ['Alice', 'Bob']
bus = Bus(team)
bus.passengers.append('Charlie')
print(team)  # ['Alice', 'Bob'] <- Protected!
print(bus.passengers)  # ['Alice', 'Bob', 'Charlie']
```

### When to Copy vs When to Alias

```python
# ALIAS (no copy) when:
# - Performance critical and you trust the caller
# - API contract says "I will modify this"
# - Building a view/wrapper intentionally

# COPY when:
# - Storing data that should be independent
# - Untrusted/external input
# - Default for most cases (safer)

# PRACTICAL PATTERN for methods
class ShoppingCart:
    def __init__(self):
        self._items = []

    def add_items(self, items):
        # Extend with copies of values, don't store reference
        self._items.extend(items)  # Safe: extend copies elements

    @property
    def items(self):
        # Return copy to prevent external modification
        return list(self._items)  # Defensive copy on read
```

---

## 6. del and Garbage Collection

```python
# del removes the REFERENCE, not the object
a = [1, 2, 3]
b = a
del a           # Only removes 'a' label
print(b)        # [1, 2, 3] - object still exists!

# Object deleted when NO references remain
import weakref

class Foo:
    pass

obj = Foo()
weak = weakref.ref(obj)
print(weak())   # <Foo object>

del obj
print(weak())   # None - object was garbage collected
```

---

## 7. Practical Patterns Summary

```python
# Pattern 1: Safe function with optional list parameter
def process_items(items=None):
    items = items if items is not None else []
    # ... work with items
    return items

# Pattern 2: Safe class with mutable attribute
class Container:
    def __init__(self, data=None):
        self._data = list(data) if data else []

    @property
    def data(self):
        return list(self._data)  # Return copy

# Pattern 3: Explicit copy for independence
from copy import deepcopy

def transform_deeply_nested(data):
    result = deepcopy(data)  # Safe to modify
    # ... modify result
    return result

# Pattern 4: Using immutable defaults (always safe)
def greet(name, greeting="Hello"):  # str is immutable - safe!
    return f"{greeting}, {name}!"
```

---

## Quick Rules

1. **Never use `[]`, `{}`, or `set()` as default parameter values**
2. **Use `None` as default, create mutable inside function**
3. **Copy incoming mutables if storing them** (`list()`, `dict()`, etc.)
4. **Return copies of internal mutables to prevent external modification**
5. **Use `is` only for `None`, `True`, `False` comparisons**
6. **Use `==` for value comparison**
7. **Use `deepcopy()` only when nested structures need full independence**
