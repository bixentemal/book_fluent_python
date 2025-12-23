"""
Chapter 8: Type Hints in Functions - Exercises
===============================================

Complete each exercise by replacing the `None` or `...` placeholders.
Run this file to check your answers with the assertions.

Note: These exercises focus on writing correct type hints.
The functions themselves are simple - the challenge is the annotations.
"""

from __future__ import annotations
from typing import TypeVar, Protocol, Callable, overload
from collections.abc import Iterable, Sequence, Iterator, Mapping


# =============================================================================
# Exercise 1: Basic Type Hints
# =============================================================================
# Add type hints to these simple functions

def greet(name, greeting):
    """
    Return a greeting message.

    TODO: Add type hints for parameters and return type
    - name: str
    - greeting: str
    - returns: str
    """
    return f"{greeting}, {name}!"


def calculate_area(length, width):
    """
    Calculate area of a rectangle.

    TODO: Add type hints for parameters and return type
    - length: float
    - width: float
    - returns: float
    """
    return length * width


def is_even(n):
    """
    Check if a number is even.

    TODO: Add type hints for parameters and return type
    - n: int
    - returns: bool
    """
    return n % 2 == 0


# Verify the functions work (type hints don't affect runtime)
assert greet("Alice", "Hello") == "Hello, Alice!"
assert calculate_area(3.0, 4.0) == 12.0
assert is_even(4) == True
assert is_even(7) == False

# Check that type hints are present
import inspect
sig = inspect.signature(greet)
assert sig.parameters['name'].annotation != inspect.Parameter.empty, "greet: 'name' needs type hint"
assert sig.parameters['greeting'].annotation != inspect.Parameter.empty, "greet: 'greeting' needs type hint"
assert sig.return_annotation != inspect.Signature.empty, "greet: needs return type hint"

sig = inspect.signature(calculate_area)
assert sig.parameters['length'].annotation != inspect.Parameter.empty, "calculate_area: 'length' needs type hint"
assert sig.return_annotation != inspect.Signature.empty, "calculate_area: needs return type hint"

sig = inspect.signature(is_even)
assert sig.parameters['n'].annotation != inspect.Parameter.empty, "is_even: 'n' needs type hint"
assert sig.return_annotation != inspect.Signature.empty, "is_even: needs return type hint"

print("✓ Exercise 1 passed: Basic Type Hints")


# =============================================================================
# Exercise 2: Optional Parameters
# =============================================================================
# Add type hints for functions with optional parameters (can be None)

def find_index(items, target, default):
    """
    Find index of target in items, return default if not found.

    TODO: Add type hints
    - items: list of strings
    - target: str
    - default: int or None
    - returns: int or None
    """
    try:
        return items.index(target)
    except ValueError:
        return default


def get_first_char(text):
    """
    Return first character of text, or None if empty.

    TODO: Add type hints
    - text: str
    - returns: str or None
    """
    if text:
        return text[0]
    return None


# Verify functionality
assert find_index(["a", "b", "c"], "b", None) == 1
assert find_index(["a", "b", "c"], "z", None) is None
assert find_index(["a", "b", "c"], "z", -1) == -1
assert get_first_char("hello") == "h"
assert get_first_char("") is None

# Check type hints
sig = inspect.signature(find_index)
assert sig.return_annotation != inspect.Signature.empty, "find_index: needs return type hint"

sig = inspect.signature(get_first_char)
assert sig.return_annotation != inspect.Signature.empty, "get_first_char: needs return type hint"

print("✓ Exercise 2 passed: Optional Parameters")


# =============================================================================
# Exercise 3: Collection Type Hints
# =============================================================================
# Add type hints for functions working with collections

def sum_values(numbers):
    """
    Sum all numbers in a list.

    TODO: Add type hints
    - numbers: list of floats
    - returns: float
    """
    return sum(numbers)


def word_lengths(words):
    """
    Return a dict mapping each word to its length.

    TODO: Add type hints
    - words: list of strings
    - returns: dict mapping str to int
    """
    return {word: len(word) for word in words}


