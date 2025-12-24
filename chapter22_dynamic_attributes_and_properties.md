# Dynamic Attributes and Properties - Practical Memo

## Overview

Dynamic attributes provide a uniform interface for accessing data, whether stored or computed on demand. This follows the **Uniform Access Principle**: services should be available through uniform notation regardless of implementation.

> "The crucial importance of properties is that their existence makes it perfectly safe and indeed advisable for you to expose public data attributes as part of your class's public interface."
> — Martelli, Ravenscroft, and Holden

---

## Key Mechanisms

| Mechanism | Purpose | When Called |
|-----------|---------|-------------|
| `@property` | Compute attributes on access | Always on read |
| `__getattr__` | Handle missing attributes | Only when attribute not found |
| `__getattribute__` | Intercept all attribute access | Always (use carefully) |
| `__setattr__` | Intercept all attribute setting | Always |
| `__new__` | Flexible object construction | Before `__init__` |

---

## The @property Decorator

Transform a method into a read-only attribute:

```python
class Circle:
    def __init__(self, radius):
        self._radius = radius

    @property
    def radius(self):
        """The radius of the circle."""
        return self._radius

    @property
    def area(self):
        """Computed on each access."""
        return 3.14159 * self._radius ** 2
```

### Read/Write Properties

```python
class LineItem:
    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight  # Uses the setter
        self.price = price

    @property
    def weight(self):
        return self.__weight

    @weight.setter
    def weight(self, value):
        if value > 0:
            self.__weight = value
        else:
            raise ValueError('weight must be > 0')

    def subtotal(self):
        return self.weight * self.price
```

### Property with Deleter

```python
class Resource:
    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @name.deleter
    def name(self):
        print(f"Deleting {self._name}")
        del self._name

# Usage
r = Resource("test")
del r.name  # Triggers deleter
```

### Classic Property Syntax

```python
class LineItem:
    def get_weight(self):
        return self.__weight

    def set_weight(self, value):
        if value > 0:
            self.__weight = value
        else:
            raise ValueError('weight must be > 0')

    weight = property(get_weight, set_weight, doc='weight in kilograms')
```

---

## Properties Override Instance Attributes

**Critical concept**: Properties are class attributes that shadow instance attributes of the same name.

```python
class Example:
    @property
    def data(self):
        return "from property"

obj = Example()
obj.__dict__['data'] = 'instance value'  # Store directly
print(obj.data)  # Still prints "from property" - property wins!
```

The lookup order for `obj.attr`:
1. Check `obj.__class__` for a property/descriptor named `attr`
2. If property found, call its getter
3. Otherwise, look in `obj.__dict__`
4. If not found, call `__getattr__` (if defined)

---

## Dynamic Attributes with __getattr__

`__getattr__` is called **only when the attribute is not found** through normal means:

```python
class FrozenJSON:
    """Navigate JSON data with attribute access."""

    def __init__(self, mapping):
        self._data = dict(mapping)

    def __getattr__(self, name):
        try:
            return getattr(self._data, name)  # dict methods
        except AttributeError:
            return FrozenJSON.build(self._data[name])

    def __dir__(self):
        return self._data.keys()

    @classmethod
    def build(cls, obj):
        if isinstance(obj, dict):
            return cls(obj)
        elif isinstance(obj, list):
            return [cls.build(item) for item in obj]
        else:
            return obj
```

**Usage:**
```python
data = {'name': 'Alice', 'address': {'city': 'Paris'}}
frozen = FrozenJSON(data)
print(frozen.name)          # 'Alice'
print(frozen.address.city)  # 'Paris' - recursive!
```

---

## The __new__ Constructor

`__new__` creates and returns the instance; `__init__` initializes it:

```python
class FrozenJSON:
    def __new__(cls, arg):
        if isinstance(arg, dict):
            return super().__new__(cls)  # Create instance
        elif isinstance(arg, list):
            return [cls(item) for item in arg]
        else:
            return arg  # Return as-is (not a FrozenJSON)

    def __init__(self, mapping):
        self._data = dict(mapping)

    def __getattr__(self, name):
        return FrozenJSON(self._data[name])
```

