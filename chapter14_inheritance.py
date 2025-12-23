"""
Chapter 14: Inheritance: For Better or for Worse - Exercises
=============================================================

Complete each exercise by replacing the `None` or `...` placeholders.
Run this file to check your answers with the assertions.
"""

from __future__ import annotations
from collections import UserDict, UserList
from typing import Any


# =============================================================================
# Exercise 1: Basic super() Usage
# =============================================================================
# Use super() to call parent class methods

class Animal:
    def __init__(self, name: str):
        self.name = name

    def speak(self) -> str:
        return f"{self.name} makes a sound"


class Dog(Animal):
    """
    A dog that adds its own behavior while calling parent methods.

    TODO: Implement __init__ and speak using super()
    """

    def __init__(self, name: str, breed: str):
        """
        Initialize Dog with name (via super) and breed.

        TODO: Call super().__init__(name) and set self.breed
        """
        ...
        pass

    def speak(self) -> str:
        """
        Return "<parent_speak> and barks!".

        TODO: Use super().speak() and add " and barks!"
        """
        ...
        pass


dog = Dog("Rex", "German Shepherd")
assert dog.name == "Rex", f"Expected 'Rex', got {dog.name}"
assert dog.breed == "German Shepherd"
assert dog.speak() == "Rex makes a sound and barks!"

print("✓ Exercise 1 passed: Basic super() Usage")


# =============================================================================
# Exercise 2: Multiple Levels of Inheritance
# =============================================================================
# Chain super() calls through multiple inheritance levels

class Vehicle:
    def __init__(self, brand: str):
        self.brand = brand

    def describe(self) -> str:
        return f"Vehicle: {self.brand}"


class Car(Vehicle):
    """
    TODO: Implement __init__ and describe using super()
    """

    def __init__(self, brand: str, model: str):
        """Initialize with brand (via super) and model."""
        ...
        pass

    def describe(self) -> str:
        """Return "<parent_describe>, Model: {model}"."""
        ...
        pass


class ElectricCar(Car):
    """
    TODO: Implement __init__ and describe using super()
    """

    def __init__(self, brand: str, model: str, battery_kwh: int):
        """Initialize with brand and model (via super) and battery_kwh."""
        ...
        pass

    def describe(self) -> str:
        """Return "<parent_describe>, Battery: {battery_kwh}kWh"."""
        ...
        pass


tesla = ElectricCar("Tesla", "Model 3", 75)
assert tesla.brand == "Tesla"
assert tesla.model == "Model 3"
assert tesla.battery_kwh == 75
assert tesla.describe() == "Vehicle: Tesla, Model: Model 3, Battery: 75kWh"

print("✓ Exercise 2 passed: Multiple Levels of Inheritance")


# =============================================================================
# Exercise 3: Subclassing Built-In Types (The Problem)
# =============================================================================
# Demonstrate why subclassing built-in dict is problematic

class BrokenDict(dict):
    """
    A dict that should uppercase all keys.
    This implementation is BROKEN because dict doesn't call our __setitem__.
    """

    def __setitem__(self, key, value):
        if isinstance(key, str):
            key = key.upper()
        super().__setitem__(key, value)


# Demonstrate the problem
bd = BrokenDict(hello='world')  # __init__ doesn't call our __setitem__
bd['foo'] = 'bar'  # Direct [] call works

# TODO: Fill in the expected values to understand the problem
assert bd.get('hello') == 'world'  # Key was NOT uppercased by __init__
assert bd.get('HELLO') == None     # So uppercase lookup fails
assert bd.get('FOO') == 'bar'      # Direct [] call DID uppercase

print("✓ Exercise 3 passed: Subclassing Built-In Types (The Problem)")


# =============================================================================
# Exercise 4: Using UserDict (The Solution)
# =============================================================================
# Properly subclass using UserDict

class UpperKeyDict(UserDict):
    """
    A dict that uppercases all string keys.

    TODO: Override __setitem__ to uppercase string keys
    """

    def __setitem__(self, key, value):
        """
        Store value with uppercased key (if string).

        TODO: Implement
        """
        ...
        pass


# This should work correctly!
ud = UpperKeyDict(hello='world')
ud['foo'] = 'bar'
ud.update({'baz': 'qux'})

