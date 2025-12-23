# Interfaces, Protocols, and ABCs - Practical Memo

## The Typing Map: Four Approaches

Python offers four ways to define and check types:

| Approach | Checked At | Based On | Explicit Definition? |
|----------|------------|----------|---------------------|
| **Duck Typing** | Runtime | Object behavior | No (implicit) |
| **Goose Typing** | Runtime | ABCs | Yes (abc.ABC) |
| **Static Typing** | Static analysis | Type hints | Yes (classes, types) |
| **Static Duck Typing** | Static analysis | Protocols | Yes (typing.Protocol) |

---

## Two Kinds of Protocols

### Dynamic Protocol (Traditional Duck Typing)

- Informal, defined by convention and documentation
- Object may implement only part of a protocol
- Cannot be verified by static type checkers

```python
# Partial sequence protocol - only __getitem__
class Vowels:
    def __getitem__(self, i):
        return 'AEIOU'[i]

v = Vowels()
v[0]        # 'A' - indexing works
for c in v: # iteration works (Python tries __getitem__ with 0, 1, 2...)
    print(c)
'E' in v    # True - containment works too!
```

### Static Protocol (typing.Protocol)

- Explicit definition as `typing.Protocol` subclass
- Must implement ALL methods declared in the protocol
- Verified by static type checkers (mypy, pyright, etc.)

```python
from typing import Protocol

class SupportsRead(Protocol):
    def read(self, n: int = -1) -> bytes: ...

def read_all(reader: SupportsRead) -> bytes:
    return reader.read()

# Any class with a compatible read() method works
# No inheritance required!
```

---

## Duck Typing in Practice

### Python Digs Sequences

Implementing `__getitem__` alone gives you:
- Indexing (`obj[0]`)
- Iteration (`for x in obj`)
- Containment (`x in obj`)
- Slicing (`obj[1:3]`)

```python
class Deck:
    def __init__(self):
        self._cards = ['A', 'B', 'C', 'D']

    def __getitem__(self, position):
        return self._cards[position]

    def __len__(self):
        return len(self._cards)

deck = Deck()
len(deck)           # 4
deck[0]             # 'A'
for card in deck:   # Works!
    print(card)
'B' in deck         # True
```

### Monkey Patching

Adding methods at runtime to fix missing protocol support:

```python
from random import shuffle

class FrenchDeck:
    def __init__(self):
        self._cards = list(range(52))

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, position):
        return self._cards[position]

deck = FrenchDeck()
# shuffle(deck)  # TypeError: does not support item assignment

# Fix by adding __setitem__ at runtime
def set_card(deck, position, card):
    deck._cards[position] = card

FrenchDeck.__setitem__ = set_card
shuffle(deck)  # Now it works!
```

---

## Defensive Programming: "Fail Fast"

### Convert Early, Fail Early

```python
def __init__(self, iterable):
    # Convert immediately - fails fast if not iterable
    self._items = list(iterable)

# Better than storing the reference and failing later
```

### Duck Type Checking Without isinstance

```python
# Handle string or iterable of strings
def process_names(field_names):
    try:
        # Assume it's a string (EAFP)
        field_names = field_names.replace(',', ' ').split()
    except AttributeError:
        # Not a string, assume it's already an iterable
        pass
    field_names = tuple(field_names)  # Make a copy, ensure iterable
    return field_names

process_names("a, b, c")       # ('a', 'b', 'c')
process_names(['a', 'b', 'c']) # ('a', 'b', 'c')
```

---

## Goose Typing: ABCs

### What is Goose Typing?

> "isinstance(obj, cls) is now just fine...as long as cls is an abstract base class"
> — Alex Martelli

Use ABCs for runtime type checking instead of concrete classes:

```python
from collections.abc import Sequence, MutableSequence, Mapping

def process(data):
    if isinstance(data, MutableSequence):
        # Can modify in place
        data.append('new')
    elif isinstance(data, Sequence):
        # Read-only sequence
        return list(data) + ['new']
    elif isinstance(data, Mapping):
        # It's a dict-like thing
        return dict(data)
```

### Key ABCs in collections.abc

| ABC | Key Methods | Description |
|-----|-------------|-------------|
| `Iterable` | `__iter__` | Can be iterated |
| `Iterator` | `__iter__`, `__next__` | Iterator object |
| `Sized` | `__len__` | Has length |
| `Container` | `__contains__` | Supports `in` |
| `Sequence` | `__getitem__`, `__len__` | Read-only sequence |
| `MutableSequence` | + `__setitem__`, `__delitem__`, `insert` | Modifiable sequence |
| `Mapping` | `__getitem__`, `__iter__`, `__len__` | Read-only dict-like |
| `MutableMapping` | + `__setitem__`, `__delitem__` | Modifiable dict-like |
| `Set` | `__contains__`, `__iter__`, `__len__` | Read-only set |
| `Callable` | `__call__` | Can be called |
| `Hashable` | `__hash__` | Can be hashed |

---

## Creating Your Own ABCs