**Key points:**
- `__new__` is a class method (implicitly)
- Can return an instance of a different class
- If `__new__` returns non-instance, `__init__` is not called

---

## Handling Invalid Attribute Names

Python keywords and invalid identifiers need special handling:

```python
import keyword

class SafeJSON:
    def __init__(self, mapping):
        self._data = {}
        for key, value in mapping.items():
            if keyword.iskeyword(key):
                key += '_'  # 'class' -> 'class_'
            if not key.isidentifier():
                key = f'_{key}'  # '2name' -> '_2name'
            self._data[key] = value
```

```python
data = {'class': 2024, 'name': 'Test'}
safe = SafeJSON(data)
safe.class_  # Access with trailing underscore
```

---

## The "Bunch" Pattern

Quickly create objects with arbitrary attributes:

```python
class Record:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __repr__(self):
        return f'<Record {self.__dict__}>'

# Usage
person = Record(name='Alice', age=30, city='Paris')
print(person.name)  # 'Alice'
print(person.age)   # 30
```

**Standard library alternatives:**
- `types.SimpleNamespace`
- `argparse.Namespace`

---

## Caching Properties

### functools.cached_property (Python 3.8+)

```python
from functools import cached_property

class DataSet:
    def __init__(self, data):
        self._data = data

    @cached_property
    def summary(self):
        """Expensive computation, cached after first access."""
        print("Computing summary...")
        return sum(self._data) / len(self._data)
```

