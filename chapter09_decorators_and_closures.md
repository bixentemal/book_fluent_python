# Decorators and Closures - Practical Memo

## What is a Decorator?

A decorator is a callable that takes a function as an argument and returns a replacement function (or the same function enhanced).

```python
@decorate
def target():
    print('running target()')

# Is equivalent to:
def target():
    print('running target()')
target = decorate(target)
```

**Three essential facts:**
1. A decorator is a function (or callable)
2. A decorator may replace the decorated function with a different one
3. Decorators run at **import time**, not when the function is called

---

## Decorator Execution: Import Time vs Runtime

```python
registry = []

def register(func):
    print(f'registering {func}')  # Runs at import time!
    registry.append(func)
    return func

@register
def f1():
    print('running f1')

@register
def f2():
    print('running f2')
```

When this module is imported:
```
registering <function f1 at 0x...>
registering <function f2 at 0x...>
```

The decorator code runs immediately, but `f1()` and `f2()` only run when explicitly called.

---

## Variable Scope Rules

Python determines variable scope at **compile time**, not runtime:

```python
b = 6

def f1(a):
    print(a)
    print(b)  # b is global - works fine

f1(3)  # Output: 3, 6

def f2(a):
    print(a)
    print(b)  # ERROR: b is local because of assignment below
    b = 9     # This makes b local for the ENTIRE function

f2(3)  # UnboundLocalError: local variable 'b' referenced before assignment
```

**Rule:** If a variable is assigned anywhere in a function, it's local for the entire function.

### The `global` Declaration

```python
b = 6

def f3(a):
    global b    # Declare b as global
    print(b)    # Now reads global b
    b = 9       # Modifies global b

f3(3)   # Output: 6
print(b) # Output: 9
```

---

## Closures

A closure is a function that captures variables from its enclosing scope.

```python
def make_averager():
    series = []  # Free variable - captured by inner function

    def averager(new_value):
        series.append(new_value)  # Uses 'series' from enclosing scope
        return sum(series) / len(series)

    return averager

avg = make_averager()
avg(10)  # 10.0
avg(11)  # 10.5
avg(12)  # 11.0
```

**Inspecting the closure:**
```python
avg.__code__.co_freevars      # ('series',)
avg.__closure__[0].cell_contents  # [10, 11, 12]
```

### The `nonlocal` Declaration

When you need to **rebind** (not just mutate) a free variable:

```python
def make_averager():
    count = 0
    total = 0

    def averager(new_value):
        nonlocal count, total  # Required to rebind immutable variables
        count += 1
        total += new_value
        return total / count

    return averager
```

**Without `nonlocal`:** `count += 1` creates a new local variable, causing `UnboundLocalError`.

**Key insight:**
- Mutable objects (lists, dicts) can be modified without `nonlocal`
- Immutable objects (int, str, tuple) require `nonlocal` to rebind

---

## Implementing a Decorator

### Basic Pattern

```python
def my_decorator(func):
    def wrapper(*args, **kwargs):
        # Do something before
        result = func(*args, **kwargs)
        # Do something after
        return result
    return wrapper
```

### Example: Timing Decorator

```python
import time

def clock(func):
    def clocked(*args, **kwargs):
        t0 = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - t0
        print(f'[{elapsed:.8f}s] {func.__name__}({args}, {kwargs}) -> {result}')
        return result
    return clocked

@clock
def slow_function(n):
    time.sleep(n)
    return n

slow_function(0.5)
# [0.50123456s] slow_function((0.5,), {}) -> 0.5
```

### Preserving Function Metadata with `functools.wraps`

Without `@wraps`, the decorated function loses its identity:

```python
@clock
def factorial(n):
    """Return n!"""
    return 1 if n < 2 else n * factorial(n - 1)

factorial.__name__  # 'clocked' - WRONG!
factorial.__doc__   # None - WRONG!
```

**Solution:** Use `@functools.wraps`:

```python
import functools

def clock(func):
    @functools.wraps(func)  # Copies __name__, __doc__, etc.
    def clocked(*args, **kwargs):
        # ... same as before
        return result
    return clocked

factorial.__name__  # 'factorial' - Correct!
factorial.__doc__   # 'Return n!' - Correct!
```

---

## Standard Library Decorators

### `@functools.cache` (Python 3.9+)

Memoization - caches all results forever:

```python
from functools import cache

@cache
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

fibonacci(30)  # Fast! Results are cached
```

### `@functools.lru_cache`

Least Recently Used cache with size limit:

```python
from functools import lru_cache

@lru_cache(maxsize=128)  # Keep last 128 results
def expensive_computation(n):
    # ...
    return result

# Check cache statistics
expensive_computation.cache_info()
# CacheInfo(hits=3, misses=2, maxsize=128, currsize=2)

# Clear the cache
expensive_computation.cache_clear()
```

**Python 3.8+:** Can use `@lru_cache` without parentheses (defaults: `maxsize=128`, `typed=False`)

### `@functools.singledispatch`

Generic function with type-based dispatch:

```python
from functools import singledispatch

@singledispatch
def htmlize(obj):
    return f'<pre>{obj}</pre>'

@htmlize.register(str)
def _(text):
    return f'<p>{text}</p>'

@htmlize.register(int)
@htmlize.register(float)
def _(n):
    return f'<span class="number">{n}</span>'

@htmlize.register(list)
def _(lst):
    items = '\n'.join(f'<li>{htmlize(item)}</li>' for item in lst)
    return f'<ul>\n{items}\n</ul>'

htmlize('Hello')      # '<p>Hello</p>'
htmlize(42)           # '<span class="number">42</span>'
htmlize([1, 'two'])   # '<ul>\n<li>...</li>\n...</ul>'
```

**Using type hints (Python 3.7+):**
```python
@htmlize.register
def _(text: str):
    return f'<p>{text}</p>'
```

---

## Parameterized Decorators

A parameterized decorator is a **decorator factory** - a function that returns a decorator.

### Pattern

```python
def decorator_factory(param1, param2):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Use param1, param2 here
            return func(*args, **kwargs)
        return wrapper
    return decorator

@decorator_factory('value1', 'value2')  # Returns a decorator
def my_function():
    pass
```

### Example: Repeat Decorator

```python
import functools

def repeat(times):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(3)
def greet(name):
    print(f'Hello, {name}!')

greet('World')
# Hello, World!
# Hello, World!
# Hello, World!
```

### Example: Optional Arguments Decorator

Make a decorator work with or without arguments:

```python
import functools

def clock(func=None, *, fmt='[{elapsed:.8f}s] {name}({args}) -> {result}'):
    if func is None:
        # Called with arguments: @clock(fmt='...')
        return lambda f: clock(f, fmt=fmt)

    @functools.wraps(func)
    def clocked(*args, **kwargs):
        t0 = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - t0
        name = func.__name__
        print(fmt.format(**locals()))
        return result
    return clocked

# Both work:
@clock
def func1(): pass

@clock(fmt='{name}: {elapsed}s')
def func2(): pass
```

---

## Class-Based Decorators

Using a class instead of a nested function:

```python
import functools

class CountCalls:
    def __init__(self, func):
        functools.update_wrapper(self, func)
        self.func = func
        self.count = 0

    def __call__(self, *args, **kwargs):
        self.count += 1
        return self.func(*args, **kwargs)

@CountCalls
def greet(name):
    print(f'Hello, {name}!')

greet('Alice')
greet('Bob')
print(greet.count)  # 2
```

---

## Stacked Decorators

Decorators can be stacked (applied bottom-up):

```python
@d1
@d2
def f():
    pass

# Equivalent to:
f = d1(d2(f))
```

---

## Common Patterns Summary

| Pattern | Use Case |
|---------|----------|
| Registration decorator | Add functions to a registry (e.g., URL routing) |
| Timing decorator | Measure execution time |
| Caching decorator | Memoize expensive computations |
| Logging decorator | Log function calls |
| Validation decorator | Check arguments/return values |
| Retry decorator | Retry on failure |
| Access control | Check permissions |

---

## Quick Reference

| Concept | Syntax |
|---------|--------|
| Simple decorator | `@decorator` |
| Parameterized decorator | `@decorator(args)` |
| Access global variable | `global x` |
| Modify closure variable | `nonlocal x` |
| Preserve metadata | `@functools.wraps(func)` |
| Cache all results | `@functools.cache` |
| Cache with limit | `@functools.lru_cache(maxsize=N)` |
| Type-based dispatch | `@functools.singledispatch` |

---

## Gotchas

1. **Decorator runs at import time** - side effects happen immediately
2. **Forgetting `@functools.wraps`** - breaks introspection
3. **Confusing `nonlocal` and `global`** - `nonlocal` is for enclosing function scope
4. **Decorator must return callable** - unless it's a registration decorator
5. **Decorated recursive functions** - each recursive call goes through the decorator
