# Python Dictionaries and Sets - Practical Memo

## Quick Comparison: Dict Types

| Type | Ordered | Default Values | Use Case |
|------|---------|----------------|----------|
| `dict` | Yes (3.7+) | No | General purpose |
| `defaultdict` | Yes | Yes (via factory) | Auto-create missing keys |
| `OrderedDict` | Yes | No | Reordering, equality cares about order |
| `Counter` | Yes | 0 | Counting, multisets |
| `ChainMap` | Yes | No | Layered lookups (scopes, configs) |
| `UserDict` | Yes | No | Base for custom dict subclasses |

## When to Use Which

| Use Case | Best Choice |
|----------|-------------|
| General key-value storage | `dict` |
| Grouping items (word → list of positions) | `defaultdict(list)` |
| Counting occurrences | `Counter` |
| Need to reorder keys / move_to_end | `OrderedDict` |
| Layered configs (defaults + overrides) | `ChainMap` |
| Custom dict with modified behavior | Subclass `UserDict` |
| Immutable set | `frozenset` |
| Unique items with fast lookup | `set` |
| Set operations on multiple collections | `set` with `|`, `&`, `-` |

---

## 1. Modern Dict Syntax

### Dict Comprehensions

```python
# Basic comprehension
squares = {x: x**2 for x in range(6)}
# {0: 0, 1: 1, 2: 4, 3: 9, 4: 16, 5: 25}

# Swap keys and values
original = {'a': 1, 'b': 2, 'c': 3}
inverted = {v: k for k, v in original.items()}
# {1: 'a', 2: 'b', 3: 'c'}

# With filtering
even_squares = {x: x**2 for x in range(10) if x % 2 == 0}
# {0: 0, 2: 4, 4: 16, 6: 36, 8: 64}
```

### Unpacking with `**`

```python
# Merge dicts in function call
def show(**kwargs):
    return kwargs

result = show(**{'a': 1}, b=2, **{'c': 3})
# {'a': 1, 'b': 2, 'c': 3}

# Merge in dict literal (later values win)
merged = {'a': 0, **{'a': 1, 'b': 2}, **{'c': 3}}
# {'a': 1, 'b': 2, 'c': 3}
```

### Merge with `|` (Python 3.9+)

```python
d1 = {'a': 1, 'b': 2}
d2 = {'b': 3, 'c': 4}

# Create new merged dict (d2 values win on conflict)
merged = d1 | d2
# {'a': 1, 'b': 3, 'c': 4}

# Update in place
d1 |= d2
# d1 is now {'a': 1, 'b': 3, 'c': 4}
```

---

## 2. Essential Dict Methods

```python
d = {'a': 1, 'b': 2}

# Safe access with default
d.get('c', 0)           # 0 (key missing, return default)
d.get('a', 0)           # 1 (key exists)

# setdefault: get or set-then-get
d.setdefault('c', 3)    # 3 (sets d['c'] = 3, returns it)
d.setdefault('a', 99)   # 1 (key exists, returns existing value)

# pop with default (no KeyError)
d.pop('x', None)        # None (key missing)
d.pop('a')              # 1 (removes and returns)

# Update from another dict or iterable
d.update({'x': 10, 'y': 20})
d.update([('p', 1), ('q', 2)])  # From key-value pairs
d.update(m=100, n=200)          # From kwargs
```

### `setdefault` Pattern (Avoid Redundant Lookups)

```python
# BAD: Three lookups for missing key
if word not in index:
    index[word] = []
index[word].append(location)

# GOOD: One lookup
index.setdefault(word, []).append(location)
```

---

## 3. `defaultdict`

**Best for:** Auto-creating default values for missing keys.

```python
from collections import defaultdict

# List as default (grouping)
index = defaultdict(list)
index['python'].append('page 1')
index['python'].append('page 5')
# {'python': ['page 1', 'page 5']}

# Int as default (counting)
counts = defaultdict(int)
for char in 'abracadabra':
    counts[char] += 1
# {'a': 5, 'b': 2, 'r': 2, 'c': 1, 'd': 1}

# Set as default (unique values)
tags = defaultdict(set)
tags['article1'].add('python')
tags['article1'].add('python')  # No duplicate
# {'article1': {'python'}}

# Custom factory
def make_default():
    return {'count': 0, 'items': []}

data = defaultdict(make_default)
data['user1']['count'] += 1
```

