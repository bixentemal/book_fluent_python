# Python Data Class Builders - Practical Memo

## Quick Comparison Table

| Feature | Plain Class | `collections.namedtuple` | `typing.NamedTuple` | `@dataclass` |
|---------|-------------|--------------------------|---------------------|--------------|
| **Mutable** | Yes | No | No | Yes (default) |
| **Type hints** | Optional | No | Required | Required |
| **Auto `__init__`** | No | Yes | Yes | Yes |
| **Auto `__repr__`** | No | Yes | Yes | Yes |
| **Auto `__eq__`** | No | Yes | Yes | Yes |
| **Auto `__hash__`** | Yes | Yes | Yes | Only if frozen |
| **Inheritance** | Any | tuple | tuple | Any |
| **Default values** | Yes | Yes (rightmost) | Yes | Yes |
| **Class syntax** | Yes | No | Yes | Yes |
| **Ordering (`<`, `>`)** | No | Yes | Yes | Optional |
| **Memory efficient** | No | Yes | Yes | No |
| **Convert to dict** | No | `._asdict()` | `._asdict()` | `asdict()` |

## When to Use Which

| Use Case | Best Choice |
|----------|-------------|
| Simple immutable record, memory-sensitive | `collections.namedtuple` |
| Immutable record with type hints | `typing.NamedTuple` |
| Mutable data container with validation | `@dataclass` |
| Immutable data with custom behavior | `@dataclass(frozen=True)` |
| Need to inherit from another class | `@dataclass` |
| JSON serialization / dict interop | `@dataclass` or `NamedTuple` |
| Database models, ORM entities | `@dataclass` |
| Configuration objects | `@dataclass(frozen=True)` |
| Function return with multiple values | `typing.NamedTuple` |
| Drop-in tuple replacement | `collections.namedtuple` |

---

## 1. `collections.namedtuple`

**Best for:** Simple, lightweight immutable records. Tuple-compatible.

```python
from collections import namedtuple

# Basic definition
Point = namedtuple('Point', ['x', 'y'])
# or: Point = namedtuple('Point', 'x y')

# With defaults (rightmost fields only)
City = namedtuple('City', 'name country population', defaults=['Unknown', 0])

# Usage
p = Point(3, 4)
print(p.x, p.y)      # 3 4
print(p[0], p[1])    # 3 4 (tuple indexing works)

# Useful methods
p._asdict()          # {'x': 3, 'y': 4}
p._replace(x=10)     # Point(x=10, y=4) - returns new instance
Point._fields        # ('x', 'y')
Point._field_defaults  # {}

# Unpack like tuple
x, y = p
```

---

## 2. `typing.NamedTuple`

**Best for:** Immutable records with type hints. Class-based syntax.

```python
from typing import NamedTuple

class Coordinate(NamedTuple):
    lat: float
    lon: float
    reference: str = 'WGS84'  # default value

    # Custom methods allowed
    def __str__(self) -> str:
        ns = 'N' if self.lat >= 0 else 'S'
        ew = 'E' if self.lon >= 0 else 'W'
        return f'{abs(self.lat):.2f}°{ns}, {abs(self.lon):.2f}°{ew}'

# Usage
paris = Coordinate(48.8566, 2.3522)
print(paris)           # 48.86°N, 2.35°E
print(paris.lat)       # 48.8566

# Still a tuple
isinstance(paris, tuple)  # True
lat, lon, ref = paris     # Unpacking works

# Immutable
paris.lat = 0  # AttributeError!
```

---

## 3. `@dataclass`

**Best for:** Flexible data containers. Mutable by default. Full customization.

### Basic Usage

```python
from dataclasses import dataclass

@dataclass
class Product:
    name: str
    price: float
    quantity: int = 0

    @property
    def total_value(self) -> float:
        return self.price * self.quantity

# Usage
item = Product('Widget', 9.99, 5)
print(item)  # Product(name='Widget', price=9.99, quantity=5)

item.quantity = 10  # Mutable - works fine
```

### Frozen (Immutable)

```python
@dataclass(frozen=True)
class Config:
    host: str
    port: int = 8080
    debug: bool = False

cfg = Config('localhost')
cfg.port = 9000  # FrozenInstanceError!
hash(cfg)        # Works - frozen dataclasses are hashable
```

### With Ordering

```python
@dataclass(order=True)
class Version:
    major: int
    minor: int
    patch: int = 0

v1 = Version(1, 0, 0)
v2 = Version(2, 0, 0)
print(v1 < v2)  # True
sorted([v2, v1])  # [Version(1, 0, 0), Version(2, 0, 0)]
```

### Field Options

```python
from dataclasses import dataclass, field

@dataclass
class Order:
    items: list = field(default_factory=list)  # Mutable default
    customer: str = field(default='Guest')
    _internal: str = field(default='', repr=False)  # Hide from repr
    id: int = field(default=0, compare=False)  # Exclude from __eq__

# default_factory for mutable types (NEVER use list directly!)
@dataclass
class ShoppingCart:
    items: list[str] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)
```

### Post-Init Processing

```python
@dataclass
class Rectangle:
    width: float
    height: float
    area: float = field(init=False)  # Not in __init__

    def __post_init__(self):
        self.area = self.width * self.height

r = Rectangle(3, 4)
print(r.area)  # 12.0
```

### Inheritance

```python
@dataclass
class Person:
    name: str
    age: int

@dataclass
class Employee(Person):
    employee_id: str
    department: str = 'General'

emp = Employee('Alice', 30, 'E123')
print(emp)  # Employee(name='Alice', age=30, employee_id='E123', department='General')
```

### Utility Functions

```python
from dataclasses import asdict, astuple, fields, replace

@dataclass
class User:
    name: str
    email: str
    active: bool = True

user = User('Bob', 'bob@example.com')

# Convert to dict/tuple
asdict(user)   # {'name': 'Bob', 'email': 'bob@example.com', 'active': True}
astuple(user)  # ('Bob', 'bob@example.com', True)

# Create modified copy
new_user = replace(user, email='newemail@example.com')

# Introspection
for f in fields(User):
    print(f.name, f.type, f.default)
```

---

## Common Patterns

### JSON Serialization

```python
import json
from dataclasses import dataclass, asdict

@dataclass
class Event:
    name: str
    timestamp: str
    data: dict = field(default_factory=dict)

event = Event('click', '2024-01-15T10:00:00', {'x': 100, 'y': 200})
json_str = json.dumps(asdict(event))
```

### Validation in `__post_init__`

```python
@dataclass
class PositiveNumber:
    value: float

    def __post_init__(self):
        if self.value <= 0:
            raise ValueError(f'value must be positive, got {self.value}')
```

### Factory Pattern

```python
@dataclass
class Connection:
    host: str
    port: int

    @classmethod
    def from_url(cls, url: str) -> 'Connection':
        # parse url...
        host, port = url.split(':')
        return cls(host, int(port))

conn = Connection.from_url('localhost:5432')
```

---

## Performance Notes

- **Memory:** `namedtuple` and `NamedTuple` use less memory (no `__dict__`)
- **Speed:** All three have similar instantiation speed
- **Slots:** Use `@dataclass(slots=True)` (Python 3.10+) for memory efficiency

```python
@dataclass(slots=True)
class Point3D:
    x: float
    y: float
    z: float
# No __dict__, uses __slots__ for memory efficiency
```
