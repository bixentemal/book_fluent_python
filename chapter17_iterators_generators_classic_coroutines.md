# Iterators, Generators, and Classic Coroutines - Practical Memo

## Overview

Iteration is fundamental to data processing. Python's iterator protocol enables lazy evaluation—fetching items one at a time on demand. Generators provide an elegant way to implement iterators without the boilerplate of the classic Iterator pattern.

> "When I see patterns in my programs, I consider it a sign of trouble... I'm using abstractions that aren't powerful enough."
> — Paul Graham

---

## The Iterator Protocol

### Iterable vs Iterator

| Concept | Definition | Methods |
|---------|------------|---------|
| **Iterable** | Object that can provide an iterator | `__iter__()` |
| **Iterator** | Object that yields items one at a time | `__next__()`, `__iter__()` |

```python
# Iterable: has __iter__ that returns an iterator
class MyIterable:
    def __iter__(self):
        return MyIterator(self.data)

# Iterator: has __next__ and __iter__ (returns self)
class MyIterator:
    def __next__(self):
        # Return next item or raise StopIteration
        pass
    def __iter__(self):
        return self
```

### How iter() Works

When Python needs to iterate over object `x`:

1. Calls `iter(x)`
2. `iter()` checks for `__iter__` → calls it to get iterator
3. If no `__iter__`, checks for `__getitem__` → creates iterator that fetches by index
4. If neither exists → raises `TypeError`

```python
# Both are iterable:
class WithIter:
    def __iter__(self):
        return iter(self.items)

class WithGetitem:
    def __getitem__(self, index):
        return self.items[index]  # Also works!
```

---

## Sequences Are Iterable

Any class implementing `__getitem__` with 0-based indexing is iterable:

```python
import re
import reprlib

RE_WORD = re.compile(r'\w+')

class Sentence:
    def __init__(self, text):
        self.text = text
        self.words = RE_WORD.findall(text)

    def __getitem__(self, index):
        return self.words[index]

    def __len__(self):
        return len(self.words)

    def __repr__(self):
        return f'Sentence({reprlib.repr(self.text)})'
```

```python
s = Sentence('The quick brown fox')
for word in s:
    print(word)
# The, quick, brown, fox

list(s)  # ['The', 'quick', 'brown', 'fox']
s[0]     # 'The' (also supports indexing)
```

---

## Classic Iterator Pattern

Explicit iterator class (not idiomatic Python, but illustrates the pattern):

```python
class Sentence:
    def __init__(self, text):
        self.text = text
        self.words = RE_WORD.findall(text)

    def __iter__(self):
        return SentenceIterator(self.words)


class SentenceIterator:
    def __init__(self, words):
        self.words = words
        self.index = 0

    def __next__(self):
        try:
            word = self.words[self.index]
        except IndexError:
            raise StopIteration()
        self.index += 1
        return word

    def __iter__(self):
        return self
```

**Important:** Don't make the iterable an iterator for itself! Each call to `iter()` should return a fresh, independent iterator.

---

## Generator Functions

A function with `yield` is a generator function. When called, it returns a generator object:

```python
def gen_123():
    yield 1
    yield 2
    yield 3

gen_123        # <function gen_123 at 0x...>
gen_123()      # <generator object gen_123 at 0x...>

list(gen_123())  # [1, 2, 3]

g = gen_123()
next(g)  # 1
next(g)  # 2
next(g)  # 3
next(g)  # StopIteration
```

### Sentence with Generator

```python
class Sentence:
    def __init__(self, text):
        self.text = text
        self.words = RE_WORD.findall(text)

    def __iter__(self):
        for word in self.words:
            yield word
        # No explicit return needed
```

Much cleaner than the classic iterator pattern!

---

## How Generators Work

```python
def gen_AB():
    print('start')
    yield 'A'
    print('continue')
    yield 'B'
    print('end.')

for c in gen_AB():
    print('-->', c)

# Output:
# start
# --> A
# continue
# --> B
# end.
```

1. Generator function body is suspended at each `yield`
2. `next()` resumes execution until next `yield`
3. When function returns, `StopIteration` is raised

---

## Lazy Generators

Use `re.finditer` instead of `re.findall` for lazy iteration:

```python
class Sentence:
    def __init__(self, text):
        self.text = text  # Don't pre-process!

    def __iter__(self):
        for match in RE_WORD.finditer(self.text):
            yield match.group()
```

Benefits:
- Lower memory usage (no list of all words)
- Faster startup (process on demand)
- Can handle infinite sequences

---

## Generator Expressions

Syntactic sugar for simple generators:

```python
# Generator expression (lazy)
gen = (x * 2 for x in range(5))

# List comprehension (eager)
lst = [x * 2 for x in range(5)]

# Sentence with generator expression
class Sentence:
    def __init__(self, text):
        self.text = text

    def __iter__(self):
        return (match.group()
                for match in RE_WORD.finditer(self.text))
```

**Rule of thumb:** If it spans more than 2 lines, use a generator function instead.

---

## iter() with a Callable

Two-argument form: `iter(callable, sentinel)`

```python
from random import randint

def d6():
    return randint(1, 6)

# Roll until we get 1
d6_iter = iter(d6, 1)
for roll in d6_iter:
    print(roll)  # Never prints 1

# Read file in blocks
with open('data.bin', 'rb') as f:
    for block in iter(lambda: f.read(64), b''):
        process(block)
```

---

## yield from

Delegate to a sub-generator:

```python
def chain(*iterables):
    for it in iterables:
        yield from it

list(chain('ABC', [1, 2, 3]))
# ['A', 'B', 'C', 1, 2, 3]
```

Equivalent to:
```python
def chain(*iterables):
    for it in iterables:
        for item in it:
            yield item
```

### Tree Traversal with yield from

```python
def tree_values(node):
    if node is not None:
        yield from tree_values(node.left)
        yield node.value
        yield from tree_values(node.right)
```

---

## Type Hints for Iterators

```python
from collections.abc import Iterator, Iterable, Generator
from typing import TypeVar

T = TypeVar('T')

def my_generator(n: int) -> Iterator[int]:
    for i in range(n):
        yield i

def count_words(text: str) -> Iterable[str]:
    return text.split()

# Full Generator type hint:
# Generator[YieldType, SendType, ReturnType]
def gen() -> Generator[int, None, str]:
    yield 1
    yield 2
    return "done"
```

---

## Standard Library Generators

### Filtering

| Function | Description |
|----------|-------------|
| `filter(pred, it)` | Items where pred is truthy |
| `itertools.filterfalse(pred, it)` | Items where pred is falsy |
| `itertools.takewhile(pred, it)` | Items until pred is false |
| `itertools.dropwhile(pred, it)` | Skip items while pred is true |
| `itertools.compress(it, selectors)` | Items where selector is truthy |
| `itertools.islice(it, stop)` | Slice of iterable |

```python
import itertools

def vowel(c):
    return c.lower() in 'aeiou'

list(filter(vowel, 'Aardvark'))      # ['A', 'a', 'a']
list(itertools.filterfalse(vowel, 'Aardvark'))  # ['r', 'd', 'v', 'r', 'k']
list(itertools.takewhile(vowel, 'Aardvark'))    # ['A', 'a']
list(itertools.islice('ABCDEF', 2, 5))          # ['C', 'D', 'E']
```

### Mapping

| Function | Description |
|----------|-------------|
| `map(func, it, ...)` | Apply func to items |
| `itertools.starmap(func, it)` | Apply func(*item) |
| `enumerate(it, start=0)` | Yield (index, item) pairs |
| `itertools.accumulate(it, func)` | Running accumulation |

```python
list(enumerate('ABC', 1))
# [(1, 'A'), (2, 'B'), (3, 'C')]

list(itertools.accumulate([1, 2, 3, 4]))
# [1, 3, 6, 10]  (running sum)

list(itertools.accumulate([1, 2, 3, 4], max))
# [1, 2, 3, 4]  (running max)
```

### Merging

| Function | Description |
|----------|-------------|
| `itertools.chain(it1, it2, ...)` | Chain iterables sequentially |
| `itertools.chain.from_iterable(it)` | Chain from iterable of iterables |
| `zip(it1, it2, ...)` | Parallel iteration (stops at shortest) |
| `itertools.zip_longest(...)` | Parallel iteration (pads shorter) |
| `itertools.product(it1, it2, ...)` | Cartesian product |

