# Chapter 7: Functions as First-Class Objects

## Quick Reference: Comparison Table

| Concept | What It Is | Use Case | Example |
|---------|-----------|----------|---------|
| First-class function | Functions are objects | Pass/return functions, store in data structures | `funcs = [len, str, int]` |
| Higher-order function | Takes or returns function | Callbacks, decorators, factories | `sorted(data, key=len)` |
| `map()` | Apply func to all items | Transformations | Prefer: `[f(x) for x in items]` |
| `filter()` | Keep items where func is True | Filtering | Prefer: `[x for x in items if cond]` |
| `reduce()` | Accumulate to single value | Aggregation | Prefer: `sum()`, `any()`, `all()` |
| `lambda` | Anonymous function | Short callbacks | `key=lambda x: x.name` |
| `operator` module | Function versions of operators | Cleaner than lambda | `key=attrgetter('name')` |
| `functools.partial` | Pre-fill function arguments | Specialize generic functions | `int_base2 = partial(int, base=2)` |

---

## 1. Functions as First-Class Objects

Functions can be assigned, passed, returned, and stored like any other object.

```python
# Assign to variable
def factorial(n):
    return 1 if n < 2 else n * factorial(n - 1)

fact = factorial          # Assign function to variable
print(fact(5))            # 120
print(fact.__name__)      # 'factorial'

# Store in data structures
operations = {
    'add': lambda a, b: a + b,
    'sub': lambda a, b: a - b,
    'mul': lambda a, b: a * b,
}
print(operations['add'](2, 3))  # 5

# Function attributes (functions are objects!)
print(factorial.__doc__)       # docstring
print(factorial.__name__)      # 'factorial'
print(factorial.__defaults__)  # default arg values
print(factorial.__code__.co_varnames)  # ('n',)
```

---

## 2. Higher-Order Functions

A function that **takes a function as argument** or **returns a function**.

```python
# TAKING a function as argument
def apply_twice(func, value):
    return func(func(value))

print(apply_twice(lambda x: x * 2, 3))  # 12

# RETURNING a function
def make_multiplier(n):
    def multiplier(x):
        return x * n
    return multiplier

triple = make_multiplier(3)
print(triple(7))  # 21

# Built-in higher-order functions
fruits = ['strawberry', 'fig', 'apple', 'cherry', 'raspberry', 'banana']
print(sorted(fruits, key=len))
# ['fig', 'apple', 'cherry', 'banana', 'raspberry', 'strawberry']

# Reverse sort by last letter
print(sorted(fruits, key=lambda word: word[::-1]))
# ['banana', 'apple', 'fig', 'raspberry', 'strawberry', 'cherry']
```

### Common Higher-Order Functions

| Function | Purpose | Example |
|----------|---------|---------|
| `sorted(iterable, key=func)` | Sort by computed key | `sorted(users, key=lambda u: u.age)` |
| `max/min(iterable, key=func)` | Find extreme by key | `max(words, key=len)` |
| `map(func, iterable)` | Transform all items | `map(str.upper, words)` |
| `filter(func, iterable)` | Keep matching items | `filter(str.isalpha, chars)` |
| `functools.reduce(func, iterable)` | Accumulate to one value | `reduce(mul, range(1, 6))` |

---

## 3. Modern Replacements for map, filter, and reduce

### map() vs List Comprehension

```python
# OLD STYLE - map
numbers = [1, 2, 3, 4, 5]
squared = list(map(lambda x: x ** 2, numbers))

# MODERN - List comprehension (preferred)
squared = [x ** 2 for x in numbers]

# Generator expression for lazy evaluation
squared_gen = (x ** 2 for x in numbers)

# map is still useful when you already have a named function
words = ['hello', 'world']
upper_words = list(map(str.upper, words))  # Clean!
# vs
upper_words = [s.upper() for s in words]   # Also fine
```

### filter() vs List Comprehension

```python
# OLD STYLE - filter
numbers = range(-5, 6)
positives = list(filter(lambda x: x > 0, numbers))

# MODERN - List comprehension (preferred)
positives = [x for x in numbers if x > 0]

# Combined map + filter
# OLD
result = list(map(lambda x: x ** 2, filter(lambda x: x > 0, numbers)))

# MODERN - Much clearer!
result = [x ** 2 for x in numbers if x > 0]
```

### reduce() vs Built-in Alternatives