def get_coordinates():
    """
    Return a fixed 3D coordinate.

    TODO: Add return type hint
    - returns: tuple of exactly 3 floats
    """
    return (1.0, 2.0, 3.0)


def get_factors(n):
    """
    Return tuple of all factors of n.

    TODO: Add type hints
    - n: int
    - returns: tuple of variable number of ints
    """
    return tuple(i for i in range(1, n + 1) if n % i == 0)


# Verify functionality
assert sum_values([1.0, 2.0, 3.0]) == 6.0
assert word_lengths(["hi", "hello"]) == {"hi": 2, "hello": 5}
assert get_coordinates() == (1.0, 2.0, 3.0)
assert get_factors(12) == (1, 2, 3, 4, 6, 12)

# Check type hints
sig = inspect.signature(sum_values)
assert sig.parameters['numbers'].annotation != inspect.Parameter.empty, "sum_values: 'numbers' needs type hint"
assert sig.return_annotation != inspect.Signature.empty, "sum_values: needs return type hint"

sig = inspect.signature(word_lengths)
assert sig.return_annotation != inspect.Signature.empty, "word_lengths: needs return type hint"

sig = inspect.signature(get_coordinates)
assert sig.return_annotation != inspect.Signature.empty, "get_coordinates: needs return type hint"
# Check it's a specific tuple type (3 elements)
ret_ann = sig.return_annotation
assert 'tuple' in str(ret_ann).lower(), "get_coordinates: return should be tuple type"

print("✓ Exercise 3 passed: Collection Type Hints")


# =============================================================================
# Exercise 4: Abstract Collection Types
# =============================================================================
# Use abstract types (Iterable, Sequence, Mapping) for more flexible APIs

def total(numbers):
    """
    Sum numbers from any iterable (list, tuple, generator, etc.)

    TODO: Add type hints using Iterable from collections.abc
    - numbers: any iterable of floats
    - returns: float
    """
    return sum(numbers)


def first_and_last(items):
    """
    Return first and last items from a sequence.

    TODO: Add type hints using Sequence from collections.abc
    - items: any sequence (supports indexing) of strings
    - returns: tuple of two strings
    """
    return (items[0], items[-1])


def get_value(mapping, key, default):
    """
    Get value from any mapping type.

    TODO: Add type hints using Mapping from collections.abc
    - mapping: any mapping from str to int
    - key: str
    - default: int
    - returns: int
    """
    return mapping.get(key, default)


# Verify with different types
assert total([1.0, 2.0, 3.0]) == 6.0
assert total((1.0, 2.0, 3.0)) == 6.0  # Works with tuple
assert total(x for x in [1.0, 2.0, 3.0]) == 6.0  # Works with generator

assert first_and_last(["a", "b", "c"]) == ("a", "c")
assert first_and_last(("a", "b", "c")) == ("a", "c")  # Works with tuple

assert get_value({"a": 1, "b": 2}, "a", 0) == 1
assert get_value({"a": 1, "b": 2}, "z", 0) == 0

# Check for abstract types in annotations
sig = inspect.signature(total)
ann_str = str(sig.parameters['numbers'].annotation)
assert 'Iterable' in ann_str or 'iterable' in ann_str.lower(), "total: use Iterable type"

sig = inspect.signature(first_and_last)
ann_str = str(sig.parameters['items'].annotation)
assert 'Sequence' in ann_str or 'sequence' in ann_str.lower(), "first_and_last: use Sequence type"

sig = inspect.signature(get_value)
ann_str = str(sig.parameters['mapping'].annotation)
assert 'Mapping' in ann_str or 'mapping' in ann_str.lower(), "get_value: use Mapping type"

print("✓ Exercise 4 passed: Abstract Collection Types")


# =============================================================================
# Exercise 5: TypeVar for Generic Functions
# =============================================================================
# Use TypeVar to create generic functions that preserve types

# TODO: Define a TypeVar named 'T' that can be any type
T = None  # Replace with TypeVar('T')


