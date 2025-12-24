# Inheritance: For Better or for Worse - Practical Memo

## The Dangers of Inheritance

> "We needed a better theory about inheritance entirely (and still do)."
> — Alan Kay, creator of Smalltalk

Inheritance creates **tight coupling** between classes. Changes to a superclass can have unexpected effects on subclasses. Use inheritance carefully.

---

## The `super()` Function

### Basic Usage

```python
class Parent:
    def __init__(self, name):
        self.name = name

    def greet(self):
        return f"Hello, I'm {self.name}"

class Child(Parent):
    def __init__(self, name, age):
        super().__init__(name)  # Call parent's __init__
        self.age = age

    def greet(self):
        parent_greeting = super().greet()  # Call parent's method
        return f"{parent_greeting}, and I'm {self.age} years old"
```

### Why Use `super()` Instead of Direct Call?

```python
# DON'T do this:
class Child(Parent):
    def __init__(self, name, age):
        Parent.__init__(self, name)  # Hardcoded parent class name!

# DO this:
class Child(Parent):
    def __init__(self, name, age):
        super().__init__(name)  # Flexible, works with multiple inheritance
```

**Reasons to use `super()`:**
1. If you change the base class, the code still works
2. Works correctly with multiple inheritance (follows MRO)
3. It's the Pythonic way

### Python 2 vs Python 3

```python
# Python 2 (old way, still works in Python 3):
super(ChildClass, self).__init__(name)

# Python 3 (preferred):
super().__init__(name)
```

---

## Subclassing Built-In Types Is Tricky

### The Problem

Built-in types (written in C) don't call overridden methods in subclasses:

```python
class DoppelDict(dict):
    def __setitem__(self, key, value):
        super().__setitem__(key, [value] * 2)  # Double the value

dd = DoppelDict(one=1)  # __init__ ignores our __setitem__!
print(dd)  # {'one': 1} - NOT doubled!

dd['two'] = 2  # Direct call works
print(dd)  # {'one': 1, 'two': [2, 2]}

dd.update(three=3)  # update also ignores our __setitem__!
print(dd)  # {'one': 1, 'two': [2, 2], 'three': 3}
```

### The Solution: Use UserDict, UserList, UserString

```python
from collections import UserDict

class DoppelDict(UserDict):
    def __setitem__(self, key, value):
        super().__setitem__(key, [value] * 2)

dd = DoppelDict(one=1)
print(dd)  # {'one': [1, 1]} - Works correctly!

dd.update(two=2)
print(dd)  # {'one': [1, 1], 'two': [2, 2]} - Also works!
```

| Built-in Type | Use Instead |
|---------------|-------------|
| `dict` | `collections.UserDict` |
| `list` | `collections.UserList` |
| `str` | `collections.UserString` |

---

## Multiple Inheritance and MRO

### The Diamond Problem

```
      Root
      /  \
     A    B
      \  /
      Leaf
```

```python
class Root:
    def ping(self):
        print(f"ping in Root")

class A(Root):
    def ping(self):
        print(f"ping in A")
        super().ping()

class B(Root):
    def ping(self):
        print(f"ping in B")
        super().ping()

class Leaf(A, B):
    def ping(self):
        print(f"ping in Leaf")
        super().ping()

leaf = Leaf()
leaf.ping()
# Output:
# ping in Leaf
# ping in A
# ping in B
# ping in Root
```

### Method Resolution Order (MRO)

The MRO determines the order in which base classes are searched:

```python
print(Leaf.__mro__)
# (<class 'Leaf'>, <class 'A'>, <class 'B'>, <class 'Root'>, <class 'object'>)
```

**Key points:**
- `super()` follows the MRO, not just the immediate parent
- The MRO is computed using the C3 linearization algorithm
- Order of base classes in declaration matters: `class Leaf(A, B)` vs `class Leaf(B, A)`

### Cooperative Methods

A **cooperative method** calls `super()` to let other classes in the MRO do their part:

```python
class A:
    def method(self):
        print("A.method")
        super().method()  # Cooperative!

class B:
    def method(self):
        print("B.method")
        # Does NOT call super() - chain stops here!
```

**Best Practice:** Every non-root class should call `super()` to be cooperative.

---

## Mixin Classes

