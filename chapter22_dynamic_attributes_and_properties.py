"""
Chapter 21: Dynamic Attributes and Properties - Exercises
==========================================================

Practice using properties, __getattr__, __setattr__, and
dynamic attribute programming techniques.

Run this file to check your implementations.
"""

import keyword
from functools import cached_property, cache
from typing import Any

# =============================================================================
# Exercise 1: Basic Read-Only Property
# =============================================================================
# Create a Circle class with a read-only 'area' property.


class Circle:
    """A circle with radius and computed area."""

    def __init__(self, radius: float):
        self._radius = radius

    @property
    def radius(self):
        return self._radius

    # TODO: Add an 'area' property that computes and returns pi * radius^2
    # Use 3.14159 for pi
    pass


# Test Exercise 1
c = Circle(5)
assert c.radius == 5
assert abs(c.area - 78.53975) < 0.0001, f"Expected ~78.54, got {c.area}"

try:
    c.area = 100  # Should fail - read-only
    assert False, "Should not be able to set area"
except AttributeError:
    pass

print("    Exercise 1 passed: Basic read-only property")


# =============================================================================
# Exercise 2: Read/Write Property with Validation
# =============================================================================
# Create a property that validates values on assignment.


class Temperature:
    """Temperature in Celsius with validation."""

    def __init__(self, celsius: float):
        self.celsius = celsius  # Uses the setter

    # TODO: Create a 'celsius' property that:
    # - Returns self._celsius in the getter
    # - In the setter, raises ValueError if value < -273.15 (absolute zero)
    # - Otherwise stores value in self._celsius
    pass


# Test Exercise 2
t = Temperature(25)
assert t.celsius == 25

t.celsius = 100
assert t.celsius == 100

try:
    t.celsius = -300  # Below absolute zero
    assert False, "Should not allow below absolute zero"
except ValueError:
    pass

try:
    Temperature(-300)  # Also fails in __init__
    assert False, "Should not allow below absolute zero"
except ValueError:
    pass

print("    Exercise 2 passed: Read/write property with validation")


# =============================================================================
# Exercise 3: Property with Getter, Setter, and Deleter
# =============================================================================
# Implement a property with all three methods.

deleted_names: list[str] = []


class Person:
    """Person with managed name attribute."""

    def __init__(self, name: str):
        self._name = name

    # TODO: Create a 'name' property with:
    # - getter: returns self._name
    # - setter: sets self._name to value
    # - deleter: appends self._name to deleted_names list, then deletes self._name
    pass


# Test Exercise 3
deleted_names.clear()
p = Person("Alice")
assert p.name == "Alice"

p.name = "Bob"
assert p.name == "Bob"

del p.name
assert deleted_names == ["Bob"]
assert not hasattr(p, '_name')

print("    Exercise 3 passed: Property with deleter")


# =============================================================================
# Exercise 4: The Bunch Pattern
# =============================================================================
# Create a class that accepts arbitrary keyword arguments as attributes.


class Bunch:
    """A simple class that creates attributes from keyword arguments."""

    def __init__(self, **kwargs):
        # TODO: Update self.__dict__ with kwargs
        pass

    def __repr__(self):
        items = ', '.join(f'{k}={v!r}' for k, v in self.__dict__.items())
        return f'Bunch({items})'


# Test Exercise 4
b = Bunch(name="Alice", age=30, city="Paris")
assert b.name == "Alice"
assert b.age == 30
assert b.city == "Paris"

b.country = "France"  # Can add more attributes
assert b.country == "France"

print("    Exercise 4 passed: Bunch pattern")


# =============================================================================
# Exercise 5: Dynamic Attribute with __getattr__
# =============================================================================
# Implement __getattr__ to provide default values for missing attributes.


class DefaultDict:
    """Object that returns a default value for missing attributes."""

    def __init__(self, default: Any, **kwargs):
        self._default = default
        self.__dict__.update(kwargs)

    # TODO: Implement __getattr__ to return self._default for missing attributes
    pass


# Test Exercise 5
dd = DefaultDict(0, x=10, y=20)
assert dd.x == 10
assert dd.y == 20
assert dd.z == 0  # Missing -> default
assert dd.anything == 0  # Missing -> default

dd2 = DefaultDict("N/A", name="Alice")
assert dd2.name == "Alice"
assert dd2.age == "N/A"

print("    Exercise 5 passed: __getattr__ for defaults")


# =============================================================================
# Exercise 6: FrozenJSON-style Nested Access
# =============================================================================
# Create a class that allows dot notation for nested dictionaries.


class DotDict:
    """Access nested dict values using dot notation."""

    def __init__(self, data: dict):
        self._data = dict(data)

    def __getattr__(self, name: str):
        # TODO: Implement to:
        # 1. If name is in self._data:
        #    - If value is a dict, return DotDict(value)
        #    - Otherwise return the value as-is
        # 2. If name not in self._data, raise AttributeError
        pass

    def __repr__(self):
        return f'DotDict({self._data!r})'