assert ud.get('HELLO') == 'world', f"Expected 'world', got {ud.get('HELLO')}"
assert ud.get('FOO') == 'bar'
assert ud.get('BAZ') == 'qux'
assert ud.get('hello') is None  # Lowercase lookup should fail

print("✓ Exercise 4 passed: Using UserDict (The Solution)")


# =============================================================================
# Exercise 5: Understanding MRO
# =============================================================================
# Explore Method Resolution Order

class A:
    def method(self) -> str:
        return "A"


class B(A):
    def method(self) -> str:
        return "B" + super().method()


class C(A):
    def method(self) -> str:
        return "C" + super().method()


class D(B, C):
    def method(self) -> str:
        return "D" + super().method()


# TODO: Fill in the expected MRO and result
# Hint: D -> B -> C -> A -> object

d = D()
# What is the MRO of D?
expected_mro_names = ['D', 'B', 'C', 'A', 'object']
actual_mro_names = [cls.__name__ for cls in D.__mro__]
assert actual_mro_names == expected_mro_names, f"MRO: {actual_mro_names}"

# What does d.method() return?
# D calls super() -> B calls super() -> C calls super() -> A
expected_result = "DBCA"
assert d.method() == expected_result, f"Got: {d.method()}"

print("✓ Exercise 5 passed: Understanding MRO")


# =============================================================================
# Exercise 6: Cooperative Multiple Inheritance
# =============================================================================
# Create classes that cooperate via super()

class Base:
    def __init__(self):
        self.initialized_by = ['Base']

    def process(self) -> list[str]:
        return ['Base.process']


class Mixin1(Base):
    """
    TODO: Implement __init__ and process cooperatively
    """

    def __init__(self):
        """Call super().__init__() and append 'Mixin1' to initialized_by."""
        ...
        pass

    def process(self) -> list[str]:
        """Call super().process() and append 'Mixin1.process'."""
        ...
        pass


class Mixin2(Base):
    """
    TODO: Implement __init__ and process cooperatively
    """

    def __init__(self):
        """Call super().__init__() and append 'Mixin2' to initialized_by."""
        ...
        pass

    def process(self) -> list[str]:
        """Call super().process() and append 'Mixin2.process'."""
        ...
        pass


class Combined(Mixin1, Mixin2):
    """Uses both mixins."""

    def __init__(self):
        super().__init__()
        self.initialized_by.append('Combined')

    def process(self) -> list[str]:
        result = super().process()
        result.append('Combined.process')
        return result


combined = Combined()

# Check initialization order (follows MRO)
expected_init = ['Base', 'Mixin2', 'Mixin1', 'Combined']
assert combined.initialized_by == expected_init, f"Got: {combined.initialized_by}"

# Check process order
expected_process = ['Base.process', 'Mixin2.process', 'Mixin1.process', 'Combined.process']
assert combined.process() == expected_process, f"Got: {combined.process()}"

print("✓ Exercise 6 passed: Cooperative Multiple Inheritance")


# =============================================================================
# Exercise 7: Simple Mixin
# =============================================================================
# Create a mixin that adds serialization capability

import json


class JsonMixin:
    """
    Mixin that adds JSON serialization to any class with a to_dict method.

    TODO: Implement to_json method
    """

    def to_json(self) -> str:
        """
        Return JSON string representation.

        TODO: Call self.to_dict() and convert to JSON
        Hint: Use json.dumps()
        """
        ...
        pass


class Person:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

    def to_dict(self) -> dict:
        return {'name': self.name, 'age': self.age}


class SerializablePerson(JsonMixin, Person):
    """A person that can be serialized to JSON."""
    pass


sp = SerializablePerson("Alice", 30)
json_str = sp.to_json()
assert json.loads(json_str) == {'name': 'Alice', 'age': 30}

print("✓ Exercise 7 passed: Simple Mixin")


# =============================================================================
# Exercise 8: Logging Mixin
# =============================================================================
# Create a mixin that logs method calls

