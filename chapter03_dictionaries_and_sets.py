"""
Chapter 3: Dictionaries and Sets - Exercises
=============================================

Complete each exercise by replacing the `None` or `...` placeholders.
Run this file to check your answers with the assertions.
"""

from collections import defaultdict, Counter, OrderedDict, ChainMap

# =============================================================================
# Exercise 1: Dict Comprehensions
# =============================================================================
# Use dict comprehensions to transform data

# TODO: Create a dict mapping numbers 1-5 to their squares
# {1: 1, 2: 4, 3: 9, 4: 16, 5: 25}
squares = None

# TODO: Invert this dict (swap keys and values)
original = {'a': 1, 'b': 2, 'c': 3}
inverted = None  # {1: 'a', 2: 'b', 3: 'c'}

# TODO: Filter to keep only items where value > 1
filtered = None  # {2: 'b', 3: 'c'}

assert squares == {1: 1, 2: 4, 3: 9, 4: 16, 5: 25}
assert inverted == {1: 'a', 2: 'b', 3: 'c'}
assert filtered == {2: 'b', 3: 'c'}
print("✓ Exercise 1 passed: Dict Comprehensions")


# =============================================================================
# Exercise 2: Dict Merging (Python 3.9+)
# =============================================================================
# Merge dictionaries with priority

defaults = {'color': 'blue', 'size': 'medium', 'count': 1}
user_settings = {'color': 'red', 'font': 'Arial'}

# TODO: Merge so user_settings override defaults
# Expected: {'color': 'red', 'size': 'medium', 'count': 1, 'font': 'Arial'}
merged = None

assert merged == {'color': 'red', 'size': 'medium', 'count': 1, 'font': 'Arial'}
print("✓ Exercise 2 passed: Dict Merging")


# =============================================================================
# Exercise 3: setdefault Pattern
# =============================================================================
# Use setdefault to build a word index

text = "the quick brown fox jumps over the lazy dog"
words = text.split()

# TODO: Build an index: word -> list of positions where it appears
# Use setdefault to avoid redundant lookups
# Expected: {'the': [0, 6], 'quick': [1], 'brown': [2], ...}
index = {}
# Your code here - iterate over words with enumerate
...

assert index['the'] == [0, 6]
assert index['quick'] == [1]
assert index['dog'] == [8]
print("✓ Exercise 3 passed: setdefault Pattern")


# =============================================================================
# Exercise 4: defaultdict for Grouping
# =============================================================================
# Group items by a key

students = [
    ('Alice', 'A'),
    ('Bob', 'B'),
    ('Charlie', 'A'),
    ('Diana', 'C'),
    ('Eve', 'B'),
    ('Frank', 'A'),
]

# TODO: Group students by grade using defaultdict(list)
# Expected: {'A': ['Alice', 'Charlie', 'Frank'], 'B': ['Bob', 'Eve'], 'C': ['Diana']}
by_grade = None

assert by_grade['A'] == ['Alice', 'Charlie', 'Frank']
assert by_grade['B'] == ['Bob', 'Eve']
assert by_grade['C'] == ['Diana']
print("✓ Exercise 4 passed: defaultdict for Grouping")


# =============================================================================
# Exercise 5: Counter
# =============================================================================
# Count occurrences and perform multiset operations

text = "abracadabra"

# TODO: Count character occurrences
char_counts = None

# TODO: Get the 3 most common characters as a list of tuples
top_3 = None  # [('a', 5), ('b', 2), ('r', 2)]

# TODO: What count does 'z' have? (missing keys)
z_count = None

# Counter arithmetic
c1 = Counter(a=3, b=1, c=2)
c2 = Counter(a=1, b=2, c=1)

# TODO: Add the counters
added = None  # Counter({'a': 4, 'b': 3, 'c': 3})

# TODO: Subtract c2 from c1 (only positive counts remain)
subtracted = None  # Counter({'a': 2, 'c': 1})

assert char_counts['a'] == 5
assert char_counts['b'] == 2
assert top_3 == [('a', 5), ('b', 2), ('r', 2)]
assert z_count == 0
assert added == Counter({'a': 4, 'b': 3, 'c': 3})
assert subtracted == Counter({'a': 2, 'c': 1})
print("✓ Exercise 5 passed: Counter")


# =============================================================================
# Exercise 6: OrderedDict
# =============================================================================
# Use OrderedDict for LRU-like behavior