def first(items):
    """
    Return first item from a sequence.

    TODO: Add type hints using T
    - items: Sequence of T
    - returns: T

    This allows: first(['a', 'b']) returns str
                 first([1, 2, 3]) returns int
    """
    return items[0]


def last(items):
    """
    Return last item from a sequence.

    TODO: Add type hints using T
    - items: Sequence of T
    - returns: T
    """
    return items[-1]


# TODO: Define a TypeVar named 'Num' constrained to int and float only
Num = None  # Replace with TypeVar('Num', int, float)


def double(x):
    """
    Double a number, preserving its type.

    TODO: Add type hints using Num
    - x: Num (int or float)
    - returns: Num

    This allows: double(5) -> int, double(5.0) -> float
    """
    return x * 2


# Verify functionality
assert first([1, 2, 3]) == 1
assert first(["a", "b"]) == "a"
assert last([1, 2, 3]) == 3
assert double(5) == 10
assert double(2.5) == 5.0

# Check TypeVars are defined
assert T is not None, "T TypeVar must be defined"
assert Num is not None, "Num TypeVar must be defined"
from typing import TypeVar as TV
assert isinstance(T, TV), "T must be a TypeVar"
assert isinstance(Num, TV), "Num must be a TypeVar"

print("✓ Exercise 5 passed: TypeVar for Generic Functions")


# =============================================================================
# Exercise 6: Callable Type Hints
# =============================================================================
# Add type hints for functions that accept other functions as arguments

def apply_twice(func, value):
    """
    Apply a function twice to a value.

    TODO: Add type hints
    - func: a callable that takes an int and returns an int
    - value: int
    - returns: int
    """
    return func(func(value))


def transform_all(items, transformer):
    """
    Apply transformer function to all items.

    TODO: Add type hints
    - items: list of strings
    - transformer: callable that takes str and returns str
    - returns: list of strings
    """
    return [transformer(item) for item in items]


def compose(f, g):
    """
    Return a new function that applies g then f.
    compose(f, g)(x) == f(g(x))

    TODO: Add type hints
    - f: callable that takes int and returns int
    - g: callable that takes int and returns int
    - returns: callable that takes int and returns int
    """
    def composed(x):
        return f(g(x))
    return composed


# Verify functionality
assert apply_twice(lambda x: x + 1, 0) == 2
assert apply_twice(lambda x: x * 2, 3) == 12
assert transform_all(["hello", "world"], str.upper) == ["HELLO", "WORLD"]

add_one = lambda x: x + 1
times_two = lambda x: x * 2
composed = compose(add_one, times_two)
assert composed(5) == 11  # add_one(times_two(5)) = add_one(10) = 11

# Check for Callable in annotations
sig = inspect.signature(apply_twice)
ann_str = str(sig.parameters['func'].annotation)
assert 'Callable' in ann_str or 'callable' in ann_str.lower(), "apply_twice: 'func' should use Callable"

sig = inspect.signature(compose)
ann_str = str(sig.return_annotation)
assert 'Callable' in ann_str or 'callable' in ann_str.lower(), "compose: return should use Callable"

print("✓ Exercise 6 passed: Callable Type Hints")


# =============================================================================
# Exercise 7: Protocol for Structural Typing
# =============================================================================
# Define a Protocol to enable duck typing with static type checking

# TODO: Define a Protocol class named 'SupportsLessThan'
# It should have a __lt__ method that:
#   - takes self and other: object
#   - returns bool

class SupportsLessThan(Protocol):
    """Protocol for objects that support < comparison."""

    def __lt__(self, other: object) -> bool:
        """
        TODO: Define the __lt__ method signature
        Use ... as the body (protocols don't implement methods)
        """
        ...
        pass  # Replace with just ... (ellipsis)


# TODO: Add type hints using SupportsLessThan
LT = TypeVar('LT', bound=SupportsLessThan)


def minimum(a, b):
    """
    Return the smaller of two values.

    TODO: Add type hints using the LT TypeVar bound to SupportsLessThan
    - a: LT
    - b: LT
    - returns: LT

    This allows any type that supports < comparison.
    """
    return a if a < b else b