class LoggingMixin:
    """
    Mixin that logs method calls.

    TODO: Implement log method and log_call decorator-like method
    """

    def __init__(self):
        self._log: list[str] = []
        super().__init__()

    def log(self, message: str) -> None:
        """
        Add message to the log.

        TODO: Append message to self._log
        """
        ...
        pass

    def get_log(self) -> list[str]:
        """Return the log."""
        return self._log


class Calculator:
    def __init__(self):
        self.value = 0

    def add(self, x: int) -> int:
        self.value += x
        return self.value

    def subtract(self, x: int) -> int:
        self.value -= x
        return self.value


class LoggedCalculator(LoggingMixin, Calculator):
    """
    A calculator that logs all operations.

    TODO: Override add and subtract to log before calling super()
    """

    def add(self, x: int) -> int:
        """Log the addition and then perform it."""
        # TODO: Log f"add({x})" then call super().add(x)
        ...
        pass

    def subtract(self, x: int) -> int:
        """Log the subtraction and then perform it."""
        # TODO: Log f"subtract({x})" then call super().subtract(x)
        ...
        pass


calc = LoggedCalculator()
calc.add(5)
calc.subtract(2)
calc.add(10)

assert calc.value == 13
assert calc.get_log() == ['add(5)', 'subtract(2)', 'add(10)']

print("✓ Exercise 8 passed: Logging Mixin")


# =============================================================================
# Exercise 9: Timestamp Mixin
# =============================================================================
# Create a mixin that tracks creation and modification times

from datetime import datetime
import time


class TimestampMixin:
    """
    Mixin that tracks when an object was created and last modified.

    TODO: Implement __init__, touch, and properties
    """

    def __init__(self):
        self._created_at = datetime.now()
        self._modified_at = self._created_at
        super().__init__()

    @property
    def created_at(self) -> datetime:
        """Return creation timestamp."""
        return self._created_at

    @property
    def modified_at(self) -> datetime:
        """Return last modification timestamp."""
        return self._modified_at

    def touch(self) -> None:
        """
        Update the modification timestamp to now.

        TODO: Implement
        """
        ...
        pass


class Document:
    def __init__(self, content: str = ""):
        self.content = content

    def write(self, text: str) -> None:
        self.content += text


class TrackedDocument(TimestampMixin, Document):
    """
    A document that tracks modification times.

    TODO: Override write to call touch() after writing
    """

    def write(self, text: str) -> None:
        """Write text and update modification time."""
        # TODO: Call super().write(text) then self.touch()
        ...
        pass


doc = TrackedDocument("Hello")
created = doc.created_at

time.sleep(0.01)  # Small delay

doc.write(" World")
modified = doc.modified_at

assert doc.content == "Hello World"
assert doc.created_at == created  # Creation time unchanged
assert doc.modified_at > created  # Modification time updated

print("✓ Exercise 9 passed: Timestamp Mixin")


# =============================================================================
# Exercise 10: UserList Subclass
# =============================================================================
# Create a sorted list using UserList

class SortedList(UserList):
    """
    A list that keeps its elements sorted.

    TODO: Override __init__, append, and extend to maintain sorted order
    """

    def __init__(self, initial=None):
        """
        Initialize with optional initial items (will be sorted).

        TODO: Call super().__init__() then add and sort items
        """
        ...
        pass

    def append(self, item) -> None:
        """
        Add item and maintain sorted order.

        TODO: Implement using super().append() then sort
        Or use bisect.insort for efficiency
        """
        ...
        pass

    def extend(self, items) -> None:
        """
        Add multiple items and maintain sorted order.

        TODO: Implement
        """
        ...
        pass


sl = SortedList([3, 1, 4, 1, 5])
assert list(sl) == [1, 1, 3, 4, 5]

sl.append(2)
assert list(sl) == [1, 1, 2, 3, 4, 5]

sl.extend([0, 6])
assert list(sl) == [0, 1, 1, 2, 3, 4, 5, 6]

print("✓ Exercise 10 passed: UserList Subclass")


# =============================================================================
# Exercise 11: Default Value Dict
# =============================================================================
# Create a dict with factory defaults using UserDict

