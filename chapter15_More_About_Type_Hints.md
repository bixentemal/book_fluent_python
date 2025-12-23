# More About Type Hints - Practical Memo

## Overview

This chapter covers advanced type hints: overloaded signatures, TypedDict, type casting, generic classes, and variance. These features enable more precise static typing for complex Python patterns.

---

## Overloaded Signatures with @overload

### The Problem

Sometimes a function returns different types based on input:

```python
def double(x):
    """Return x * 2 - but what's the return type?"""
    return x * 2

double(3)      # Returns 6 (int)
double("ab")   # Returns "abab" (str)
double([1, 2]) # Returns [1, 2, 1, 2] (list)
```

### The Solution: @overload

```python
from typing import overload

@overload
def double(x: int) -> int: ...
@overload
def double(x: str) -> str: ...
@overload
def double(x: list) -> list: ...

def double(x):
    """The actual implementation - no type hints here."""
    return x * 2
```

**Key points:**
- `@overload` decorated functions are just for the type checker
- They have no implementation (just `...`)
- The actual implementation comes last, without `@overload`
- Type checkers use the overloaded signatures to determine return types

### Practical Example: Getting Items

```python
from typing import overload, Sequence, TypeVar

T = TypeVar('T')

@overload
def get_item(seq: Sequence[T], index: int) -> T: ...
@overload
def get_item(seq: Sequence[T], index: int, default: T) -> T: ...

def get_item(seq, index, default=None):
    try:
        return seq[index]
    except IndexError:
        if default is None:
            raise
        return default
```

---

## TypedDict

### What Is TypedDict?

A way to type dictionaries with specific string keys and value types:

```python
from typing import TypedDict

class BookDict(TypedDict):
    isbn: str
    title: str
    authors: list[str]
    pagecount: int

# Now we can type a dict precisely
def get_book_info(book: BookDict) -> str:
    return f"{book['title']} by {', '.join(book['authors'])}"

# Valid usage
book: BookDict = {
    'isbn': '978-1-4919-5021-8',
    'title': 'Fluent Python',
    'authors': ['Luciano Ramalho'],
    'pagecount': 1012
}
```

### Optional Keys with total=False

```python
class BookDict(TypedDict, total=False):
    isbn: str        # Optional
    title: str       # Optional
    authors: list[str]  # Optional
```

### Mixing Required and Optional Keys

```python
from typing import TypedDict, Required, NotRequired

class BookDict(TypedDict):
    isbn: str                      # Required by default
    title: str                     # Required
    authors: list[str]             # Required
    subtitle: NotRequired[str]     # Optional

# Or with total=False as base
class BookDict(TypedDict, total=False):
    isbn: Required[str]   # Required
    title: Required[str]  # Required
    authors: list[str]    # Optional
    subtitle: str         # Optional
```

### TypedDict Limitations

- **Runtime**: No validation at runtime - it's just a dict!
- **Immutable keys**: Key names are fixed at definition
- **No extra keys**: Type checkers flag unknown keys
- **String keys only**: All keys must be strings

```python
# TypedDict does NOT validate at runtime!
book: BookDict = {'wrong_key': 42}  # Type checker catches this
# But at runtime, it's just a regular dict
```

---

## Type Casting with typing.cast

### When to Use cast()

Use `cast()` when you know more than the type checker:

```python
from typing import cast

def find_user(users: list[dict], name: str) -> dict | None:
    for user in users:
        if user.get('name') == name:
            return user
    return None

# You KNOW user exists, but type checker doesn't
user = find_user(users, 'Alice')
if user is not None:
    # Still typed as dict, not more specific
    email = user['email']

# With cast - tell the type checker you're sure
from typing import TypedDict

class UserDict(TypedDict):
    name: str
    email: str

user = cast(UserDict, find_user(users, 'Alice'))
# Now user is typed as UserDict
```

### cast() Does Nothing at Runtime

```python
from typing import cast

x = cast(str, 123)  # Type checker thinks x is str
print(x)            # Prints: 123 (still an int!)
print(type(x))      # <class 'int'>
```