# TODO: Create an OrderedDict and demonstrate move_to_end
cache = OrderedDict()
cache['a'] = 1
cache['b'] = 2
cache['c'] = 3

# TODO: Access 'a' and move it to the end (simulating LRU cache access)
# After this, order should be: b, c, a
...

# TODO: Get the keys as a list
keys_after_move = None

# TODO: Pop the least recently used item (first item)
# Hint: use popitem(last=False)
lru_item = None  # Should be ('b', 2)

assert keys_after_move == ['b', 'c', 'a']
assert lru_item == ('b', 2)
print("✓ Exercise 6 passed: OrderedDict")


# =============================================================================
# Exercise 7: ChainMap
# =============================================================================
# Use ChainMap for layered configuration

cli_args = {'verbose': True}
env_vars = {'timeout': '30', 'verbose': False}
defaults = {'timeout': '10', 'retries': '3', 'verbose': False}

# TODO: Create a ChainMap where cli_args has highest priority,
# then env_vars, then defaults
config = None

# TODO: What values do we get?
verbose_value = None   # From cli_args (True)
timeout_value = None   # From env_vars ('30')
retries_value = None   # From defaults ('3')

assert verbose_value == True
assert timeout_value == '30'
assert retries_value == '3'
print("✓ Exercise 7 passed: ChainMap")


# =============================================================================
# Exercise 8: Set Operations
# =============================================================================
# Perform set operations

python_devs = {'Alice', 'Bob', 'Charlie', 'Diana'}
java_devs = {'Bob', 'Diana', 'Eve', 'Frank'}

# TODO: Developers who know both Python AND Java
both = None

# TODO: Developers who know Python OR Java (or both)
either = None

# TODO: Developers who know Python but NOT Java
python_only = None

# TODO: Developers who know exactly one language (not both)
one_only = None

assert both == {'Bob', 'Diana'}
assert either == {'Alice', 'Bob', 'Charlie', 'Diana', 'Eve', 'Frank'}
assert python_only == {'Alice', 'Charlie'}
assert one_only == {'Alice', 'Charlie', 'Eve', 'Frank'}
print("✓ Exercise 8 passed: Set Operations")


# =============================================================================
# Exercise 9: Set Comparisons
# =============================================================================
# Check subset/superset relationships

small = {1, 2}
medium = {1, 2, 3, 4}
large = {1, 2, 3, 4, 5, 6}
other = {7, 8}

# TODO: Is small a subset of medium?
is_subset = None

# TODO: Is large a superset of medium?
is_superset = None

# TODO: Are small and other disjoint (no common elements)?
is_disjoint = None

# TODO: Is small a proper subset of medium (subset but not equal)?
is_proper_subset = None

assert is_subset == True
assert is_superset == True
assert is_disjoint == True
assert is_proper_subset == True
print("✓ Exercise 9 passed: Set Comparisons")


# =============================================================================
# Exercise 10: Removing Duplicates Preserving Order
# =============================================================================
# Remove duplicates while keeping the first occurrence order

items = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]

# TODO: Remove duplicates, keep order of first occurrence
# Expected: [3, 1, 4, 5, 9, 2, 6]
# Hint: Use dict.fromkeys()
unique = None

assert unique == [3, 1, 4, 5, 9, 2, 6]
print("✓ Exercise 10 passed: Remove Duplicates Preserving Order")


# =============================================================================
# Exercise 11: Dict Views for Set Operations
# =============================================================================
# Use dict views to find common/different keys

dict1 = {'a': 1, 'b': 2, 'c': 3}
dict2 = {'b': 2, 'c': 30, 'd': 4}

# TODO: Find keys that are in both dicts
common_keys = None  # {'b', 'c'}

# TODO: Find keys only in dict1
only_in_dict1 = None  # {'a'}

# TODO: Find key-value pairs that are identical in both dicts
same_items = None  # {('b', 2)}

assert common_keys == {'b', 'c'}
assert only_in_dict1 == {'a'}
assert same_items == {('b', 2)}
print("✓ Exercise 11 passed: Dict Views for Set Operations")


# =============================================================================
# Exercise 12: Practical - Word Frequency Analysis
# =============================================================================
# Analyze word frequencies in text

paragraph = """
Python is a programming language. Python is popular.
Programming in Python is fun. Python makes programming easy.
"""

