# Type Hints in Functions - Practical Memo

## What is Gradual Typing?

Python's type system is **gradual** (PEP 484):
- **Optional**: Type hints are never required; the type checker assumes `Any` for untyped code
- **No runtime enforcement**: Type hints are ignored at runtime; they're for static analysis only
- **No performance benefit**: Annotations don't optimize bytecode

**Key insight**: You can add type hints incrementally, file by file, function by function.

---

## Quick Reference: Common Type Hints

### Basic Types

```python
def greet(name: str) -> str:
    return f'Hello, {name}'

def add(a: int, b: int) -> int:
    return a + b

def process(data: bytes) -> bool:
    return len(data) > 0
```

### Optional and Union

```python
from typing import Optional, Union

# Optional[X] means X or None
def find_user(user_id: int) -> Optional[str]:
    if user_id == 0:
        return None
    return 'Alice'

# Union[X, Y] means X or Y
def parse_id(value: Union[str, int]) -> int:
    return int(value)

# Python 3.10+ syntax (preferred)
def find_user(user_id: int) -> str | None:
    ...

def parse_id(value: str | int) -> int:
    ...
```

### Collections

```python
# Python 3.9+ - use built-in types directly
def process_items(items: list[str]) -> dict[str, int]:
    return {item: len(item) for item in items}

def get_coords() -> tuple[float, float]:
    return (1.0, 2.0)

# Variable-length tuple
def get_values() -> tuple[int, ...]:
    return (1, 2, 3, 4, 5)

# For older Python, import from typing
from typing import List, Dict, Tuple
def old_style(items: List[str]) -> Dict[str, int]:
    ...
```

### Callable

```python
from typing import Callable

# Callable[[arg_types], return_type]
def apply_func(func: Callable[[int, int], int], a: int, b: int) -> int:
    return func(a, b)

# No arguments
def run(callback: Callable[[], None]) -> None:
    callback()

# Any arguments (use ... for ParamSpec-like behavior)
def decorator(func: Callable[..., str]) -> Callable[..., str]:
    ...
```

### Iterables and Sequences

```python
from collections.abc import Iterable, Sequence, Iterator

# Use Iterable for input you only need to iterate once
def sum_all(numbers: Iterable[float]) -> float:
    return sum(numbers)

# Use Sequence when you need indexing or len()
def first_and_last(items: Sequence[str]) -> tuple[str, str]:
    return items[0], items[-1]

# Use Iterator for generator return types
def count_up(n: int) -> Iterator[int]:
    for i in range(n):
        yield i
```

---

## TypeVar: Generic Functions

```python
from typing import TypeVar

T = TypeVar('T')

# T is bound to the same type for input and output
def first(items: list[T]) -> T:
    return items[0]

# With constraints
Number = TypeVar('Number', int, float)

def double(x: Number) -> Number:
    return x * 2

# With upper bound
from collections.abc import Hashable
HashableT = TypeVar('HashableT', bound=Hashable)

def mode(data: Iterable[HashableT]) -> HashableT:
    # Returns most common item
    ...
```

---

## Protocols: Static Duck Typing

Protocols let you define structural types (duck typing for static checkers):

```python
from typing import Protocol

class SupportsRead(Protocol):
    def read(self, n: int = -1) -> bytes:
        ...

# Any class with a compatible read() method works
def read_all(reader: SupportsRead) -> bytes:
    return reader.read()

# Works with file objects, io.BytesIO, custom classes, etc.
```

### Common Built-in Protocols

```python
from typing import SupportsInt, SupportsFloat, SupportsAbs, SupportsBytes

def to_int(x: SupportsInt) -> int:
    return int(x)

def magnitude(x: SupportsAbs[float]) -> float:
    return abs(x)
```

---

## Variadic Parameters

```python
from typing import Any

# *args with uniform type
def sum_ints(*args: int) -> int:
    return sum(args)

# **kwargs with uniform type
def configure(**kwargs: str) -> None:
    for key, value in kwargs.items():
        print(f'{key}={value}')

# For heterogeneous types, use Any or specific overloads
def flexible(*args: Any, **kwargs: Any) -> None:
    ...
```

---

## Special Return Types

```python
from typing import NoReturn, Never

# NoReturn: function never returns normally (raises or infinite loop)
def fail(msg: str) -> NoReturn:
    raise SystemExit(msg)

# None: function returns None (implicit or explicit)
def log(msg: str) -> None:
    print(msg)

# Python 3.11+: Never is preferred over NoReturn
def infinite_loop() -> Never:
    while True:
        pass
```