class DefaultDict(UserDict):
    """
    A dict that uses a factory function for missing keys.

    Similar to collections.defaultdict but using UserDict.

    TODO: Implement __init__ and __missing__
    """

    def __init__(self, default_factory, initial=None):
        """
        Initialize with a default factory and optional initial data.

        TODO: Store default_factory and call super().__init__()
        """
        ...
        pass

    def __missing__(self, key):
        """
        Called when key is not found.

        TODO: Call default_factory(), store the result, and return it
        """
        ...
        pass


# Test with list factory
dd = DefaultDict(list)
dd['a'].append(1)
dd['a'].append(2)
dd['b'].append(3)

assert dd['a'] == [1, 2]
assert dd['b'] == [3]
assert dd['c'] == []  # Creates empty list

# Test with int factory
counter = DefaultDict(int, {'existing': 5})
counter['existing'] += 1
counter['new'] += 1

assert counter['existing'] == 6
assert counter['new'] == 1

print("✓ Exercise 11 passed: Default Value Dict")


# =============================================================================
# Exercise 12: Validation Mixin
# =============================================================================
# Create a mixin that validates attribute assignments

class ValidationMixin:
    """
    Mixin that validates attribute assignments.

    Subclasses define _validators dict mapping attribute names to
    validation functions.
    """

    _validators: dict[str, callable] = {}

    def __setattr__(self, name: str, value: Any) -> None:
        """
        Validate value before setting attribute.

        TODO: Implement
        - Check if name is in _validators
        - If so, call the validator function with value
        - If validator returns False, raise ValueError
        - Call super().__setattr__(name, value)
        """
        ...
        pass


def positive_number(value) -> bool:
    """Validate that value is a positive number."""
    return isinstance(value, (int, float)) and value > 0


def non_empty_string(value) -> bool:
    """Validate that value is a non-empty string."""
    return isinstance(value, str) and len(value) > 0


class Product(ValidationMixin):
    _validators = {
        'price': positive_number,
        'name': non_empty_string,
    }

    def __init__(self, name: str, price: float):
        self.name = name
        self.price = price


# Valid product
p = Product("Widget", 9.99)
assert p.name == "Widget"
assert p.price == 9.99

# Invalid price
try:
    p.price = -5
    assert False, "Should raise ValueError for negative price"
except ValueError:
    pass

# Invalid name
try:
    p.name = ""
    assert False, "Should raise ValueError for empty name"
except ValueError:
    pass

print("✓ Exercise 12 passed: Validation Mixin")


# =============================================================================
# Exercise 13: Diamond Problem Resolution
# =============================================================================
# Understand and resolve the diamond problem

class Root:
    def __init__(self):
        self.value = 0

    def increment(self) -> int:
        self.value += 1
        return self.value


class Left(Root):
    """
    TODO: Override __init__ and increment, calling super()
    """

    def __init__(self):
        super().__init__()
        self.left_initialized = True

    def increment(self) -> int:
        """Add 10 then call super().increment()."""
        # TODO: Implement
        ...
        pass


class Right(Root):
    """
    TODO: Override __init__ and increment, calling super()
    """

    def __init__(self):
        super().__init__()
        self.right_initialized = True

    def increment(self) -> int:
        """Add 100 then call super().increment()."""
        # TODO: Implement
        ...
        pass


class Bottom(Left, Right):
    """Diamond inheritance: Bottom -> Left, Right -> Root"""

    def __init__(self):
        super().__init__()
        self.bottom_initialized = True


# Test diamond inheritance
bottom = Bottom()

# All __init__ methods should have run
assert hasattr(bottom, 'value')
assert bottom.left_initialized == True
assert bottom.right_initialized == True
assert bottom.bottom_initialized == True

# MRO: Bottom -> Left -> Right -> Root -> object
assert [c.__name__ for c in Bottom.__mro__] == ['Bottom', 'Left', 'Right', 'Root', 'object']

# increment should chain: Left (+10) -> Right (+100) -> Root (+1)
result = bottom.increment()
assert bottom.value == 111, f"Expected 111, got {bottom.value}"
assert result == 111

print("✓ Exercise 13 passed: Diamond Problem Resolution")


# =============================================================================
# All exercises completed!
# =============================================================================
print("\n" + "=" * 60)
print("🎉 Congratulations! All Chapter 14 exercises passed!")
print("=" * 60)