# Test Exercise 6
data = {
    'name': 'Alice',
    'address': {
        'city': 'Paris',
        'country': 'France',
        'geo': {
            'lat': 48.8566,
            'lon': 2.3522
        }
    },
    'age': 30
}

dd = DotDict(data)
assert dd.name == 'Alice'
assert dd.age == 30
assert dd.address.city == 'Paris'
assert dd.address.country == 'France'
assert dd.address.geo.lat == 48.8566

try:
    dd.missing
    assert False, "Should raise AttributeError"
except AttributeError:
    pass

print("    Exercise 6 passed: DotDict nested access")


# =============================================================================
# Exercise 7: Keyword-Safe Attribute Names
# =============================================================================
# Handle Python keywords in attribute names.


class SafeRecord:
    """Record that handles Python keywords in attribute names."""

    def __init__(self, **kwargs):
        # TODO: For each key-value pair:
        # - If key is a Python keyword (use keyword.iskeyword), append '_'
        # - Store in self.__dict__
        pass


# Test Exercise 7
sr = SafeRecord(name="Test", **{'class': 2024, 'for': 'loop', 'normal': 'value'})
assert sr.name == "Test"
assert sr.class_ == 2024  # 'class' -> 'class_'
assert sr.for_ == 'loop'  # 'for' -> 'for_'
assert sr.normal == 'value'

print("    Exercise 7 passed: Keyword-safe attributes")


# =============================================================================
# Exercise 8: Property Factory
# =============================================================================
# Create a factory function that generates validating properties.


def positive(storage_name: str):
    """Property factory for positive number validation."""
    # TODO: Return a property that:
    # - getter: returns instance.__dict__[storage_name]
    # - setter: if value > 0, stores in instance.__dict__[storage_name]
    #           else raises ValueError
    pass


class Product:
    """Product with validated positive price and quantity."""
    price = positive('price')
    quantity = positive('quantity')

    def __init__(self, name: str, price: float, quantity: int):
        self.name = name
        self.price = price
        self.quantity = quantity

    def total(self):
        return self.price * self.quantity


# Test Exercise 8
p = Product("Widget", 9.99, 5)
assert p.price == 9.99
assert p.quantity == 5
assert p.total() == 49.95

p.price = 19.99
assert p.price == 19.99

try:
    p.price = -10
    assert False, "Should not allow negative price"
except ValueError:
    pass

try:
    Product("Bad", -5, 10)
    assert False, "Should not allow negative price"
except ValueError:
    pass

print("    Exercise 8 passed: Property factory")


# =============================================================================
# Exercise 9: Cached Property (Manual Implementation)
# =============================================================================
# Implement manual caching that preserves key-sharing optimization.


class ExpensiveComputation:
    """Class with manually cached expensive computation."""

    def __init__(self, data: list[int]):
        self._data = data
        self._cached_sum = None  # Initialize in __init__ for key-sharing

    @property
    def total(self) -> int:
        # TODO: If self._cached_sum is None, compute sum(self._data)
        # and store in self._cached_sum
        # Return self._cached_sum
        pass

    def invalidate_cache(self):
        """Call this when data changes."""
        self._cached_sum = None


# Test Exercise 9
ec = ExpensiveComputation([1, 2, 3, 4, 5])
assert ec.total == 15
assert ec._cached_sum == 15  # Cached

ec._data.append(10)
assert ec.total == 15  # Still cached (stale)

ec.invalidate_cache()
assert ec.total == 25  # Recomputed

print("    Exercise 9 passed: Manual cached property")


# =============================================================================
# Exercise 10: Using functools.cached_property
# =============================================================================
# Use the built-in cached_property decorator.


class DataAnalyzer:
    """Analyzer with cached expensive computations."""

    def __init__(self, numbers: list[int]):
        self._numbers = numbers

    # TODO: Use @cached_property decorator
    # Return the average of self._numbers
    @property  # Replace with @cached_property
    def average(self) -> float:
        print("Computing average...")  # Should only print once
        pass


# Test Exercise 10
da = DataAnalyzer([10, 20, 30, 40, 50])
# First access computes
avg1 = da.average
assert avg1 == 30.0

# Second access uses cache (no "Computing..." printed)
avg2 = da.average
assert avg2 == 30.0

# Can clear cache by deleting the attribute
del da.average
avg3 = da.average  # Recomputes
assert avg3 == 30.0

print("    Exercise 10 passed: functools.cached_property")


# =============================================================================
# Exercise 11: __setattr__ for Validation
# =============================================================================
# Use __setattr__ to validate all attribute assignments.


class StrictTyped:
    """Class that enforces type annotations on assignment."""

    name: str
    age: int
    score: float

    def __init__(self, name: str, age: int, score: float):
        self.name = name
        self.age = age
        self.score = score

    def __setattr__(self, name: str, value: Any):
        # TODO: Get type hints from self.__class__.__annotations__
        # If name is in annotations, check isinstance(value, expected_type)
        # Raise TypeError if wrong type
        # Use super().__setattr__(name, value) to actually set
        pass


