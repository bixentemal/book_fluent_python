"""
Chapter 15: More About Type Hints - Exercises
=============================================

Practice advanced type hints: @overload, TypedDict, cast, Generic classes, and variance.

Run this file to check your implementations.
"""

from typing import (
    overload, TypedDict, cast, get_type_hints, get_origin, get_args,
    TypeVar, Generic, Sequence, Callable, Required, NotRequired
)
from collections.abc import Iterator

# =============================================================================
# Exercise 1: Basic @overload
# =============================================================================
# Implement a function 'double' that doubles its input.
# Use @overload to specify:
# - int -> int
# - str -> str
# - list -> list
#
# The function should return x * 2 for any input.

@overload
def double(x: int) -> int: ...
@overload
def double(x: str) -> str: ...
@overload
def double(x: list) -> list: ...

def double(x):
    # TODO: Implement the actual function
    pass


# Test Exercise 1
assert double(5) == 10, "double(5) should return 10"
assert double("ab") == "abab", "double('ab') should return 'abab'"
assert double([1, 2]) == [1, 2, 1, 2], "double([1, 2]) should return [1, 2, 1, 2]"
print("✓ Exercise 1 passed: @overload with double")


# =============================================================================
# Exercise 2: @overload with Optional Default
# =============================================================================
# Implement 'safe_get' that gets an item from a sequence by index.
# Use @overload to specify:
# - (seq, index) -> T | None  (returns None if index out of bounds)
# - (seq, index, default) -> T  (returns default if index out of bounds)
#
# Hint: Check if index is within bounds of the sequence.

T = TypeVar('T')

@overload
def safe_get(seq: Sequence[T], index: int) -> T | None: ...
@overload
def safe_get(seq: Sequence[T], index: int, default: T) -> T: ...

def safe_get(seq, index, default=None):
    # TODO: Implement the function
    # Return seq[index] if valid, otherwise return default (or None)
    pass


# Test Exercise 2
assert safe_get([1, 2, 3], 1) == 2, "Should return item at index"
assert safe_get([1, 2, 3], 10) is None, "Should return None for out of bounds"
assert safe_get([1, 2, 3], 10, -1) == -1, "Should return default for out of bounds"
assert safe_get("hello", 0) == "h", "Should work with strings"
assert safe_get("hello", 100, "?") == "?", "Should return default for strings too"
print("✓ Exercise 2 passed: @overload with optional default")


# =============================================================================
# Exercise 3: Basic TypedDict
# =============================================================================
# Create a TypedDict called 'PersonDict' with:
# - name: str (required)
# - age: int (required)
# - email: str (optional - use NotRequired)
#
# Then implement 'greet_person' that takes a PersonDict and returns a greeting.

class PersonDict(TypedDict):
    # TODO: Define the fields
    pass


def greet_person(person: PersonDict) -> str:
    # TODO: Return "Hello, {name}! You are {age} years old."
    pass


# Test Exercise 3
person1: PersonDict = {"name": "Alice", "age": 30}
person2: PersonDict = {"name": "Bob", "age": 25, "email": "bob@example.com"}
assert greet_person(person1) == "Hello, Alice! You are 30 years old."
assert greet_person(person2) == "Hello, Bob! You are 25 years old."
print("✓ Exercise 3 passed: Basic TypedDict")


# =============================================================================
# Exercise 4: TypedDict with total=False
# =============================================================================
# Create a TypedDict called 'ConfigDict' where all fields are optional:
# - debug: bool
# - log_level: str
# - max_retries: int
#
# Implement 'get_log_level' that returns the log_level or "INFO" as default.

class ConfigDict(TypedDict, total=False):
    # TODO: Define the optional fields
    pass


def get_log_level(config: ConfigDict) -> str:
    # TODO: Return config's log_level or "INFO" if not present
    pass


# Test Exercise 4
config1: ConfigDict = {"log_level": "DEBUG"}
config2: ConfigDict = {}
config3: ConfigDict = {"debug": True, "max_retries": 3}
assert get_log_level(config1) == "DEBUG"
assert get_log_level(config2) == "INFO"
assert get_log_level(config3) == "INFO"
print("✓ Exercise 4 passed: TypedDict with total=False")