```python
from functools import reduce
from operator import add, mul

numbers = [1, 2, 3, 4, 5]

# AVOID reduce for common operations
total = reduce(add, numbers)      # Works but...
total = sum(numbers)              # BETTER!

product = reduce(mul, numbers)    # Works but...
import math
product = math.prod(numbers)      # BETTER! (Python 3.8+)

# AVOID reduce for any/all logic
has_even = reduce(lambda a, b: a or b % 2 == 0, numbers, False)
has_even = any(x % 2 == 0 for x in numbers)  # BETTER!

all_positive = reduce(lambda a, b: a and b > 0, numbers, True)
all_positive = all(x > 0 for x in numbers)   # BETTER!
```

### When reduce() IS Appropriate

```python
from functools import reduce
from operator import or_

# Combining flags/sets
flags = [0b001, 0b010, 0b100]
combined = reduce(or_, flags)  # 0b111

# Composing functions
def compose(*funcs):
    """compose(f, g, h)(x) == f(g(h(x)))"""
    def composed(x):
        return reduce(lambda acc, f: f(acc), reversed(funcs), x)
    return composed

# Deep dictionary access
def deep_get(d, *keys):
    return reduce(lambda d, k: d.get(k, {}), keys, d)

data = {'a': {'b': {'c': 42}}}
print(deep_get(data, 'a', 'b', 'c'))  # 42
```

### Comparison Table: map/filter/reduce vs Modern Python

| Old Style | Modern Replacement | When to Use Modern |
|-----------|-------------------|-------------------|
| `map(func, seq)` | `[func(x) for x in seq]` | Always, unless func is already named |
| `filter(func, seq)` | `[x for x in seq if cond]` | Always |
| `reduce(add, seq)` | `sum(seq)` | Always |
| `reduce(mul, seq)` | `math.prod(seq)` | Always (3.8+) |
| `reduce(or_, seq)` | `any(seq)` | For boolean reduction |
| `reduce(and_, seq)` | `all(seq)` | For boolean reduction |
| `reduce(func, seq)` | Keep reduce | Complex accumulations |

---

## 4. The Nine Flavors of Callable Objects

Anything that can be called with `()` is callable. Check with `callable(obj)`.

```python
# Check if callable
print(callable(len))        # True
print(callable('hello'))    # False
print(callable(str))        # True (classes are callable)
```

### All 9 Callable Types

| # | Type | Description | Example |
|---|------|-------------|---------|
| 1 | User-defined function | Created with `def` or `lambda` | `def foo(): pass` |
| 2 | Built-in function | Implemented in C | `len`, `open`, `print` |
| 3 | Built-in method | C methods | `'hello'.upper` |
| 4 | Method | Function in class body | `obj.method()` |
| 5 | Class | Calling class creates instance | `MyClass()` |
| 6 | Class instance | If class defines `__call__` | `obj()` |
| 7 | Generator function | Uses `yield` | Returns generator object |
| 8 | Native coroutine | `async def` | Returns coroutine object |
| 9 | Asynchronous generator | `async def` + `yield` | Returns async generator |

### Making Instances Callable with `__call__`

```python
# Callable class instance - useful for stateful functions
class Counter:
    def __init__(self):
        self.count = 0

    def __call__(self):
        self.count += 1
        return self.count

counter = Counter()
print(counter())  # 1
print(counter())  # 2
print(counter())  # 3
print(callable(counter))  # True

# Practical example: Memoizing callable
class Memoize:
    def __init__(self, func):
        self.func = func
        self.cache = {}

    def __call__(self, *args):
        if args not in self.cache:
            self.cache[args] = self.func(*args)
        return self.cache[args]

@Memoize
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

print(fibonacci(100))  # Fast!
```

---

## 5. Packages for Functional Programming

### The `operator` Module

Provides function equivalents of operators - cleaner than lambdas.

```python
from operator import add, mul, itemgetter, attrgetter, methodcaller

# Arithmetic operators as functions
from functools import reduce
print(reduce(mul, range(1, 6)))  # 120 (factorial)

# itemgetter - get items by index/key
data = [('a', 1), ('b', 2), ('c', 3)]
sorted_by_second = sorted(data, key=itemgetter(1))

# Multiple keys
student_data = [
    ('john', 'A', 15),
    ('jane', 'B', 12),
    ('dave', 'B', 10),
]
# Sort by grade (index 1), then age (index 2)
sorted(student_data, key=itemgetter(1, 2))

# For dictionaries
users = [
    {'name': 'John', 'age': 30},
    {'name': 'Jane', 'age': 25},
]
sorted(users, key=itemgetter('age'))

# attrgetter - get attributes by name
from collections import namedtuple

City = namedtuple('City', 'name country population')
cities = [
    City('Tokyo', 'Japan', 36933000),
    City('Delhi', 'India', 24953000),
    City('Shanghai', 'China', 24150000),
]

# Sort by attribute
sorted(cities, key=attrgetter('population'))

# Nested attribute access
class Person:
    def __init__(self, name, address):
        self.name = name
        self.address = address

class Address:
    def __init__(self, city):
        self.city = city

p = Person('John', Address('NYC'))
get_city = attrgetter('address.city')
print(get_city(p))  # 'NYC'

# methodcaller - call a method
words = ['hello', 'WORLD', 'Python']
upper_words = list(map(methodcaller('upper'), words))
# Same as: [w.upper() for w in words]

# With arguments
replace_spaces = methodcaller('replace', ' ', '_')
print(replace_spaces('hello world'))  # 'hello_world'
```

