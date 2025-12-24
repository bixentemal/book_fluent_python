"""
Chapter 17: Iterators, Generators, and Classic Coroutines - Exercises
======================================================================

Practice implementing iterators, generator functions, generator
expressions, and using itertools for data processing.

Run this file to check your implementations.
"""

import re
import itertools
from collections.abc import Iterator, Iterable
from typing import Any

RE_WORD = re.compile(r'\w+')

# =============================================================================
# Exercise 1: Classic Iterator Pattern
# =============================================================================
# Implement a Sentence class with a separate iterator class.


class SentenceIterator:
    """Iterator for Sentence class."""

    def __init__(self, words: list[str]):
        self.words = words
        self.index = 0

    def __next__(self) -> str:
        # TODO: Return the word at self.index
        # TODO: Raise StopIteration if index is out of bounds
        # TODO: Increment self.index
        pass

    def __iter__(self) -> "SentenceIterator":
        return self


class SentenceV1:
    """Sentence using classic iterator pattern."""

    def __init__(self, text: str):
        self.text = text
        self.words = RE_WORD.findall(text)

    def __iter__(self) -> SentenceIterator:
        # TODO: Return a SentenceIterator for self.words
        pass


# Test Exercise 1
s1 = SentenceV1("The quick brown fox")
words = list(s1)
assert words == ["The", "quick", "brown", "fox"]

# Should support multiple independent iterations
iter1 = iter(s1)
iter2 = iter(s1)
assert next(iter1) == "The"
assert next(iter1) == "quick"
assert next(iter2) == "The"  # Independent!

print("    Exercise 1 passed: Classic iterator pattern")


# =============================================================================
# Exercise 2: Generator Function for Iteration
# =============================================================================
# Implement Sentence using a generator function.


class SentenceV2:
    """Sentence using generator function."""

    def __init__(self, text: str):
        self.text = text
        self.words = RE_WORD.findall(text)

    def __iter__(self):
        # TODO: Use a for loop and yield to iterate over self.words
        pass


# Test Exercise 2
s2 = SentenceV2("Hello world from Python")
assert list(s2) == ["Hello", "world", "from", "Python"]
assert list(s2) == ["Hello", "world", "from", "Python"]  # Repeatable

print("    Exercise 2 passed: Generator function")


# =============================================================================
# Exercise 3: Lazy Generator with finditer
# =============================================================================
# Implement a lazy Sentence that doesn't pre-compute all words.


class SentenceV3:
    """Lazy Sentence using re.finditer."""

    def __init__(self, text: str):
        self.text = text
        # Don't store words list!

    def __iter__(self):
        # TODO: Use RE_WORD.finditer(self.text)
        # TODO: yield match.group() for each match
        pass


# Test Exercise 3
s3 = SentenceV3("Lazy evaluation saves memory")
assert list(s3) == ["Lazy", "evaluation", "saves", "memory"]

print("    Exercise 3 passed: Lazy generator with finditer")


# =============================================================================
# Exercise 4: Generator Expression
# =============================================================================
# Implement Sentence using a generator expression.


class SentenceV4:
    """Sentence using generator expression."""

    def __init__(self, text: str):
        self.text = text

    def __iter__(self):
        # TODO: Return a generator expression that yields match.group()
        # for each match in RE_WORD.finditer(self.text)
        pass


# Test Exercise 4
s4 = SentenceV4("Generator expressions are concise")
assert list(s4) == ["Generator", "expressions", "are", "concise"]

print("    Exercise 4 passed: Generator expression")


# =============================================================================
# Exercise 5: Simple Generator Function
# =============================================================================
# Write a generator function that yields squares of numbers.


def squares(n: int):
    """Yield squares from 0 to n-1."""
    # TODO: Yield i*i for i in range(n)
    pass


# Test Exercise 5
assert list(squares(5)) == [0, 1, 4, 9, 16]
assert list(squares(0)) == []

print("    Exercise 5 passed: Simple generator function")


# =============================================================================
# Exercise 6: Fibonacci Generator
# =============================================================================
# Write a generator that yields Fibonacci numbers.