# =============================================================================
# Exercise 5: Nested TypedDict
# =============================================================================
# Create TypedDicts for a book structure:
# - AuthorDict: name (str), country (str)
# - BookDict: title (str), year (int), author (AuthorDict)
#
# Implement 'format_book' that returns "{title} ({year}) by {author_name}"

class AuthorDict(TypedDict):
    # TODO: Define fields
    pass


class BookDict(TypedDict):
    # TODO: Define fields (author should be AuthorDict)
    pass


def format_book(book: BookDict) -> str:
    # TODO: Format as "{title} ({year}) by {author_name}"
    pass


# Test Exercise 5
book: BookDict = {
    "title": "Fluent Python",
    "year": 2022,
    "author": {"name": "Luciano Ramalho", "country": "Brazil"}
}
assert format_book(book) == "Fluent Python (2022) by Luciano Ramalho"
print("✓ Exercise 5 passed: Nested TypedDict")


# =============================================================================
# Exercise 6: Using get_type_hints
# =============================================================================
# Implement 'get_return_type' that takes a function and returns its return type.
# Use get_type_hints() to extract the type hints.
# Return None if there's no return type annotation.

def get_return_type(func: Callable) -> type | None:
    # TODO: Use get_type_hints to get the 'return' type
    # Return None if 'return' is not in the hints
    pass


# Test Exercise 6
def sample_func(x: int, y: str) -> bool:
    return True

def no_return_hint(x: int):
    pass

assert get_return_type(sample_func) == bool
assert get_return_type(no_return_hint) is None
print("✓ Exercise 6 passed: get_type_hints")


# =============================================================================
# Exercise 7: Using get_origin and get_args
# =============================================================================
# Implement 'describe_generic' that takes a generic type hint and returns
# a description string.
# Examples:
# - list[int] -> "list of int"
# - dict[str, int] -> "dict of str to int"
# - tuple[int, str] -> "tuple of int, str"
#
# Use get_origin() and get_args() to extract the information.

def describe_generic(hint) -> str:
    # TODO: Use get_origin and get_args to build the description
    # Handle: list[X] -> "list of X"
    #         dict[K, V] -> "dict of K to V"
    #         tuple[...] -> "tuple of X, Y, ..."
    pass


# Test Exercise 7
assert describe_generic(list[int]) == "list of int"
assert describe_generic(dict[str, int]) == "dict of str to int"
assert describe_generic(tuple[int, str, bool]) == "tuple of int, str, bool"
print("✓ Exercise 7 passed: get_origin and get_args")


# =============================================================================
# Exercise 8: Basic Generic Class
# =============================================================================
# Implement a generic Stack class with:
# - __init__: initialize empty stack
# - push(item: T) -> None: add item to top
# - pop() -> T: remove and return top item (raise IndexError if empty)
# - peek() -> T: return top item without removing (raise IndexError if empty)
# - is_empty() -> bool: return True if stack is empty

S = TypeVar('S')

class Stack(Generic[S]):
    def __init__(self) -> None:
        # TODO: Initialize the internal storage
        pass

    def push(self, item: S) -> None:
        # TODO: Add item to top of stack
        pass

    def pop(self) -> S:
        # TODO: Remove and return top item
        pass

    def peek(self) -> S:
        # TODO: Return top item without removing
        pass

    def is_empty(self) -> bool:
        # TODO: Return True if empty
        pass


# Test Exercise 8
int_stack: Stack[int] = Stack()
assert int_stack.is_empty() == True
int_stack.push(1)
int_stack.push(2)
int_stack.push(3)
assert int_stack.is_empty() == False
assert int_stack.peek() == 3
assert int_stack.pop() == 3
assert int_stack.pop() == 2
assert int_stack.peek() == 1

str_stack: Stack[str] = Stack()
str_stack.push("hello")
str_stack.push("world")
assert str_stack.pop() == "world"
assert str_stack.pop() == "hello"
assert str_stack.is_empty() == True
print("✓ Exercise 8 passed: Generic Stack class")


# =============================================================================
# Exercise 9: Generic Class with Multiple Type Parameters
# =============================================================================
# Implement a generic Pair class with two type parameters K and V:
# - __init__(key: K, value: V): store key and value
# - key property: return the key
# - value property: return the value
# - swap() -> Pair[V, K]: return a new Pair with key and value swapped