**Use cast sparingly** - it bypasses type checking!

---

## Reading Type Hints at Runtime

### Using __annotations__

```python
def greet(name: str, times: int = 1) -> str:
    return (f"Hello, {name}! " * times).strip()

print(greet.__annotations__)
# {'name': <class 'str'>, 'times': <class 'int'>, 'return': <class 'str'>}
```

### Using typing.get_type_hints()

Better than `__annotations__` because it resolves forward references:

```python
from typing import get_type_hints

class Node:
    def __init__(self, value: int, next: 'Node | None' = None):
        self.value = value
        self.next = next

# __annotations__ keeps the string
print(Node.__init__.__annotations__)
# {'value': <class 'int'>, 'next': 'Node | None', 'return': <class 'NoneType'>}

# get_type_hints resolves it
print(get_type_hints(Node.__init__))
# {'value': <class 'int'>, 'next': Node | None, 'return': <class 'NoneType'>}
```

### Checking Type Origins

```python
from typing import get_origin, get_args

hint = list[str]
print(get_origin(hint))  # <class 'list'>
print(get_args(hint))    # (<class 'str'>,)

hint = dict[str, int]
print(get_origin(hint))  # <class 'dict'>
print(get_args(hint))    # (<class 'str'>, <class 'int'>)
```

---

## Generic Classes

### Basic Generic Class

```python
from typing import TypeVar, Generic

T = TypeVar('T')

class Stack(Generic[T]):
    def __init__(self) -> None:
        self._items: list[T] = []

    def push(self, item: T) -> None:
        self._items.append(item)

    def pop(self) -> T:
        return self._items.pop()

    def is_empty(self) -> bool:
        return len(self._items) == 0

# Usage
int_stack: Stack[int] = Stack()
int_stack.push(1)
int_stack.push(2)
x = int_stack.pop()  # x is typed as int

str_stack: Stack[str] = Stack()
str_stack.push("hello")
s = str_stack.pop()  # s is typed as str
```

### Multiple Type Parameters

```python
from typing import TypeVar, Generic

K = TypeVar('K')
V = TypeVar('V')

class Pair(Generic[K, V]):
    def __init__(self, key: K, value: V) -> None:
        self.key = key
        self.value = value

    def swap(self) -> 'Pair[V, K]':
        return Pair(self.value, self.key)

pair: Pair[str, int] = Pair("age", 25)
swapped = pair.swap()  # Pair[int, str]
```

### Bounded TypeVar

```python
from typing import TypeVar
from collections.abc import Hashable

H = TypeVar('H', bound=Hashable)

class HashSet(Generic[H]):
    def __init__(self) -> None:
        self._items: set[H] = set()

    def add(self, item: H) -> None:
        self._items.add(item)

# Only hashable types allowed
hs: HashSet[str] = HashSet()  # OK
# hs: HashSet[list] = HashSet()  # Error: list is not Hashable
```

---

## Variance: Covariant, Contravariant, and Invariant

### The Problem

```python
class Animal: pass
class Dog(Animal): pass
class Cat(Animal): pass

def feed_animals(animals: list[Animal]) -> None:
    for animal in animals:
        print(f"Feeding {animal}")

dogs: list[Dog] = [Dog(), Dog()]
feed_animals(dogs)  # Should this be allowed?
```

### Invariance (Default for Mutable Containers)

**Invariant**: `list[Dog]` is NOT a subtype of `list[Animal]`

```python
# Why? Because this could happen:
def add_cat(animals: list[Animal]) -> None:
    animals.append(Cat())  # Oops! Added a cat to a dog list!

dogs: list[Dog] = [Dog()]
add_cat(dogs)  # If allowed, dogs would contain a Cat!
```

**Mutable containers are invariant** for safety.

### Covariance (Read-Only Containers)

**Covariant**: If `Dog` is a subtype of `Animal`, then `Sequence[Dog]` IS a subtype of `Sequence[Animal]`