# Verify functionality with different types
assert minimum(3, 5) == 3
assert minimum("apple", "banana") == "apple"
assert minimum(3.14, 2.71) == 2.71

# Verify Protocol is correctly defined
assert hasattr(SupportsLessThan, '__lt__'), "SupportsLessThan needs __lt__ method"

# Check annotations
sig = inspect.signature(minimum)
assert sig.parameters['a'].annotation != inspect.Parameter.empty, "minimum: 'a' needs type hint"
assert sig.return_annotation != inspect.Signature.empty, "minimum: needs return type"

print("✓ Exercise 7 passed: Protocol for Structural Typing")


# =============================================================================
# Exercise 8: Iterator Return Type
# =============================================================================
# Add type hints for generator functions

def count_up_to(n):
    """
    Yield integers from 0 to n-1.

    TODO: Add type hints
    - n: int
    - returns: Iterator[int]
    """
    for i in range(n):
        yield i


def repeat(value, times):
    """
    Yield value repeated times.

    TODO: Add type hints
    - value: str
    - times: int
    - returns: Iterator[str]
    """
    for _ in range(times):
        yield value


def fibonacci(limit):
    """
    Yield Fibonacci numbers up to limit.

    TODO: Add type hints
    - limit: int
    - returns: Iterator[int]
    """
    a, b = 0, 1
    while a < limit:
        yield a
        a, b = b, a + b


# Verify functionality
assert list(count_up_to(5)) == [0, 1, 2, 3, 4]
assert list(repeat("x", 3)) == ["x", "x", "x"]
assert list(fibonacci(10)) == [0, 1, 1, 2, 3, 5, 8]

# Check return type annotations
sig = inspect.signature(count_up_to)
ann_str = str(sig.return_annotation)
assert 'Iterator' in ann_str or 'iterator' in ann_str.lower(), "count_up_to: should return Iterator"

sig = inspect.signature(repeat)
ann_str = str(sig.return_annotation)
assert 'Iterator' in ann_str or 'iterator' in ann_str.lower(), "repeat: should return Iterator"

print("✓ Exercise 8 passed: Iterator Return Type")


# =============================================================================
# Exercise 9: Overloaded Functions
# =============================================================================
# Use @overload to provide multiple type signatures

# TODO: Add overload decorators to specify these signatures:
# 1. process(x: int) -> int
# 2. process(x: str) -> str
# 3. process(x: list[int]) -> list[int]

# First, add the @overload decorated signatures (stubs)
# @overload
# def process(x: int) -> int: ...
# @overload
# def process(x: str) -> str: ...
# @overload
# def process(x: list[int]) -> list[int]: ...

# Then the actual implementation:
def process(x):
    """
    Double integers, uppercase strings, or double each element in a list.

    TODO: Add @overload signatures above this function
    The implementation below handles all cases.
    """
    if isinstance(x, int):
        return x * 2
    elif isinstance(x, str):
        return x.upper()
    elif isinstance(x, list):
        return [i * 2 for i in x]
    raise TypeError(f"Unsupported type: {type(x)}")


# Verify functionality
assert process(5) == 10
assert process("hello") == "HELLO"
assert process([1, 2, 3]) == [2, 4, 6]

print("✓ Exercise 9 passed: Overloaded Functions")


# =============================================================================
# Exercise 10: NoReturn Type
# =============================================================================
# Use NoReturn for functions that never return normally

from typing import NoReturn


def raise_error(message):
    """
    Raise a ValueError with the given message.

    TODO: Add type hints
    - message: str
    - returns: NoReturn (this function never returns normally)
    """
    raise ValueError(message)


def infinite_loop():
    """
    Run forever (never returns).

    TODO: Add return type hint: NoReturn
    """
    while True:
        pass


# Verify the function raises
try:
    raise_error("test error")
    assert False, "Should have raised ValueError"
except ValueError as e:
    assert str(e) == "test error"

# Check NoReturn annotation
sig = inspect.signature(raise_error)
ann_str = str(sig.return_annotation)
assert 'NoReturn' in ann_str or 'Never' in ann_str, "raise_error: should return NoReturn"