def analyze_words(text):
    """
    Analyze word frequencies in text.

    Returns a dict with:
    - 'total_words': total word count
    - 'unique_words': number of unique words
    - 'top_3': list of (word, count) for 3 most common words
    - 'word_lengths': dict mapping word length to list of words

    TODO: Implement this function
    """
    # Normalize: lowercase and split
    words = text.lower().split()

    # Remove punctuation from words
    words = [w.strip('.,!?') for w in words]

    result = {
        'total_words': None,
        'unique_words': None,
        'top_3': None,
        'word_lengths': None,
    }

    # TODO: Fill in the result dict
    ...

    return result


analysis = analyze_words(paragraph)

assert analysis['total_words'] == 18
assert analysis['unique_words'] == 9
assert analysis['top_3'][0] == ('python', 4)  # Most common word
assert 6 in analysis['word_lengths']  # Words of length 6
assert 'python' in analysis['word_lengths'][6]

print("✓ Exercise 12 passed: Word Frequency Analysis")


# =============================================================================
# Exercise 13: Practical - Nested defaultdict
# =============================================================================
# Create a nested data structure using nested defaultdicts

# TODO: Create a function that returns a defaultdict of defaultdicts
# So we can do: data[key1][key2] = value without KeyError
def nested_dict():
    """Return a defaultdict that creates defaultdicts on missing keys."""
    ...
    pass


data = nested_dict()
data['users']['alice']['email'] = 'alice@example.com'
data['users']['bob']['email'] = 'bob@example.com'
data['users']['alice']['age'] = 30

assert data['users']['alice']['email'] == 'alice@example.com'
assert data['users']['bob']['email'] == 'bob@example.com'
assert data['users']['alice']['age'] == 30

# Accessing missing keys should not raise KeyError
try:
    _ = data['missing']['key']['deep']
    missing_access_ok = True
except KeyError:
    missing_access_ok = False

assert missing_access_ok, "Nested access should not raise KeyError"
print("✓ Exercise 13 passed: Nested defaultdict")


# =============================================================================
# Exercise 14: Practical - Immutable Configuration
# =============================================================================
# Create a configuration system using frozenset

# Configuration options that can be combined
OPTION_DEBUG = frozenset({'debug'})
OPTION_VERBOSE = frozenset({'verbose'})
OPTION_STRICT = frozenset({'strict'})

# TODO: Create a combined configuration with debug and verbose enabled
# Use set union
config = None

# TODO: Check if debug is enabled (using set intersection or subset check)
debug_enabled = None  # True or False

# TODO: Create a function that validates if a config is a subset of valid options
VALID_OPTIONS = frozenset({'debug', 'verbose', 'strict', 'quiet', 'fast'})

def is_valid_config(config):
    """Return True if all options in config are valid."""
    # TODO: Implement using subset check
    ...
    pass


assert config == frozenset({'debug', 'verbose'})
assert debug_enabled == True
assert is_valid_config(config) == True
assert is_valid_config(frozenset({'debug', 'invalid'})) == False
print("✓ Exercise 14 passed: Immutable Configuration")


# =============================================================================
# Exercise 15: Practical - Inverted Index
# =============================================================================
# Build an inverted index for document search

documents = {
    'doc1': 'Python is a programming language',
    'doc2': 'Java is also a programming language',
    'doc3': 'Python and Java are popular',
}

def build_inverted_index(docs):
    """
    Build an inverted index: word -> set of doc_ids containing that word.

    TODO: Implement using defaultdict(set)
    """
    ...
    pass


def search(index, *terms):
    """
    Find documents containing ALL search terms.

    TODO: Implement using set intersection
    """
    ...
    pass


index = build_inverted_index(documents)

# Test the index
assert 'doc1' in index['python']
assert 'doc3' in index['python']
assert 'doc2' not in index['python']

# Test search
assert search(index, 'python') == {'doc1', 'doc3'}
assert search(index, 'programming', 'language') == {'doc1', 'doc2'}
assert search(index, 'python', 'java') == {'doc3'}
assert search(index, 'nonexistent') == set()

print("✓ Exercise 15 passed: Inverted Index")


# =============================================================================
# All exercises completed!
# =============================================================================
print("\n" + "=" * 60)
print("🎉 Congratulations! All Chapter 3 exercises passed!")
print("=" * 60)
