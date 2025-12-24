# Attribute Descriptors - Practical Memo

## Overview

Descriptors are a way of reusing access logic across multiple attributes. A descriptor is a class implementing `__get__`, `__set__`, and/or `__delete__`. Properties are implemented as descriptors. Methods are also descriptors.

> "Learning about descriptors not only provides access to a larger toolset, it creates a deeper understanding of how Python works and an appreciation for the elegance of its design."
> — Raymond Hettinger

---

## The Descriptor Protocol

| Method | Signature | Called When |
|--------|-----------|-------------|
| `__get__` | `(self, instance, owner)` | Reading attribute |
| `__set__` | `(self, instance, value)` | Writing attribute |
| `__delete__` | `(self, instance)` | Deleting attribute |
| `__set_name__` | `(self, owner, name)` | Class creation (Python 3.6+) |

**Parameters:**
- `self` - The descriptor instance (class attribute)
- `instance` - The managed instance (or `None` if accessed via class)
- `owner` - The managed class
- `value` - The value being assigned

---

## Key Terminology

| Term | Meaning |
|------|---------|
| **Descriptor class** | Class implementing descriptor protocol (e.g., `Quantity`) |
| **Managed class** | Class using descriptors as class attributes (e.g., `LineItem`) |
| **Descriptor instance** | Instance of descriptor class (class attribute of managed class) |
| **Managed instance** | Instance of managed class |
| **Storage attribute** | Instance attribute holding actual data |
| **Managed attribute** | Public attribute handled by descriptor |

---

## Basic Descriptor Example

```python
class Quantity:
    """Descriptor for positive quantities."""

    def __set_name__(self, owner, name):
        self.storage_name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self  # Accessed via class
        return instance.__dict__[self.storage_name]

    def __set__(self, instance, value):
        if value > 0:
            instance.__dict__[self.storage_name] = value
        else:
            raise ValueError(f'{self.storage_name} must be > 0')


class LineItem:
    weight = Quantity()  # Descriptor instance
    price = Quantity()   # Another descriptor instance

    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight  # Triggers Quantity.__set__
        self.price = price

    def subtotal(self):
        return self.weight * self.price
```

**Usage:**
```python
item = LineItem("Widget", 10, 2.50)
item.weight  # Triggers Quantity.__get__
item.weight = 5  # Triggers Quantity.__set__

LineItem.weight  # Returns the Quantity descriptor instance
```

---

## The __set_name__ Method (Python 3.6+)

Automatically called when the class is created:

```python
class Descriptor:
    def __set_name__(self, owner, name):
        # owner = the managed class (e.g., LineItem)
        # name = attribute name in managed class (e.g., 'weight')
        self.storage_name = name
        self.public_name = name

class MyClass:
    attr = Descriptor()  # __set_name__(MyClass, 'attr') is called
```

This eliminates the need to pass the attribute name to the descriptor:

```python
# Before __set_name__ (redundant)
class LineItem:
    weight = Quantity('weight')  # Had to repeat name
    price = Quantity('price')

# With __set_name__ (clean)
class LineItem:
    weight = Quantity()  # Name automatically detected
    price = Quantity()
```

---

## Overriding vs Nonoverriding Descriptors

### Overriding Descriptors (Data Descriptors)

Have `__set__` method. **Always intercept attribute writes.**

```python
class Overriding:
    """Descriptor with __get__ and __set__."""

    def __get__(self, instance, owner):
        return f'Overriding.__get__({instance})'

    def __set__(self, instance, value):
        print(f'Overriding.__set__({instance}, {value})')

class Managed:
    over = Overriding()

obj = Managed()
obj.over = 7       # Triggers __set__
obj.over           # Triggers __get__

# Even direct __dict__ access doesn't bypass on read:
obj.__dict__['over'] = 8
obj.over           # Still triggers __get__ (descriptor wins!)
```

### Nonoverriding Descriptors (Non-data Descriptors)