K = TypeVar('K')
V = TypeVar('V')

class Pair(Generic[K, V]):
    def __init__(self, key: K, value: V) -> None:
        # TODO: Store key and value
        pass

    @property
    def key(self) -> K:
        # TODO: Return the key
        pass

    @property
    def value(self) -> V:
        # TODO: Return the value
        pass

    def swap(self) -> 'Pair[V, K]':
        # TODO: Return new Pair with swapped key/value
        pass


# Test Exercise 9
pair1: Pair[str, int] = Pair("age", 25)
assert pair1.key == "age"
assert pair1.value == 25

swapped = pair1.swap()
assert swapped.key == 25
assert swapped.value == "age"

pair2: Pair[int, list] = Pair(1, [1, 2, 3])
assert pair2.key == 1
assert pair2.value == [1, 2, 3]
print("✓ Exercise 9 passed: Generic Pair class")


# =============================================================================
# Exercise 10: Bounded TypeVar
# =============================================================================
# Create a function 'find_max' that finds the maximum value in a sequence.
# Use a TypeVar bounded to types that support comparison (have __lt__).
#
# Hint: You can bound to a Protocol or use a simple approach.

from typing import Protocol

class Comparable(Protocol):
    def __lt__(self, other) -> bool: ...

C = TypeVar('C', bound=Comparable)

def find_max(items: Sequence[C]) -> C:
    # TODO: Return the maximum item
    # Raise ValueError if sequence is empty
    pass


# Test Exercise 10
assert find_max([3, 1, 4, 1, 5, 9, 2, 6]) == 9
assert find_max(["apple", "banana", "cherry"]) == "cherry"
assert find_max([3.14, 2.71, 1.41]) == 3.14
try:
    find_max([])
    assert False, "Should raise ValueError for empty sequence"
except ValueError:
    pass
print("✓ Exercise 10 passed: Bounded TypeVar")


# =============================================================================
# Exercise 11: Understanding Covariance
# =============================================================================
# Implement a generic 'Producer' class that is COVARIANT in T.
# This means Producer[Dog] is a subtype of Producer[Animal].
#
# - __init__(items: list[T]): store items
# - produce() -> T: return and remove the first item (FIFO)
# - has_items() -> bool: return True if items remain
#
# Use TypeVar with covariant=True

T_co = TypeVar('T_co', covariant=True)

class Producer(Generic[T_co]):
    def __init__(self, items: Sequence[T_co]) -> None:
        # TODO: Store a copy of items (as list for internal mutation)
        pass

    def produce(self) -> T_co:
        # TODO: Return and remove first item
        pass

    def has_items(self) -> bool:
        # TODO: Return True if items remain
        pass


# Test Exercise 11
class Animal:
    def __init__(self, name: str):
        self.name = name

class Dog(Animal):
    def bark(self) -> str:
        return "Woof!"

# Create a Producer of Dogs
dogs = [Dog("Rex"), Dog("Buddy")]
dog_producer: Producer[Dog] = Producer(dogs)

assert dog_producer.has_items() == True
first_dog = dog_producer.produce()
assert first_dog.name == "Rex"
assert first_dog.bark() == "Woof!"

# This should work because Producer is covariant
# Producer[Dog] is a subtype of Producer[Animal]
animal_producer: Producer[Animal] = dog_producer  # type: ignore (runtime works)
second = animal_producer.produce()
assert second.name == "Buddy"
assert animal_producer.has_items() == False
print("✓ Exercise 11 passed: Covariant Producer")


# =============================================================================
# Exercise 12: Using Sequence for Covariant Parameters
# =============================================================================
# Implement 'count_by_type' that counts items of a specific type in a sequence.
# Use Sequence (covariant) instead of list (invariant) for the parameter.
#
# This allows passing list[Dog] where Sequence[Animal] is expected.

def count_by_type(items: Sequence[object], target_type: type) -> int:
    # TODO: Count how many items are instances of target_type
    pass


# Test Exercise 12
class Cat(Animal):
    pass

animals: list[Animal] = [Dog("Rex"), Cat("Whiskers"), Dog("Buddy"), Cat("Mittens")]
assert count_by_type(animals, Dog) == 2
assert count_by_type(animals, Cat) == 2
assert count_by_type(animals, Animal) == 4
assert count_by_type(animals, str) == 0