sig = inspect.signature(infinite_loop)
ann_str = str(sig.return_annotation)
assert 'NoReturn' in ann_str or 'Never' in ann_str, "infinite_loop: should return NoReturn"

print("✓ Exercise 10 passed: NoReturn Type")


# =============================================================================
# Exercise 11: Putting It All Together
# =============================================================================
# Create a fully typed function using multiple concepts

# TODO: Add complete type hints to this function
# Use:
#   - Iterable for the data parameter
#   - Callable for the key parameter (takes T, returns value for comparison)
#   - TypeVar T for the generic type
#   - Optional/| None for the default parameter
#   - Proper return type

T2 = TypeVar('T2')


def find_max(data, key, default):
    """
    Find the maximum item in data according to key function.
    Return default if data is empty.

    TODO: Add type hints
    - data: Iterable[T2]
    - key: Callable[[T2], float]  (function to extract comparison value)
    - default: T2 | None
    - returns: T2 | None

    Example: find_max(['a', 'bbb', 'cc'], len, None) returns 'bbb'
    """
    max_item = default
    max_value = None
    for item in data:
        value = key(item)
        if max_value is None or value > max_value:
            max_item = item
            max_value = value
    return max_item


# Verify functionality
assert find_max([1, 3, 2], lambda x: x, None) == 3
assert find_max(['a', 'bbb', 'cc'], len, None) == 'bbb'
assert find_max([], len, 'default') == 'default'
assert find_max([], len, None) is None

# Check type hints are present
sig = inspect.signature(find_max)
assert sig.parameters['data'].annotation != inspect.Parameter.empty, "find_max: 'data' needs type hint"
assert sig.parameters['key'].annotation != inspect.Parameter.empty, "find_max: 'key' needs type hint"
assert sig.parameters['default'].annotation != inspect.Parameter.empty, "find_max: 'default' needs type hint"
assert sig.return_annotation != inspect.Signature.empty, "find_max: needs return type"

print("✓ Exercise 11 passed: Putting It All Together")


# =============================================================================
# Exercise 12: Type Hints with *args and **kwargs
# =============================================================================
# Add type hints for variadic parameters

def join_strings(*args):
    """
    Join all string arguments with spaces.

    TODO: Add type hints
    - *args: each argument is a str
    - returns: str
    """
    return ' '.join(args)


def configure(**kwargs):
    """
    Print configuration as key=value pairs.

    TODO: Add type hints
    - **kwargs: each value is a str
    - returns: None
    """
    for key, value in kwargs.items():
        print(f"{key}={value}")


def create_point(*coords):
    """
    Create a point from coordinate values.

    TODO: Add type hints
    - *coords: each argument is a float
    - returns: tuple of floats (variable length)
    """
    return tuple(coords)


# Verify functionality
assert join_strings("hello", "world") == "hello world"
assert join_strings("a", "b", "c") == "a b c"
assert create_point(1.0, 2.0) == (1.0, 2.0)
assert create_point(1.0, 2.0, 3.0) == (1.0, 2.0, 3.0)

# Check annotations exist
sig = inspect.signature(join_strings)
# For *args, the annotation applies to each element
args_param = [p for p in sig.parameters.values() if p.kind == inspect.Parameter.VAR_POSITIONAL][0]
assert args_param.annotation != inspect.Parameter.empty, "join_strings: *args needs type hint"

sig = inspect.signature(configure)
kwargs_param = [p for p in sig.parameters.values() if p.kind == inspect.Parameter.VAR_KEYWORD][0]
assert kwargs_param.annotation != inspect.Parameter.empty, "configure: **kwargs needs type hint"

print("✓ Exercise 12 passed: Type Hints with *args and **kwargs")


# =============================================================================
# All exercises completed!
# =============================================================================
print("\n" + "=" * 60)
print("🎉 Congratulations! All Chapter 8 exercises passed!")
print("=" * 60)
print("\nNote: While these exercises check for the presence of type hints,")
print("you should also run 'mypy chapter8_type_hints_in_functions.py'")
print("to verify your annotations are correct according to the type checker.")