Only have `__get__`. **Can be shadowed by instance attributes.**

```python
class NonOverriding:
    """Descriptor with only __get__."""

    def __get__(self, instance, owner):
        return f'NonOverriding.__get__({instance})'

class Managed:
    non_over = NonOverriding()

obj = Managed()
obj.non_over       # Triggers __get__
obj.non_over = 7   # Creates instance attribute (no __set__)
obj.non_over       # Returns 7 (instance attr shadows descriptor)

del obj.non_over   # Remove instance attribute
obj.non_over       # Triggers __get__ again
```

---

## Descriptor Type Summary

| Type | Has `__set__` | Behavior |
|------|---------------|----------|
| **Overriding** | Yes | Always intercepts reads and writes |
| **Overriding (no __get__)** | Yes (no __get__) | Intercepts writes; reads return descriptor |
| **Nonoverriding** | No | Can be shadowed by instance attributes |

---

## Methods Are Descriptors

Functions implement `__get__`, making them nonoverriding descriptors:

```python
class MyClass:
    def method(self):
        return 'method called'

obj = MyClass()

# Via class: returns function
MyClass.method  # <function MyClass.method at ...>

# Via instance: returns bound method
obj.method      # <bound method MyClass.method of ...>

# The magic happens in __get__:
MyClass.method.__get__(obj, MyClass)  # Same as obj.method
MyClass.method.__get__(None, MyClass)  # Same as MyClass.method
```

**Bound method internals:**
```python
bound = obj.method
bound.__self__  # The instance (obj)
bound.__func__  # The original function (MyClass.method)
bound()         # Calls __func__(__self__)
```

---

## Validation Descriptor Pattern

Abstract base class with template method:

```python
import abc

class Validated(abc.ABC):
    """Abstract descriptor with validation."""

    def __set_name__(self, owner, name):
        self.storage_name = name

    def __set__(self, instance, value):
        value = self.validate(self.storage_name, value)
        instance.__dict__[self.storage_name] = value

    @abc.abstractmethod
    def validate(self, name, value):
        """Return validated value or raise ValueError."""


class Quantity(Validated):
    """Positive number validator."""

    def validate(self, name, value):
        if value <= 0:
            raise ValueError(f'{name} must be > 0')
        return value


class NonBlank(Validated):
    """Non-empty string validator."""

    def validate(self, name, value):
        value = value.strip()
        if not value:
            raise ValueError(f'{name} cannot be blank')
        return value


class LineItem:
    description = NonBlank()
    weight = Quantity()
    price = Quantity()

    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight
        self.price = price
```

---

## Handling Class-level Access

Return the descriptor itself when accessed via the class:

```python
class Quantity:
    def __set_name__(self, owner, name):
        self.storage_name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self  # Accessed via class
        return instance.__dict__[self.storage_name]

    def __set__(self, instance, value):
        if value > 0:
            instance.__dict__[self.storage_name] = value
        else:
            raise ValueError(f'{self.storage_name} must be > 0')
```

```python
LineItem.weight  # Returns <Quantity object>
item.weight      # Returns the stored value
```

---

## Read-Only Descriptors

Must implement `__set__` to prevent shadowing:

```python
class ReadOnly:
    """Read-only descriptor."""

    def __set_name__(self, owner, name):
        self.storage_name = name
        self.private_name = f'_{name}'

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance, self.private_name, None)

    def __set__(self, instance, value):
        if hasattr(instance, self.private_name):
            raise AttributeError(f'{self.storage_name} is read-only')
        setattr(instance, self.private_name, value)


class Circle:
    radius = ReadOnly()

    def __init__(self, radius):
        self.radius = radius  # Sets once

c = Circle(5)
c.radius = 10  # Raises AttributeError
```

---

## Caching Descriptor (Nonoverriding)