def fibonacci(limit: int):
    """Yield Fibonacci numbers less than limit."""
    # TODO: Start with a=0, b=1
    # TODO: While a < limit, yield a and update a, b = b, a+b
    pass


# Test Exercise 6
assert list(fibonacci(10)) == [0, 1, 1, 2, 3, 5, 8]
assert list(fibonacci(100)) == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]

print("    Exercise 6 passed: Fibonacci generator")


# =============================================================================
# Exercise 7: yield from
# =============================================================================
# Use yield from to flatten nested iterables.


def flatten(nested):
    """Flatten one level of nesting."""
    # TODO: For each item in nested, yield from item
    pass


# Test Exercise 7
nested = [[1, 2], [3, 4, 5], [6]]
assert list(flatten(nested)) == [1, 2, 3, 4, 5, 6]

nested_str = ["abc", "de", "f"]
assert list(flatten(nested_str)) == ['a', 'b', 'c', 'd', 'e', 'f']

print("    Exercise 7 passed: yield from")


# =============================================================================
# Exercise 8: Deep Flatten with yield from
# =============================================================================
# Recursively flatten arbitrarily nested iterables.


def deep_flatten(nested):
    """Recursively flatten nested iterables (except strings)."""
    # TODO: For each item in nested:
    #   - If item is iterable (but not str), yield from deep_flatten(item)
    #   - Otherwise yield item
    # Hint: Use isinstance(item, Iterable) and not isinstance(item, str)
    pass


# Test Exercise 8
deep = [1, [2, [3, 4], 5], [6, [7, 8]]]
assert list(deep_flatten(deep)) == [1, 2, 3, 4, 5, 6, 7, 8]

mixed = [1, "ab", [2, ["cd", 3]]]
assert list(deep_flatten(mixed)) == [1, "ab", 2, "cd", 3]

print("    Exercise 8 passed: Deep flatten")


# =============================================================================
# Exercise 9: Arithmetic Progression Generator
# =============================================================================
# Create a generator for arithmetic progressions.


def aritprog(begin, step, end=None):
    """Generate arithmetic progression.

    If end is None, generates infinite sequence.
    """
    # TODO: Compute result type from begin + step
    # TODO: Generate values while result < end (or forever if end is None)
    # Use: result = begin + step * index to avoid floating point drift
    pass


# Test Exercise 9
assert list(aritprog(0, 1, 5)) == [0, 1, 2, 3, 4]
assert list(aritprog(1, 0.5, 3)) == [1.0, 1.5, 2.0, 2.5]
assert list(aritprog(0, 2, 10)) == [0, 2, 4, 6, 8]

# Test infinite (take first 5)
infinite = aritprog(0, 1)
first_five = [next(infinite) for _ in range(5)]
assert first_five == [0, 1, 2, 3, 4]

print("    Exercise 9 passed: Arithmetic progression")


# =============================================================================
# Exercise 10: Using itertools.takewhile and count
# =============================================================================
# Reimplement arithmetic progression using itertools.


def aritprog_itertools(begin, step, end=None):
    """Arithmetic progression using itertools."""
    # TODO: Use itertools.count(begin, step)
    # TODO: If end is not None, use itertools.takewhile
    pass


# Test Exercise 10
assert list(aritprog_itertools(0, 1, 5)) == [0, 1, 2, 3, 4]
assert list(aritprog_itertools(1, 0.5, 3)) == [1.0, 1.5, 2.0, 2.5]

print("    Exercise 10 passed: itertools arithmetic progression")


# =============================================================================
# Exercise 11: Filter with itertools
# =============================================================================
# Use itertools filtering functions.


def vowels_only(text: str) -> list[str]:
    """Return only vowels from text using filter."""
    # TODO: Use filter() with a lambda that checks if char is a vowel
    pass


def consonants_only(text: str) -> list[str]:
    """Return only consonants using itertools.filterfalse."""
    # TODO: Use itertools.filterfalse with same vowel check
    pass


def take_until_space(text: str) -> list[str]:
    """Take characters until first space using itertools.takewhile."""
    # TODO: Use itertools.takewhile
    pass


