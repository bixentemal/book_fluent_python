# Class Metaprogramming - Practical Memo

## Overview

Class metaprogramming is the art of creating or customizing classes at runtime. Python provides several mechanisms, from simple to advanced:

1. **Class factory functions** - using `type()` to create classes
2. **`__init_subclass__`** - hook for customizing subclass creation
3. **Class decorators** - functions that transform classes
4. **Metaclasses** - classes whose instances are classes

> "For the sake of readability and maintainability, you should probably avoid the techniques described in this chapter in application code. On the other hand, these are the tools of the trade if you want to write the next great Python framework."

---

## Classes as Objects

Every class has these special attributes:

| Attribute | Description |
|-----------|-------------|
| `cls.__class__` | The class of the class (usually `type`) |
| `cls.__name__` | Class name as string |
| `cls.__qualname__` | Qualified name (includes outer class) |
| `cls.__bases__` | Tuple of base classes |
| `cls.__mro__` | Method Resolution Order tuple |
| `cls.__dict__` | Class namespace (mappingproxy) |
| `cls.__subclasses__()` | List of immediate subclasses |

---

## type: The Built-In Class Factory

`type` is both a function and a metaclass:

```python
# As a function: get type of an object
type(42)  # <class 'int'>

# As a class factory: create a new class
MyClass = type('MyClass', (BaseClass,), {'x': 42, 'method': lambda self: self.x})
```

**type() signature for class creation:**
```python
type(name, bases, dict) -> new class
```

- `name`: Class name (string)
- `bases`: Tuple of base classes
- `dict`: Namespace dictionary

**Equivalent forms:**
```python
# Using class statement
class MyClass(Base):
    x = 42

# Using type()
MyClass = type('MyClass', (Base,), {'x': 42})
```

---

## Class Factory Function

Create classes dynamically:

```python
def record_factory(cls_name: str, field_names: str) -> type:
    """Factory that creates simple record classes."""
    slots = tuple(field_names.split())

    def __init__(self, *args, **kwargs):
        for name, value in zip(self.__slots__, args):
            setattr(self, name, value)
        for name, value in kwargs.items():
            setattr(self, name, value)

    def __repr__(self):
        values = ', '.join(f'{n}={getattr(self, n)!r}'
                          for n in self.__slots__)
        return f'{self.__class__.__name__}({values})'

    def __iter__(self):
        for name in self.__slots__:
            yield getattr(self, name)

    cls_attrs = {
        '__slots__': slots,
        '__init__': __init__,
        '__repr__': __repr__,
        '__iter__': __iter__,
    }

    return type(cls_name, (object,), cls_attrs)


# Usage
Dog = record_factory('Dog', 'name weight owner')
rex = Dog('Rex', 30, 'Bob')
print(rex)  # Dog(name='Rex', weight=30, owner='Bob')
```

---

## __init_subclass__ (Python 3.6+)

Hook called when a class is subclassed:

```python
class Validated:
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        # cls is the newly created subclass
        for name, hint in cls.__annotations__.items():
            setattr(cls, name, ValidatedField(name, hint))

class Person(Validated):
    name: str
    age: int

# __init_subclass__ is called here, adding ValidatedField descriptors
```

**Key points:**
- Called after class is built by `type.__new__`
- Receives the new subclass as first argument (not `self` or `cls`)
- Always call `super().__init_subclass__(**kwargs)`
- Cannot configure `__slots__` (class already built)

### Example: Auto-registering Subclasses

```python
class Plugin:
    registry = {}

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        Plugin.registry[cls.__name__] = cls

class AudioPlugin(Plugin):
    pass

class VideoPlugin(Plugin):
    pass

print(Plugin.registry)
# {'AudioPlugin': <class 'AudioPlugin'>, 'VideoPlugin': <class 'VideoPlugin'>}
```

---

## Class Decorators

Functions that receive and return a class:

```python
def add_repr(cls):
    """Class decorator that adds a __repr__ method."""
    def __repr__(self):
        attrs = ', '.join(f'{k}={v!r}'
                         for k, v in self.__dict__.items())
        return f'{cls.__name__}({attrs})'
    cls.__repr__ = __repr__
    return cls

@add_repr
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

p = Point(1, 2)
print(p)  # Point(x=1, y=2)
```

### Decorator vs __init_subclass__

| Feature | Class Decorator | `__init_subclass__` |
|---------|-----------------|---------------------|
| Applied to | Decorated class only | All subclasses |
| Inheritance | Must decorate each class | Automatic |
| Timing | After `__init_subclass__` | Before decorator |
| Conflicts | Less likely | May conflict with metaclasses |

---

## Import Time vs Runtime

### Import Time

When a module is imported:

1. Source code is parsed (may raise `SyntaxError`)
2. Bytecode is compiled
3. Top-level code is executed

```python
# All of this runs at import time:
print("Module loading")  # Runs

class MyClass:  # Class object is created
    print("Class body")  # Runs
    x = expensive_computation()  # Runs

def my_function():  # Function object is created
    print("Function body")  # Does NOT run yet
```

### Execution Order for Classes

```python
@decorator           # 4. Decorator applied
class Klass(Base):   # 1. Base.__init_subclass__ prep
    x = Descriptor() # 2. Descriptor.__init__, __set_name__
    ...
                     # 3. Base.__init_subclass__ called
```

Order:
1. `__prepare__` (if metaclass has it)
2. Class body executed
3. Descriptors' `__set_name__` called
4. `__init_subclass__` called on parent
5. Class decorator applied