```python
class CachedProperty:
    """Nonoverriding descriptor that caches computed values."""

    def __init__(self, func):
        self.func = func
        self.name = None

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        # Compute and cache in instance __dict__
        value = self.func(instance)
        instance.__dict__[self.name] = value  # Shadows descriptor
        return value


class DataSet:
    def __init__(self, data):
        self._data = data

    @CachedProperty
    def average(self):
        print("Computing...")
        return sum(self._data) / len(self._data)


ds = DataSet([1, 2, 3, 4, 5])
ds.average  # "Computing..." -> 3.0
ds.average  # 3.0 (cached, no "Computing...")
```

---

## Storage Strategies

### Same-name Storage (Recommended)

```python
class Quantity:
    def __set_name__(self, owner, name):
        self.storage_name = name  # Use same name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__[self.storage_name]

    def __set__(self, instance, value):
        instance.__dict__[self.storage_name] = value
```

### Private-name Storage

```python
class Quantity:
    def __set_name__(self, owner, name):
        self.storage_name = f'_{name}'  # Prefix with _

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance, self.storage_name)

    def __set__(self, instance, value):
        setattr(instance, self.storage_name, value)
```

---

## Common Pitfalls

### Pitfall 1: Storing in Descriptor (Wrong!)

```python
class BadDescriptor:
    def __set__(self, instance, value):
        self.value = value  # WRONG! Shared across all instances!

class MyClass:
    attr = BadDescriptor()

a = MyClass()
b = MyClass()
a.attr = 1
b.attr = 2
print(a.attr)  # 2! (shared state)
```

**Fix:** Always store in the managed instance:
```python
instance.__dict__[self.storage_name] = value
```

### Pitfall 2: Using setattr in __set__ (Infinite Loop)

```python
class BadDescriptor:
    def __set__(self, instance, value):
        setattr(instance, self.storage_name, value)  # Infinite recursion!
```

**Fix:** Write directly to `__dict__`:
```python
instance.__dict__[self.storage_name] = value
```

---

## Descriptor Usage Tips

1. **Use `property` for simple cases** - Properties are overriding descriptors

2. **Read-only descriptors need `__set__`** - Otherwise instance attrs shadow them

3. **Validation-only descriptors can skip `__get__`** - Just validate in `__set__`, store directly

4. **Caching works with `__get__` only** - Store result as instance attr to shadow descriptor

5. **Methods can be shadowed** - Functions are nonoverriding descriptors

6. **Class-level assignment overwrites descriptors** - `MyClass.attr = 5` replaces the descriptor

---

## Quick Reference

```python
class Descriptor:
    """Complete descriptor template."""

    def __set_name__(self, owner, name):
        """Called when class is created."""
        self.name = name

    def __get__(self, instance, owner):
        """Called when attribute is read."""
        if instance is None:
            return self  # Class-level access
        return instance.__dict__.get(self.name)

    def __set__(self, instance, value):
        """Called when attribute is written."""
        instance.__dict__[self.name] = value

    def __delete__(self, instance):
        """Called when attribute is deleted."""
        del instance.__dict__[self.name]


class ManagedClass:
    attr = Descriptor()  # Descriptor instance as class attribute

    def __init__(self, value):
        self.attr = value  # Triggers Descriptor.__set__
```

---

## Summary

1. **Descriptors** implement `__get__`, `__set__`, and/or `__delete__`
2. **Overriding descriptors** have `__set__` and always intercept access
3. **Nonoverriding descriptors** only have `__get__` and can be shadowed
4. **`__set_name__`** (Python 3.6+) auto-detects attribute name
5. **Methods are descriptors** - `__get__` returns bound methods
6. **Properties are descriptors** - Built using the descriptor protocol
7. **Store values in managed instance**, not in descriptor
8. **Use `instance.__dict__`** directly to avoid recursion
9. **Return `self`** from `__get__` when `instance is None`
10. **Descriptors enable ORM field types**, validation, caching, and more