---

## 4. `Counter`

**Best for:** Counting, multiset operations, most common elements.

```python
from collections import Counter

# Count from iterable
c = Counter('abracadabra')
# Counter({'a': 5, 'b': 2, 'r': 2, 'c': 1, 'd': 1})

# Most common
c.most_common(2)  # [('a', 5), ('b', 2)]

# Missing keys return 0 (not KeyError)
c['z']  # 0

# Arithmetic operations
c1 = Counter(a=3, b=1)
c2 = Counter(a=1, b=2)
c1 + c2  # Counter({'a': 4, 'b': 3})
c1 - c2  # Counter({'a': 2}) - only positive counts
c1 & c2  # Counter({'a': 1, 'b': 1}) - min of each
c1 | c2  # Counter({'a': 3, 'b': 2}) - max of each

# Total count (Python 3.10+)
c.total()  # 11

# Update counts
c.update('aaa')  # Add counts from iterable
c.update({'a': 10})  # Add from dict

# Elements iterator (repeats by count)
list(c.elements())  # ['a', 'a', 'a', 'a', 'a', 'b', 'b', ...]
```

---

## 5. `OrderedDict`

**Best for:** When order matters for equality, or need `move_to_end()`.

```python
from collections import OrderedDict

# Regular dict keeps insertion order (Python 3.7+)
# But OrderedDict equality considers order:
od1 = OrderedDict([('a', 1), ('b', 2)])
od2 = OrderedDict([('b', 2), ('a', 1)])
od1 == od2  # False (order differs)

d1 = {'a': 1, 'b': 2}
d2 = {'b': 2, 'a': 1}
d1 == d2  # True (order ignored for dict)

# move_to_end (LRU cache pattern)
od = OrderedDict([('a', 1), ('b', 2), ('c', 3)])
od.move_to_end('a')        # Move to end
# OrderedDict([('b', 2), ('c', 3), ('a', 1)])
od.move_to_end('c', last=False)  # Move to beginning
# OrderedDict([('c', 3), ('b', 2), ('a', 1)])

# popitem from either end
od.popitem()               # ('a', 1) - from end (LIFO)
od.popitem(last=False)     # ('c', 3) - from start (FIFO)
```

---

## 6. `ChainMap`

**Best for:** Layered lookups without copying (configs, scopes).

```python
from collections import ChainMap

defaults = {'theme': 'light', 'language': 'en', 'timeout': 30}
user_prefs = {'theme': 'dark'}
cli_args = {'timeout': 60}

# Lookup searches maps in order (first wins)
config = ChainMap(cli_args, user_prefs, defaults)
config['theme']     # 'dark' (from user_prefs)
config['timeout']   # 60 (from cli_args)
config['language']  # 'en' (from defaults)

# Updates only affect first map
config['new_key'] = 'value'  # Added to cli_args

# Add a new scope (child context)
local_scope = config.new_child({'timeout': 10})
local_scope['timeout']  # 10
config['timeout']       # 60 (unchanged)

# Get parent chain
local_scope.parents  # ChainMap without first map
```

---

## 7. Subclassing with `UserDict`

**Best for:** Custom dict behavior (always use this, not `dict`).

```python
from collections import UserDict

class StrKeyDict(UserDict):
    """Dict that converts keys to str on lookup and storage."""

    def __missing__(self, key):
        if isinstance(key, str):
            raise KeyError(key)
        return self[str(key)]

    def __contains__(self, key):
        return str(key) in self.data

    def __setitem__(self, key, value):
        self.data[str(key)] = value

# Usage
d = StrKeyDict()
d[1] = 'one'
d['1']  # 'one'
d[1]    # 'one'
1 in d  # True
```

---

## 8. Sets

### Basic Operations

```python
s = {1, 2, 3}
s = set([1, 2, 3])  # From iterable
empty = set()       # NOT {} (that's a dict)

# Add/remove
s.add(4)
s.discard(2)    # No error if missing
s.remove(3)     # KeyError if missing
s.pop()         # Remove arbitrary element

# Membership (O(1) average)
2 in s          # True
```

### Set Comprehensions

```python
{x**2 for x in range(5)}  # {0, 1, 4, 9, 16}
{c.lower() for c in 'Hello World' if c.isalpha()}  # {'h', 'e', 'l', 'o', 'w', 'r', 'd'}
```