### Basic ABC

```python
from abc import ABC, abstractmethod

class Tombola(ABC):
    """An ABC for a random item picker."""

    @abstractmethod
    def load(self, iterable):
        """Add items from an iterable."""

    @abstractmethod
    def pick(self):
        """Remove and return a random item."""

    def loaded(self):
        """Return True if there's at least one item."""
        return bool(self.inspect())

    def inspect(self):
        """Return a sorted tuple of current items."""
        items = []
        while True:
            try:
                items.append(self.pick())
            except LookupError:
                break
        self.load(items)
        return tuple(sorted(items))
```

### Implementing an ABC

```python
class BingoCage(Tombola):
    def __init__(self, items):
        self._items = list(items)

    def load(self, iterable):
        self._items.extend(iterable)

    def pick(self):
        if not self._items:
            raise LookupError('pick from empty cage')
        return self._items.pop()

# Must implement all abstract methods!
```

---

## Virtual Subclasses

### Using register()

Make a class a "virtual subclass" without inheritance:

```python
from collections.abc import Sequence

@Sequence.register
class MyClass:
    def __getitem__(self, index):
        ...
    def __len__(self):
        ...

isinstance(MyClass(), Sequence)  # True
issubclass(MyClass, Sequence)    # True
# But MyClass doesn't inherit any Sequence methods!
```

### Automatic Recognition with __subclasshook__

Some ABCs automatically recognize classes that implement certain methods:

```python
from collections.abc import Sized

class MyClass:
    def __len__(self):
        return 42

isinstance(MyClass(), Sized)  # True - no registration needed!
```

This works because `Sized` implements `__subclasshook__`:

```python
class Sized(ABC):
    @classmethod
    def __subclasshook__(cls, C):
        if cls is Sized:
            if any("__len__" in B.__dict__ for B in C.__mro__):
                return True
        return NotImplemented
```

---

## Static Protocols (typing.Protocol)

### Defining a Protocol

```python
from typing import Protocol, runtime_checkable

class SupportsClose(Protocol):
    def close(self) -> None: ...

def finish(obj: SupportsClose) -> None:
    obj.close()

# Any class with close() method works - no inheritance needed
class Connection:
    def close(self) -> None:
        print("Closing connection")

finish(Connection())  # Works!
```

### runtime_checkable

Enable isinstance() checks:

```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class SupportsRead(Protocol):
    def read(self, n: int = -1) -> bytes: ...

class MyReader:
    def read(self, n: int = -1) -> bytes:
        return b'data'

isinstance(MyReader(), SupportsRead)  # True
```

**Limitations of runtime_checkable:**
- Only checks method names exist
- Doesn't verify signatures or return types
- Can't check non-method attributes reliably

### Protocol with Attributes

```python
from typing import Protocol

class Named(Protocol):
    name: str  # Attribute requirement

class Person:
    def __init__(self, name: str):
        self.name = name

def greet(obj: Named) -> str:
    return f"Hello, {obj.name}"
```

---

## When to Use What

| Situation | Approach |
|-----------|----------|
| Simple duck typing, flexibility is key | Dynamic protocol (no checks) |
| Need runtime type checking | Goose typing with ABCs |
| Static type checking, no runtime overhead | Static protocol (`typing.Protocol`) |
| Runtime + static checking | `@runtime_checkable` Protocol |
| Defining a contract for a framework | Custom ABC |
| Checking against built-in concepts | `collections.abc` ABCs |

---

## Best Practices

### DO:
- Use ABCs from `collections.abc` for `isinstance` checks
- Create custom ABCs only for frameworks/libraries
- Prefer composition over inheritance
- Use `typing.Protocol` for static duck typing
- Fail fast with defensive programming

### DON'T:
- Check `type(obj) is SomeClass` (use `isinstance`)
- Create ABCs in application code (usually overkill)
- Forget that virtual subclasses don't inherit implementations
- Rely on `runtime_checkable` for thorough validation

---

## Quick Reference

```python
from abc import ABC, abstractmethod
from collections.abc import Sequence, Mapping, Iterable
from typing import Protocol, runtime_checkable

# Custom ABC
class MyABC(ABC):
    @abstractmethod
    def required_method(self): ...

    def concrete_method(self):
        return self.required_method()

# Static Protocol
@runtime_checkable
class MyProtocol(Protocol):
    def method(self) -> int: ...

# Virtual subclass registration
@Sequence.register
class MySequence:
    ...

# Type checking
isinstance(obj, Sequence)      # Goose typing
isinstance(obj, MyProtocol)    # Static duck typing (runtime)
```

---

## Summary

1. **Duck Typing**: Default Python approach - if it quacks, it's a duck
2. **Goose Typing**: Use ABCs for explicit interface contracts with runtime checks
3. **Static Protocols**: Use `typing.Protocol` for structural subtyping checked by type checkers
4. **Virtual Subclasses**: Register classes as subclasses without inheritance
5. **Fail Fast**: Validate inputs early to catch errors quickly