A **mixin** is a class designed to add functionality to other classes through multiple inheritance. It's not meant to be instantiated on its own.

### Example: UpperCaseMixin

```python
class UpperCaseMixin:
    """Mixin that uppercases all string keys in a mapping."""

    def __setitem__(self, key, item):
        if isinstance(key, str):
            key = key.upper()
        super().__setitem__(key, item)

    def __getitem__(self, key):
        if isinstance(key, str):
            key = key.upper()
        return super().__getitem__(key)

# Use mixin FIRST in base class list
class UpperDict(UpperCaseMixin, dict):
    pass

d = UpperDict()
d['hello'] = 'world'
print(d)  # {'HELLO': 'world'}
print(d['Hello'])  # 'world'
```

### Mixin Rules

1. **Mixins should appear first** in the base class list
2. **Mixins should call `super()`** for every method they override
3. **Mixins don't provide `__init__`** (usually)
4. **Mixins are named with `Mixin` suffix** (convention)

### Real-World Mixin: ThreadingMixIn

```python
from socketserver import ThreadingMixIn
from http.server import HTTPServer

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    pass

# Now each request is handled in a separate thread
```

---

## ABCs Are Mixins Too

Abstract Base Classes often provide **mixin methods** - concrete implementations that subclasses can use:

```python
from collections.abc import MutableMapping

class MyDict(MutableMapping):
    def __init__(self):
        self._data = {}

    # Must implement these abstract methods:
    def __getitem__(self, key): return self._data[key]
    def __setitem__(self, key, value): self._data[key] = value
    def __delitem__(self, key): del self._data[key]
    def __iter__(self): return iter(self._data)
    def __len__(self): return len(self._data)

    # Get these mixin methods for FREE:
    # keys(), values(), items(), get(), pop(), update(), setdefault(), etc.
```

---

## Best Practices for Inheritance

### DO:

1. **Prefer composition over inheritance**
   ```python
   # Instead of:
   class MyList(list):
       pass

   # Consider:
   class MyContainer:
       def __init__(self):
           self._items = []  # Composition
   ```

2. **Use ABCs for interfaces**
   ```python
   from abc import ABC, abstractmethod

   class Animal(ABC):
       @abstractmethod
       def speak(self): pass
   ```

3. **Keep inheritance hierarchies shallow** (2-3 levels max)

4. **Use mixins for cross-cutting concerns**

5. **Always use `super()` in overriding methods**

### DON'T:

1. **Don't subclass built-in types directly** (use User* classes)

2. **Don't create deep inheritance hierarchies**

3. **Don't use inheritance just to reuse code** (use composition)

4. **Don't forget to call `super().__init__()`**

5. **Don't mix unrelated functionality in a single class**

---

## Composition vs Inheritance

### When to Use Inheritance

- "Is-a" relationship: A `Dog` IS an `Animal`
- You need polymorphism
- The base class is designed for inheritance (ABC, mixin)

### When to Use Composition

- "Has-a" relationship: A `Car` HAS an `Engine`
- You want to reuse behavior without the coupling
- You need flexibility to change implementations

```python
# Inheritance (tight coupling)
class Dog(Animal):
    pass

# Composition (loose coupling)
class Car:
    def __init__(self, engine: Engine):
        self._engine = engine  # Can swap engines!

    def start(self):
        self._engine.start()
```

---

## Quick Reference

```python
# Call parent method
super().method_name()

# Check MRO
MyClass.__mro__

# Mixin pattern
class MyMixin:
    def method(self):
        # Do something
        super().method()  # Always call super!

class MyClass(MyMixin, BaseClass):
    pass

# Avoid subclassing built-ins
from collections import UserDict, UserList, UserString

class MyDict(UserDict):  # NOT dict!
    pass
```

---

## Summary

1. **Use `super()`** - It follows MRO and works with multiple inheritance

2. **Don't subclass built-in types** - Use UserDict, UserList, UserString

3. **Understand MRO** - The order matters in multiple inheritance

4. **Use mixins carefully** - They should be cooperative and appear first

5. **Prefer composition** - Inheritance creates tight coupling

6. **Keep hierarchies shallow** - Deep inheritance is hard to maintain

7. **Every overriding method should call `super()`** - Be cooperative!