**Caveats:**
- Not a true property (doesn't override instance attributes)
- Cannot be used if method depends on same-named instance attribute
- Cannot be used with `__slots__`
- Defeats key-sharing optimization (creates attribute after `__init__`)

### Stacking @property and @cache

```python
from functools import cache

class Event:
    @property
    @cache  # cache goes below property
    def speakers(self):
        """Cached but still respects property semantics."""
        return self._fetch_speakers()
```

### Manual Caching (Key-Sharing Safe)

```python
class Event:
    def __init__(self, **kwargs):
        self._speaker_objs = None  # Initialize in __init__
        self.__dict__.update(kwargs)

    @property
    def speakers(self):
        if self._speaker_objs is None:
            self._speaker_objs = self._fetch_speakers()
        return self._speaker_objs
```

---

## Property Factory

Avoid repetitive property definitions with a factory function:

```python
def quantity(storage_name):
    """Property factory for validated positive quantities."""

    def qty_getter(instance):
        return instance.__dict__[storage_name]

    def qty_setter(instance, value):
        if value > 0:
            instance.__dict__[storage_name] = value
        else:
            raise ValueError('value must be > 0')

    return property(qty_getter, qty_setter)


class LineItem:
    weight = quantity('weight')
    price = quantity('price')

    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight
        self.price = price

    def subtotal(self):
        return self.weight * self.price
```

**Note:** Accessing `instance.__dict__` directly bypasses the property, avoiding infinite recursion.

---

## Special Attributes

| Attribute | Description |
|-----------|-------------|
| `__class__` | Reference to object's class (`type(obj)`) |
| `__dict__` | Mapping of writable attributes |
| `__slots__` | Tuple of allowed attribute names (memory optimization) |

---

## Built-in Functions for Attributes

| Function | Purpose |
|----------|---------|
| `getattr(obj, name[, default])` | Get attribute, optionally with default |
| `setattr(obj, name, value)` | Set attribute |
| `hasattr(obj, name)` | Check if attribute exists |
| `delattr(obj, name)` | Delete attribute |
| `dir(obj)` | List attributes (interactive use) |
| `vars(obj)` | Return `obj.__dict__` |

---

## Special Methods for Attribute Handling

```python
class Traced:
    def __getattribute__(self, name):
        """Called for EVERY attribute access."""
        print(f"Getting {name}")
        return super().__getattribute__(name)

    def __getattr__(self, name):
        """Called only when attribute NOT found."""
        print(f"Missing {name}")
        raise AttributeError(name)

    def __setattr__(self, name, value):
        """Called for EVERY attribute assignment."""
        print(f"Setting {name} = {value}")
        super().__setattr__(name, value)

    def __delattr__(self, name):
        """Called when deleting an attribute."""
        print(f"Deleting {name}")
        super().__delattr__(name)
```

**Warning:** `__getattribute__` and `__setattr__` are called unconditionally. Use `super()` to avoid infinite recursion.

---

## Common Patterns

### Pattern 1: Computed Virtual Attributes

```python
class Vector:
    __match_args__ = ('x', 'y', 'z')

    def __init__(self, x, y, z):
        self._components = [x, y, z]

    def __getattr__(self, name):
        cls = type(self)
        if name in cls.__match_args__:
            index = cls.__match_args__.index(name)
            return self._components[index]
        raise AttributeError(f'{cls.__name__!r} has no {name!r}')
```

### Pattern 2: Attribute Access Logging

```python
class LoggedAccess:
    def __getattribute__(self, name):
        value = super().__getattribute__(name)
        print(f"Accessed {name}: {value!r}")
        return value

    def __setattr__(self, name, value):
        print(f"Set {name} = {value!r}")
        super().__setattr__(name, value)
```

### Pattern 3: Read-Only After Init

```python
class Frozen:
    _frozen = False

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        self._frozen = True

    def __setattr__(self, name, value):
        if self._frozen and name != '_frozen':
            raise AttributeError("Cannot modify frozen object")
        super().__setattr__(name, value)
```

---

## Best Practices

### 1. Prefer Properties Over __getattr__

```python
# GOOD - explicit, easy to understand
@property
def area(self):
    return self.width * self.height

# Use __getattr__ only for truly dynamic cases
```

### 2. Always Use super() in Attribute Methods

```python
def __setattr__(self, name, value):
    # GOOD - delegates properly
    super().__setattr__(name, value)

def __setattr__(self, name, value):
    # BAD - may cause issues
    self.__dict__[name] = value
```

### 3. Document Computed Properties

```python
@property
def total(self):
    """Total cost including tax (computed, not cached)."""
    return self.subtotal * (1 + self.tax_rate)
```

### 4. Cache Expensive Computations

```python
from functools import cached_property

@cached_property  # For properties that don't change
def expensive_result(self):
    return self._complex_calculation()
```

---

## Quick Reference

```python
# Property decorator
@property
def attr(self): return self._attr

@attr.setter
def attr(self, value): self._attr = value

@attr.deleter
def attr(self): del self._attr

# Classic property
attr = property(getter, setter, deleter, "docstring")

# Cached property (3.8+)
from functools import cached_property
@cached_property
def attr(self): return expensive_computation()

# Dynamic attributes
def __getattr__(self, name):  # Only for missing attrs
def __getattribute__(self, name):  # For ALL access
def __setattr__(self, name, value):  # For ALL assignment

# Built-ins
getattr(obj, 'attr', default)
setattr(obj, 'attr', value)
hasattr(obj, 'attr')
delattr(obj, 'attr')
vars(obj)  # Returns __dict__
dir(obj)   # Lists attributes
```

---

## Summary

1. **Properties** turn method calls into attribute access syntax
2. **@property** creates read-only attributes; add `@attr.setter` for read/write
3. **Properties override instance attributes** - the property always wins
4. **__getattr__** handles missing attributes only (not found by normal lookup)
5. **__getattribute__** intercepts ALL attribute access (use carefully)
6. **__new__** can return different types based on arguments
7. **Property factories** reduce code duplication for similar validations
8. **@cached_property** caches computed values after first access
9. Access `__dict__` directly to bypass properties when needed
10. Use `super()` in attribute special methods to avoid recursion