### Comparison: lambda vs operator

| Task | lambda | operator (preferred) |
|------|--------|---------------------|
| Multiply | `lambda a, b: a * b` | `mul` |
| Get dict value | `lambda d: d['name']` | `itemgetter('name')` |
| Get attribute | `lambda o: o.name` | `attrgetter('name')` |
| Call method | `lambda s: s.upper()` | `methodcaller('upper')` |
| Get index | `lambda t: t[0]` | `itemgetter(0)` |

### The `functools` Module

```python
from functools import partial, partialmethod, reduce, wraps

# partial - freeze some arguments
def power(base, exponent):
    return base ** exponent

square = partial(power, exponent=2)
cube = partial(power, exponent=3)

print(square(5))  # 25
print(cube(5))    # 125

# Practical: partial for callbacks
from functools import partial

def handle_button_click(button_id, event):
    print(f"Button {button_id} clicked!")

# Pre-fill button_id for each button
button1_handler = partial(handle_button_click, 'save')
button2_handler = partial(handle_button_click, 'cancel')

# Practical: partial with int for base conversion
int_base2 = partial(int, base=2)
print(int_base2('1010'))  # 10

int_base16 = partial(int, base=16)
print(int_base16('ff'))   # 255

# partialmethod - for methods in classes
class Cell:
    def __init__(self):
        self.alive = False

    def set_state(self, state):
        self.alive = state

    # Create specialized methods
    set_alive = partialmethod(set_state, True)
    set_dead = partialmethod(set_state, False)

cell = Cell()
cell.set_alive()
print(cell.alive)  # True
```

---

## 6. Lambda Best Practices

```python
# GOOD: Short, simple transforms
sorted(names, key=lambda s: s.lower())
max(items, key=lambda x: x.priority)

# BAD: Complex logic in lambda
# Don't do this:
process = lambda x: x.strip().lower().replace(' ', '_') if x else ''
# Do this instead:
def process(x):
    if not x:
        return ''
    return x.strip().lower().replace(' ', '_')

# PREFER operator module when possible
# Instead of:
sorted(items, key=lambda x: x['name'])
# Use:
sorted(items, key=itemgetter('name'))

# REMEMBER: lambda is just syntactic sugar
# These are equivalent:
add = lambda a, b: a + b
def add(a, b): return a + b
```

---

## 7. Function Introspection

```python
def greet(name, greeting='Hello', *, excited=False):
    """Generate a greeting message."""
    msg = f"{greeting}, {name}!"
    return msg.upper() if excited else msg

# Useful attributes
print(greet.__name__)        # 'greet'
print(greet.__doc__)         # 'Generate a greeting message.'
print(greet.__defaults__)    # ('Hello',) - positional defaults
print(greet.__kwdefaults__)  # {'excited': False} - keyword-only defaults
print(greet.__code__.co_varnames)  # ('name', 'greeting', 'excited', 'msg')

# Using inspect module for detailed info
import inspect

sig = inspect.signature(greet)
print(sig)  # (name, greeting='Hello', *, excited=False)

for name, param in sig.parameters.items():
    print(f"{name}: {param.kind.name}, default={param.default}")
# name: POSITIONAL_OR_KEYWORD, default=<class 'inspect._empty'>
# greeting: POSITIONAL_OR_KEYWORD, default=Hello
# excited: KEYWORD_ONLY, default=False
```

---

## Quick Reference: When to Use What

| Need | Solution |
|------|----------|
| Sort by attribute | `key=attrgetter('attr')` |
| Sort by dict key | `key=itemgetter('key')` |
| Sort by method result | `key=methodcaller('method')` |
| Transform all items | List comprehension `[f(x) for x in items]` |
| Filter items | List comprehension `[x for x in items if cond]` |
| Sum values | `sum(items)` |
| Product of values | `math.prod(items)` |
| Any/all boolean | `any(...)` / `all(...)` |
| Pre-fill arguments | `functools.partial(func, arg1, arg2)` |
| Stateful callable | Class with `__call__` |
| Simple one-liner | `lambda x: expr` |