```python
list(itertools.chain('AB', [1, 2]))
# ['A', 'B', 1, 2]

list(zip('ABC', [1, 2, 3, 4]))
# [('A', 1), ('B', 2), ('C', 3)]

list(itertools.product('AB', range(2)))
# [('A', 0), ('A', 1), ('B', 0), ('B', 1)]
```

### Expanding

| Function | Description |
|----------|-------------|
| `itertools.count(start, step)` | Infinite counter |
| `itertools.cycle(it)` | Repeat iterable forever |
| `itertools.repeat(item, n)` | Repeat item n times |
| `itertools.combinations(it, r)` | r-length combinations |
| `itertools.permutations(it, r)` | r-length permutations |

```python
list(itertools.repeat('A', 3))
# ['A', 'A', 'A']

list(itertools.combinations('ABC', 2))
# [('A', 'B'), ('A', 'C'), ('B', 'C')]

list(itertools.permutations('AB', 2))
# [('A', 'B'), ('B', 'A')]
```

### Grouping

```python
import itertools

data = [('a', 1), ('a', 2), ('b', 3), ('b', 4)]

for key, group in itertools.groupby(data, key=lambda x: x[0]):
    print(key, list(group))
# a [('a', 1), ('a', 2)]
# b [('b', 3), ('b', 4)]
```

**Note:** `groupby` requires sorted input!

---

## Arithmetic Progression Generator

```python
def aritprog_gen(begin, step, end=None):
    result = type(begin + step)(begin)
    forever = end is None
    index = 0
    while forever or result < end:
        yield result
        index += 1
        result = begin + step * index

list(aritprog_gen(0, 1, 5))      # [0, 1, 2, 3, 4]
list(aritprog_gen(0, 0.5, 2))    # [0.0, 0.5, 1.0, 1.5]
```

Using itertools:
```python
import itertools

def aritprog_gen(begin, step, end=None):
    first = type(begin + step)(begin)
    ap_gen = itertools.count(first, step)
    if end is None:
        return ap_gen
    return itertools.takewhile(lambda n: n < end, ap_gen)
```

---

## Classic Coroutines (Brief)

Before `async/await`, generators could be used as coroutines with `.send()`:

```python
def averager():
    total = 0.0
    count = 0
    average = None
    while True:
        term = yield average  # Receive value via .send()
        total += term
        count += 1
        average = total / count

coro = averager()
next(coro)         # Prime the coroutine
coro.send(10)      # 10.0
coro.send(20)      # 15.0
coro.send(30)      # 20.0
```

**Note:** Classic coroutines are mostly superseded by native coroutines (`async def`).

---

## Quick Reference

```python
# Generator function
def gen():
    yield 1
    yield 2

# Generator expression
g = (x * 2 for x in items)

# Delegate to sub-generator
yield from other_generator

# iter() with callable
iter(callable, sentinel)

# Check if iterable
from collections.abc import Iterable
isinstance(obj, Iterable)

# Better check (handles __getitem__)
try:
    iter(obj)
except TypeError:
    print("Not iterable")

# Common itertools
import itertools
itertools.chain(it1, it2)
itertools.count(start, step)
itertools.cycle(it)
itertools.takewhile(pred, it)
itertools.dropwhile(pred, it)
itertools.groupby(it, key)
itertools.islice(it, start, stop, step)
itertools.accumulate(it, func)
itertools.product(it1, it2)
itertools.combinations(it, r)
itertools.permutations(it, r)
```

---

## Summary

1. **Iterables** provide iterators via `__iter__` (or `__getitem__`)
2. **Iterators** yield items via `__next__`, raise `StopIteration` when done
3. **Generator functions** use `yield` to create generators automatically
4. **Generator expressions** are compact syntax for simple generators
5. **yield from** delegates to sub-generators
6. **Lazy evaluation** saves memory and enables infinite sequences
7. **itertools** provides powerful generator utilities
8. **Classic coroutines** used `.send()` but are now superseded by `async/await`
9. Use generator functions over manual iterator classes
10. Check iterability with `iter(obj)`, not `isinstance(obj, Iterable)`