---

## Duck Typing vs Nominal Typing

| Aspect | Duck Typing | Nominal Typing |
|--------|-------------|----------------|
| **When** | Runtime | Static analysis |
| **Check** | "Does it quack?" | "Is it declared as Duck?" |
| **Focus** | Supported operations | Class hierarchy |
| **Python** | Default behavior | With type hints |

```python
class Bird:
    pass

class Duck(Bird):
    def quack(self):
        print('Quack!')

# Duck typing (no hints) - works at runtime if object has quack()
def alert(birdie):
    birdie.quack()

# Nominal typing - type checker validates based on declared type
def alert_duck(birdie: Duck) -> None:
    birdie.quack()  # OK: Duck has quack()

def alert_bird(birdie: Bird) -> None:
    birdie.quack()  # ERROR: Bird has no quack()
```

---

## Mypy Configuration

### Command Line

```bash
# Basic check
mypy module.py

# Stricter checking
mypy --strict module.py

# Common useful flags
mypy --disallow-untyped-defs module.py      # Require all functions typed
mypy --disallow-incomplete-defs module.py   # Only check partially typed functions
mypy --ignore-missing-imports module.py     # Ignore untyped libraries
```

### Configuration File (mypy.ini)

```ini
[mypy]
python_version = 3.12
warn_unused_configs = True
disallow_incomplete_defs = True
ignore_missing_imports = True

# Per-module overrides
[mypy-tests.*]
disallow_untyped_defs = False
```

---

## Type Aliases

```python
# Simple alias
UserId = int
Username = str

# Complex alias
from typing import TypeAlias

ConnectionOptions: TypeAlias = dict[str, str]
Address: TypeAlias = tuple[str, int]

# Python 3.12+ syntax
type Vector = list[float]
type ConnectionPool = dict[str, list[Connection]]
```

---

## Overloaded Functions

```python
from typing import overload

@overload
def process(x: int) -> int: ...
@overload
def process(x: str) -> str: ...
@overload
def process(x: list[int]) -> list[int]: ...

def process(x):
    if isinstance(x, int):
        return x * 2
    elif isinstance(x, str):
        return x.upper()
    else:
        return [i * 2 for i in x]
```

---

## Best Practices

1. **Start with function signatures** - annotate parameters and return types first
2. **Use abstract types for parameters** - accept `Iterable[T]` not `list[T]` when possible
3. **Use concrete types for returns** - return `list[T]` not `Iterable[T]`
4. **Prefer `| None` over `Optional`** - clearer syntax (Python 3.10+)
5. **Use `# type: ignore` sparingly** - only when you know better than the checker
6. **Don't fight the type checker** - if hints are too complex, reconsider the design

---

## Common Gotchas

### Forward References

```python
# Class references itself - use string or __future__
from __future__ import annotations

class Node:
    def __init__(self, value: int, next: Node | None = None):
        self.value = value
        self.next = next

# Or use string quotes (older style)
class Node:
    def __init__(self, value: int, next: 'Node | None' = None):
        ...
```

### Mutable Default Arguments

```python
# WRONG: annotation doesn't change default behavior
def append_to(item: str, target: list[str] = []) -> list[str]:
    target.append(item)
    return target

# CORRECT: use None as default
def append_to(item: str, target: list[str] | None = None) -> list[str]:
    if target is None:
        target = []
    target.append(item)
    return target
```

### = vs :

```python
# WRONG: sets default to the type str itself!
def greet(name = str) -> str:
    return f'Hello, {name}'

# CORRECT: annotation with colon
def greet(name: str) -> str:
    return f'Hello, {name}'
```

---

## Summary: When to Use What

| You Want To... | Use |
|----------------|-----|
| Accept any type | `Any` or no annotation |
| Accept None or X | `X \| None` or `Optional[X]` |
| Accept multiple types | `X \| Y` or `Union[X, Y]` |
| Accept any iterable | `Iterable[T]` |
| Accept indexable sequence | `Sequence[T]` |
| Accept any mapping | `Mapping[K, V]` |
| Return a generator | `Iterator[T]` or `Generator[Y, S, R]` |
| Accept a function | `Callable[[Args], Return]` |
| Duck-type by behavior | `Protocol` subclass |
| Generic over a type | `TypeVar` |
| Function never returns | `NoReturn` or `Never` |