# Test Exercise 11
st = StrictTyped("Alice", 30, 95.5)
assert st.name == "Alice"
assert st.age == 30
assert st.score == 95.5

st.name = "Bob"
assert st.name == "Bob"

try:
    st.age = "thirty"  # Wrong type
    assert False, "Should not allow wrong type"
except TypeError:
    pass

try:
    st.score = "high"  # Wrong type
    assert False, "Should not allow wrong type"
except TypeError:
    pass

print("    Exercise 11 passed: __setattr__ for type validation")


# =============================================================================
# Exercise 12: Read-Only Object After Initialization
# =============================================================================
# Create an object that becomes immutable after __init__.


class FrozenRecord:
    """Record that cannot be modified after creation."""

    _frozen: bool = False

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        self._frozen = True

    def __setattr__(self, name: str, value: Any):
        # TODO: If self._frozen is True and name != '_frozen',
        # raise AttributeError("Cannot modify frozen record")
        # Otherwise use super().__setattr__
        pass

    def __delattr__(self, name: str):
        # TODO: If self._frozen, raise AttributeError
        pass


# Test Exercise 12
fr = FrozenRecord(name="Alice", age=30)
assert fr.name == "Alice"
assert fr.age == 30

try:
    fr.name = "Bob"
    assert False, "Should not allow modification"
except AttributeError:
    pass

try:
    fr.new_attr = "value"
    assert False, "Should not allow new attributes"
except AttributeError:
    pass

try:
    del fr.name
    assert False, "Should not allow deletion"
except AttributeError:
    pass

print("    Exercise 12 passed: Frozen record")


# =============================================================================
# Exercise 13: Virtual Attributes with __getattr__
# =============================================================================
# Implement virtual attributes for a Vector class.


class Vector:
    """Vector with virtual x, y, z attributes."""

    _components = ('x', 'y', 'z')

    def __init__(self, *args):
        if len(args) > 3:
            raise ValueError("Maximum 3 components")
        self._data = list(args)

    def __getattr__(self, name: str):
        # TODO: If name in _components, return self._data[index]
        # where index is the position of name in _components
        # Raise AttributeError for missing indices or unknown names
        pass

    def __setattr__(self, name: str, value: Any):
        # TODO: If name in _components, set self._data[index] = value
        # Otherwise use super().__setattr__
        pass

    def __repr__(self):
        return f'Vector{tuple(self._data)}'


# Test Exercise 13
v = Vector(1, 2, 3)
assert v.x == 1
assert v.y == 2
assert v.z == 3

v.x = 10
assert v.x == 10
assert v._data == [10, 2, 3]

v2 = Vector(5, 6)  # Only 2 components
assert v2.x == 5
assert v2.y == 6

try:
    v2.z  # Index out of range
    assert False, "Should raise AttributeError"
except AttributeError:
    pass

print("    Exercise 13 passed: Virtual attributes")


# =============================================================================
# Exercise 14: __new__ for Flexible Construction
# =============================================================================
# Use __new__ to return different types based on input.


class SmartNumber:
    """Returns int or float based on input."""

    def __new__(cls, value):
        # TODO: If value is an int, return that int directly
        # If value is a float with no decimal part (e.g., 5.0), return int
        # Otherwise return a float
        pass


# Test Exercise 14
n1 = SmartNumber(42)
assert n1 == 42
assert type(n1) == int

n2 = SmartNumber(3.14)
assert n2 == 3.14
assert type(n2) == float

n3 = SmartNumber(5.0)
assert n3 == 5
assert type(n3) == int

n4 = SmartNumber(0.5)
assert n4 == 0.5
assert type(n4) == float

print("    Exercise 14 passed: __new__ for flexible construction")


# =============================================================================
# Exercise 15: Property that Overrides Instance Attribute
# =============================================================================
# Demonstrate that properties shadow instance attributes.


class Shadowed:
    """Demonstrate property shadowing."""

    def __init__(self, value: int):
        self.__dict__['data'] = value  # Store directly in __dict__

    @property
    def data(self):
        # TODO: Return self.__dict__['data'] * 2
        # This demonstrates that property is called even though
        # 'data' exists in instance __dict__
        pass

    def get_raw_data(self):
        """Get the actual stored value bypassing the property."""
        return self.__dict__['data']


# Test Exercise 15
s = Shadowed(10)
assert s.get_raw_data() == 10  # Raw value
assert s.data == 20  # Property doubles it
assert 'data' in s.__dict__  # Instance attribute exists
assert s.data == 20  # Property still wins

s.__dict__['data'] = 50
assert s.data == 100  # Property still active

print("    Exercise 15 passed: Property shadows instance attribute")


# =============================================================================
print("\n" + "=" * 60)
print("Congratulations! All Chapter 21 exercises completed!")
print("=" * 60)