# Works with list[Dog] too (Sequence is covariant)
dogs_only: list[Dog] = [Dog("Max"), Dog("Charlie")]
assert count_by_type(dogs_only, Dog) == 2
assert count_by_type(dogs_only, Animal) == 2
print("✓ Exercise 12 passed: Sequence covariance")


# =============================================================================
# Exercise 13: Callable Contravariance
# =============================================================================
# Demonstrate understanding of contravariance in Callable parameters.
#
# Implement 'apply_to_dog' that takes a handler function and a Dog,
# and applies the handler to the dog.
#
# The handler can be Callable[[Dog], str] OR Callable[[Animal], str]
# (because a function that handles any Animal can certainly handle a Dog)

def apply_to_dog(handler: Callable[[Animal], str], dog: Dog) -> str:
    # TODO: Apply handler to dog and return result
    pass


# Test Exercise 13
def describe_animal(animal: Animal) -> str:
    return f"Animal named {animal.name}"

def describe_dog(dog: Dog) -> str:
    return f"Dog named {dog.name} says {dog.bark()}"

rex = Dog("Rex")

# Both should work due to contravariance
assert apply_to_dog(describe_animal, rex) == "Animal named Rex"
# describe_dog also works but type checker might complain (it's more specific)
print("✓ Exercise 13 passed: Callable contravariance")


# =============================================================================
# Exercise 14: Generic Iterator
# =============================================================================
# Implement a generic 'Repeater' class that repeats an item a specified number
# of times when iterated.
#
# - __init__(item: T, times: int): store item and repeat count
# - __iter__() -> Iterator[T]: return self
# - __next__() -> T: return item (times) times, then raise StopIteration

R = TypeVar('R')

class Repeater(Generic[R]):
    def __init__(self, item: R, times: int) -> None:
        # TODO: Store item and times
        pass

    def __iter__(self) -> Iterator[R]:
        # TODO: Return iterator (self)
        pass

    def __next__(self) -> R:
        # TODO: Return item until times exhausted, then StopIteration
        pass


# Test Exercise 14
repeater: Repeater[str] = Repeater("hello", 3)
result = list(repeater)
assert result == ["hello", "hello", "hello"]

int_repeater: Repeater[int] = Repeater(42, 5)
assert list(int_repeater) == [42, 42, 42, 42, 42]

empty_repeater: Repeater[str] = Repeater("x", 0)
assert list(empty_repeater) == []
print("✓ Exercise 14 passed: Generic Iterator")


# =============================================================================
# BONUS Exercise 15: Type-Safe Registry with Generics
# =============================================================================
# Implement a type-safe registry that maps string keys to typed values.
# The registry should ensure type safety when getting values.
#
# - register(key: str, value: T) -> None: register a value
# - get(key: str, value_type: type[T]) -> T: get value, raise if wrong type
# - get_optional(key: str, value_type: type[T]) -> T | None: get or None

class Registry:
    def __init__(self) -> None:
        # TODO: Initialize storage
        pass

    def register(self, key: str, value: object) -> None:
        # TODO: Store the value
        pass

    def get(self, key: str, value_type: type[T]) -> T:
        # TODO: Get value, raise KeyError if missing, TypeError if wrong type
        pass

    def get_optional(self, key: str, value_type: type[T]) -> T | None:
        # TODO: Get value or None, raise TypeError if present but wrong type
        pass


# Test Exercise 15
registry = Registry()
registry.register("name", "Alice")
registry.register("age", 30)
registry.register("scores", [95, 87, 92])

assert registry.get("name", str) == "Alice"
assert registry.get("age", int) == 30
assert registry.get("scores", list) == [95, 87, 92]

assert registry.get_optional("name", str) == "Alice"
assert registry.get_optional("missing", str) is None

try:
    registry.get("name", int)  # Wrong type
    assert False, "Should raise TypeError"
except TypeError:
    pass

try:
    registry.get("missing", str)  # Missing key
    assert False, "Should raise KeyError"
except KeyError:
    pass
print("✓ Exercise 15 passed: Type-safe Registry")


# =============================================================================
print("\n" + "=" * 60)
print("Congratulations! All Chapter 15 exercises completed!")
print("=" * 60)