---

## Metaclasses

A metaclass is a class whose instances are classes:

```python
class MyMeta(type):
    def __new__(mcs, name, bases, namespace):
        # mcs: the metaclass
        # name: class name
        # bases: base classes tuple
        # namespace: class dict
        print(f"Creating class {name}")
        cls = super().__new__(mcs, name, bases, namespace)
        return cls

class MyClass(metaclass=MyMeta):
    pass
# Prints: Creating class MyClass
```

### Metaclass Hierarchy

```
type (metaclass) ─────creates────> MyClass (class) ─────creates────> obj (instance)
      │                                  │
      └── is instance of ◄───────────────┘
```

```python
type(obj)      # <class 'MyClass'>
type(MyClass)  # <class 'type'> (or custom metaclass)
type(type)     # <class 'type'>
```

### __prepare__ Method

Provides the namespace dict for class body:

```python
class OrderedMeta(type):
    @classmethod
    def __prepare__(mcs, name, bases, **kwargs):
        return OrderedDict()  # Custom namespace

    def __new__(mcs, name, bases, namespace):
        cls = super().__new__(mcs, name, bases, dict(namespace))
        cls._field_order = list(namespace.keys())
        return cls
```

### Complete Metaclass Example

```python
class ValidatedMeta(type):
    def __new__(mcs, name, bases, namespace):
        # Add __slots__ based on annotations
        if '__annotations__' in namespace:
            slots = []
            for attr_name, attr_type in namespace['__annotations__'].items():
                namespace[attr_name] = ValidatedField(attr_name, attr_type)
                slots.append(f'_{attr_name}')
            namespace['__slots__'] = tuple(slots)

        return super().__new__(mcs, name, bases, namespace)


class Validated(metaclass=ValidatedMeta):
    pass


class Person(Validated):
    name: str
    age: int
```

---

## When to Use What

| Need | Solution |
|------|----------|
| Simple attribute injection | `__init_subclass__` |
| Transform single class | Class decorator |
| Configure `__slots__` | Metaclass or factory function |
| Custom class namespace | Metaclass with `__prepare__` |
| Control class creation | Metaclass |

### Decision Flow

```
Do you need to configure __slots__?
  ├─ Yes → Use metaclass or factory function
  └─ No
      └─ Do subclasses need auto-enhancement?
           ├─ Yes → Use __init_subclass__
           └─ No → Use class decorator
```

---

## Metaclass Caveats

### 1. Single Metaclass Rule

A class can only have one metaclass:

```python
class Meta1(type): pass
class Meta2(type): pass

class A(metaclass=Meta1): pass
class B(metaclass=Meta2): pass

# This fails:
class C(A, B): pass  # TypeError: metaclass conflict
```

**Solution:** Create combined metaclass:
```python
class CombinedMeta(Meta1, Meta2): pass
class C(A, B, metaclass=CombinedMeta): pass
```

### 2. Complexity

Metaclasses are hard to understand and debug. Prefer simpler solutions:

```python
# Instead of metaclass, often __init_subclass__ works:
class Base:
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        # Enhancement logic here
```

### 3. ABCMeta Compatibility

```python
import abc

# If you need both ABC and custom metaclass:
class MyMeta(abc.ABCMeta):  # Inherit from ABCMeta
    pass

class MyABC(abc.ABC, metaclass=MyMeta):
    pass
```

---

## Practical Example: Auto Slots

```python
class AutoSlotsMeta(type):
    def __new__(mcs, name, bases, namespace):
        # Skip if __slots__ already defined
        if '__slots__' in namespace:
            return super().__new__(mcs, name, bases, namespace)

        # Get annotations and create slots
        annotations = namespace.get('__annotations__', {})
        namespace['__slots__'] = tuple(annotations.keys())

        return super().__new__(mcs, name, bases, namespace)


class AutoSlots(metaclass=AutoSlotsMeta):
    __slots__ = ()  # Base class, skip processing


class Point(AutoSlots):
    x: float
    y: float

    def __init__(self, x, y):
        self.x = x
        self.y = y


p = Point(1.0, 2.0)
p.z = 3.0  # AttributeError: 'Point' object has no attribute 'z'
```

---

## Quick Reference

```python
# Class factory function
def factory(name, fields):
    return type(name, (object,), {'__slots__': fields})

# __init_subclass__
class Base:
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        # customize cls

# Class decorator
def decorator(cls):
    # modify cls
    return cls

# Metaclass
class Meta(type):
    @classmethod
    def __prepare__(mcs, name, bases, **kwargs):
        return {}  # custom namespace

    def __new__(mcs, name, bases, namespace):
        return super().__new__(mcs, name, bases, namespace)

    def __init__(cls, name, bases, namespace):
        super().__init__(name, bases, namespace)

class MyClass(metaclass=Meta):
    pass

# Using type directly
MyClass = type('MyClass', (Base,), {'attr': value})
```

---

## Summary

1. **Classes are objects** created by `type` (or a custom metaclass)
2. **`type(name, bases, dict)`** creates classes programmatically
3. **`__init_subclass__`** customizes subclass creation (simplest approach)
4. **Class decorators** transform classes after creation
5. **Metaclasses** control class creation at the deepest level
6. **`__prepare__`** provides custom namespace for class body
7. **Import time** executes class bodies and decorators
8. **Prefer simpler solutions**: `__init_subclass__` > decorator > metaclass
9. **A class can only have one metaclass** - conflicts require combined metaclass
10. **Metaclasses are implementation details** - hide them behind base classes