# Test Exercise 11
assert vowels_only("Hello World") == ['e', 'o', 'o']
assert consonants_only("Hello") == ['H', 'l', 'l']
assert take_until_space("Hello World") == ['H', 'e', 'l', 'l', 'o']

print("    Exercise 11 passed: itertools filtering")


# =============================================================================
# Exercise 12: Mapping with itertools
# =============================================================================
# Use itertools mapping functions.


def running_sum(numbers: list[int]) -> list[int]:
    """Calculate running sum using itertools.accumulate."""
    # TODO: Use itertools.accumulate
    pass


def running_max(numbers: list[int]) -> list[int]:
    """Calculate running maximum using itertools.accumulate."""
    # TODO: Use itertools.accumulate with max function
    pass


def multiply_pairs(pairs: list[tuple[int, int]]) -> list[int]:
    """Multiply pairs using itertools.starmap."""
    # TODO: Use itertools.starmap with operator.mul or lambda
    pass


# Test Exercise 12
assert running_sum([1, 2, 3, 4]) == [1, 3, 6, 10]
assert running_max([3, 1, 4, 1, 5]) == [3, 3, 4, 4, 5]
assert multiply_pairs([(2, 3), (4, 5), (6, 7)]) == [6, 20, 42]

print("    Exercise 12 passed: itertools mapping")


# =============================================================================
# Exercise 13: Merging with itertools
# =============================================================================
# Use itertools merging functions.


def interleave(*iterables):
    """Interleave items from multiple iterables."""
    # TODO: Use zip() and flatten the result
    # Or use itertools.chain.from_iterable with zip
    pass


def cartesian_product(letters: str, numbers: range) -> list[tuple]:
    """Return Cartesian product using itertools.product."""
    # TODO: Use itertools.product
    pass


# Test Exercise 13
assert list(interleave("AB", "12")) == ['A', '1', 'B', '2']
assert list(interleave([1, 2], [3, 4], [5, 6])) == [1, 3, 5, 2, 4, 6]
assert cartesian_product("AB", range(2)) == [
    ('A', 0), ('A', 1), ('B', 0), ('B', 1)
]

print("    Exercise 13 passed: itertools merging")


# =============================================================================
# Exercise 14: Grouping with itertools.groupby
# =============================================================================
# Use itertools.groupby to group consecutive items.


def group_by_length(words: list[str]) -> dict[int, list[str]]:
    """Group words by length (input must be sorted by length)."""
    # TODO: Sort words by length first
    # TODO: Use itertools.groupby with len as key
    # TODO: Return dict mapping length to list of words
    pass


def run_length_encode(data: str) -> list[tuple[str, int]]:
    """Run-length encode a string."""
    # TODO: Use itertools.groupby to group consecutive chars
    # TODO: Return list of (char, count) tuples
    pass


# Test Exercise 14
words = ["a", "to", "hi", "the", "cat", "dogs"]
grouped = group_by_length(words)
assert grouped[1] == ["a"]
assert grouped[2] == ["to", "hi"]
assert grouped[3] == ["the", "cat"]
assert grouped[4] == ["dogs"]

assert run_length_encode("aaabbc") == [('a', 3), ('b', 2), ('c', 1)]
assert run_length_encode("aabbaa") == [('a', 2), ('b', 2), ('a', 2)]

print("    Exercise 14 passed: itertools.groupby")


# =============================================================================
# Exercise 15: iter() with Callable
# =============================================================================
# Use two-argument iter() with a callable and sentinel.

call_count = 0


def counter():
    """Function that returns incrementing numbers."""
    global call_count
    call_count += 1
    return call_count


def iter_until_sentinel(func, sentinel) -> list:
    """Collect values from func until sentinel is returned."""
    # TODO: Use iter(func, sentinel) and convert to list
    pass


# Test Exercise 15
call_count = 0
result = iter_until_sentinel(counter, 5)
assert result == [1, 2, 3, 4]  # Stops before returning 5

print("    Exercise 15 passed: iter() with callable")


# =============================================================================
print("\n" + "=" * 60)
print("Congratulations! All Chapter 17 exercises completed!")
print("=" * 60)