```python
from collections.abc import Sequence

def count_animals(animals: Sequence[Animal]) -> int:
    return len(animals)

dogs: list[Dog] = [Dog(), Dog()]
count_animals(dogs)  # OK! Sequence is covariant (read-only)
```

**Use `Sequence` instead of `list` for read-only parameters.**

### Contravariance (For Callables)

**Contravariant**: If `Dog` is a subtype of `Animal`, then `Callable[[Animal], None]` IS a subtype of `Callable[[Dog], None]`

```python
from collections.abc import Callable

def process_dog(handler: Callable[[Dog], None], dog: Dog) -> None:
    handler(dog)

def handle_animal(animal: Animal) -> None:
    print(f"Handling {animal}")

def handle_dog(dog: Dog) -> None:
    print(f"Handling dog {dog}")

process_dog(handle_animal, Dog())  # OK! handle_animal accepts any Animal
process_dog(handle_dog, Dog())     # OK! handle_dog accepts Dog
```

### Creating Variant TypeVars

```python
from typing import TypeVar, Generic

# Covariant (for outputs/producers)
T_co = TypeVar('T_co', covariant=True)

class Producer(Generic[T_co]):
    def get(self) -> T_co: ...

# Contravariant (for inputs/consumers)
T_contra = TypeVar('T_contra', contravariant=True)

class Consumer(Generic[T_contra]):
    def put(self, item: T_contra) -> None: ...
```

### Variance Summary Table

| Variance | When | Example | Meaning |
|----------|------|---------|---------|
| **Invariant** | Mutable containers | `list[T]` | `list[Dog]` ≠ `list[Animal]` |
| **Covariant** | Read-only / producers | `Sequence[T]`, `Iterator[T]` | `Sequence[Dog]` → `Sequence[Animal]` |
| **Contravariant** | Write-only / consumers | `Callable[[T], None]` | `Callable[[Animal], None]` → `Callable[[Dog], None]` |

---

## Practical Guidelines

### When to Use @overload

- Function returns different types based on input
- Method has multiple valid signatures
- You want precise return type based on arguments

### When to Use TypedDict

- Working with JSON data from APIs
- Config dictionaries with known structure
- When you need typed dictionary access

### When to Use cast()

- You know the type better than the checker
- Working with dynamic data (JSON, external APIs)
- **Use sparingly** - prefer proper type narrowing

### Variance Quick Rules

1. **For parameters**: Use `Sequence` not `list` for read-only
2. **For returns**: Use specific types
3. **Mutable containers**: Always invariant
4. **Callables**: Contravariant in parameters, covariant in return

---

## Quick Reference

```python
from typing import (
    overload, TypedDict, cast, get_type_hints,
    get_origin, get_args, TypeVar, Generic,
    Required, NotRequired
)

# Overloaded function
@overload
def func(x: int) -> int: ...
@overload
def func(x: str) -> str: ...
def func(x):
    return x * 2

# TypedDict
class PersonDict(TypedDict):
    name: str
    age: int
    email: NotRequired[str]

# Cast (use sparingly!)
value = cast(TargetType, some_value)

# Generic class
T = TypeVar('T')
class Container(Generic[T]):
    def __init__(self, item: T) -> None:
        self.item = item

# Covariant TypeVar (for producers/outputs)
T_co = TypeVar('T_co', covariant=True)

# Contravariant TypeVar (for consumers/inputs)
T_contra = TypeVar('T_contra', contravariant=True)

# Runtime type inspection
get_type_hints(func)
get_origin(list[int])  # list
get_args(list[int])    # (int,)
```

---

## Summary

1. **@overload**: Define multiple type signatures for one function
2. **TypedDict**: Type dictionaries with specific keys and value types
3. **cast()**: Tell the type checker you know the type (no runtime effect)
4. **Generic classes**: Create reusable typed containers with `Generic[T]`
5. **Variance**: Understand covariant (output), contravariant (input), invariant (mutable)
6. **Use Sequence over list**: For read-only parameters, enables covariance