### Set Operations

```python
a = {1, 2, 3, 4}
b = {3, 4, 5, 6}

# Union (all elements)
a | b           # {1, 2, 3, 4, 5, 6}
a.union(b)

# Intersection (common elements)
a & b           # {3, 4}
a.intersection(b)

# Difference (in a but not in b)
a - b           # {1, 2}
a.difference(b)

# Symmetric difference (in either, not both)
a ^ b           # {1, 2, 5, 6}
a.symmetric_difference(b)

# In-place versions
a |= b          # a.update(b)
a &= b          # a.intersection_update(b)
a -= b          # a.difference_update(b)
a ^= b          # a.symmetric_difference_update(b)
```

### Set Comparisons

```python
a = {1, 2, 3}
b = {1, 2, 3, 4, 5}

a <= b          # True (a is subset of b)
a < b           # True (a is proper subset)
b >= a          # True (b is superset of a)
a.issubset(b)   # True
b.issuperset(a) # True
a.isdisjoint({4, 5})  # True (no common elements)
```

### `frozenset` (Immutable)

```python
fs = frozenset([1, 2, 3])

# Can be used as dict key or set element
d = {fs: 'value'}
s = {fs, frozenset([4, 5])}

# Same operations, returns new frozenset
fs | {4}  # frozenset({1, 2, 3, 4})
```

---

## 9. Dict Views

```python
d = {'a': 1, 'b': 2, 'c': 3}

# Views are dynamic (reflect changes)
keys = d.keys()
values = d.values()
items = d.items()

d['d'] = 4
list(keys)  # ['a', 'b', 'c', 'd']

# Set operations on keys and items views
d1 = {'a': 1, 'b': 2, 'c': 3}
d2 = {'b': 2, 'c': 30, 'd': 4}

d1.keys() & d2.keys()   # {'b', 'c'} - common keys
d1.keys() - d2.keys()   # {'a'} - keys only in d1
d1.items() & d2.items() # {('b', 2)} - same key-value pairs
```

---

## Common Patterns

### Grouping with `defaultdict`

```python
from collections import defaultdict

records = [
    ('sales', 100), ('marketing', 50), ('sales', 200), ('engineering', 300)
]

by_dept = defaultdict(list)
for dept, amount in records:
    by_dept[dept].append(amount)
# {'sales': [100, 200], 'marketing': [50], 'engineering': [300]}
```

### Inverting a Dict

```python
original = {'a': 1, 'b': 2, 'c': 3}
inverted = {v: k for k, v in original.items()}
# {1: 'a', 2: 'b', 3: 'c'}

# Handle duplicate values (keep all keys)
from collections import defaultdict
multi = defaultdict(list)
for k, v in original.items():
    multi[v].append(k)
```

### Merge Dicts (Priority Order)

```python
# Python 3.9+
defaults = {'a': 1, 'b': 2}
overrides = {'b': 3, 'c': 4}
final = defaults | overrides  # {'a': 1, 'b': 3, 'c': 4}

# Python 3.5+
final = {**defaults, **overrides}
```

### Remove Duplicates Preserving Order

```python
items = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
unique = list(dict.fromkeys(items))
# [3, 1, 4, 5, 9, 2, 6]
```

### Filter Dict

```python
d = {'a': 1, 'b': 2, 'c': 3, 'd': 4}

# Keep only even values
{k: v for k, v in d.items() if v % 2 == 0}
# {'b': 2, 'd': 4}

# Keep only specific keys
keys_to_keep = {'a', 'c'}
{k: v for k, v in d.items() if k in keys_to_keep}
# {'a': 1, 'c': 3}
```

---

## Performance Notes

| Operation | dict | set |
|-----------|------|-----|
| `x in d` | O(1) avg | O(1) avg |
| `d[key]` | O(1) avg | N/A |
| `d.get(key)` | O(1) avg | N/A |
| Add/remove | O(1) avg | O(1) avg |
| Iteration | O(n) | O(n) |

- **Keys must be hashable** (immutable: str, int, tuple of hashables, frozenset)
- **Dict preserves insertion order** (Python 3.7+, guaranteed)
- **Memory:** dicts are optimized; sets use similar hash table structure
