"""
Chapter 22: Attribute Descriptors - Exercises
==============================================

Practice implementing and using descriptors for attribute
management, validation, and metaprogramming.

Run this file to check your implementations.
"""

import abc
from typing import Any

# =============================================================================
# Exercise 1: Basic Descriptor with __get__ and __set__
# =============================================================================
# Create a simple descriptor that stores values in the managed instance.


class SimpleDescriptor:
    """A basic descriptor that stores values in the instance."""

    def __set_name__(self, owner, name):
        self.storage_name = name

    def __get__(self, instance, owner):
        # TODO: If instance is None, return self
        # Otherwise return instance.__dict__[self.storage_name]
        pass

    def __set__(self, instance, value):
        # TODO: Store value in instance.__dict__[self.storage_name]
        pass


class Point:
    x = SimpleDescriptor()
    y = SimpleDescriptor()

    def __init__(self, x, y):
        self.x = x
        self.y = y


# Test Exercise 1
p = Point(3, 4)
assert p.x == 3
assert p.y == 4

p.x = 10
assert p.x == 10
assert p.__dict__ == {'x': 10, 'y': 4}

# Class-level access should return descriptor
assert isinstance(Point.x, SimpleDescriptor)

print("    Exercise 1 passed: Basic descriptor")


# =============================================================================
# Exercise 2: Validating Descriptor
# =============================================================================
# Create a descriptor that validates positive values.


class Positive:
    """Descriptor that only accepts positive numbers."""

    def __set_name__(self, owner, name):
        self.storage_name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self.storage_name)

    def __set__(self, instance, value):
        # TODO: Raise ValueError if value <= 0
        # Otherwise store in instance.__dict__[self.storage_name]
        pass


class Product:
    price = Positive()
    quantity = Positive()

    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity

    def total(self):
        return self.price * self.quantity


# Test Exercise 2
prod = Product("Widget", 9.99, 5)
assert prod.price == 9.99
assert prod.quantity == 5
assert prod.total() == 49.95

prod.price = 19.99
assert prod.price == 19.99

try:
    prod.price = -10
    assert False, "Should not allow negative price"
except ValueError:
    pass

try:
    prod.quantity = 0
    assert False, "Should not allow zero quantity"
except ValueError:
    pass

print("    Exercise 2 passed: Validating descriptor")


# =============================================================================
# Exercise 3: Type-Checking Descriptor
# =============================================================================
# Create a descriptor that enforces type checking.


class Typed:
    """Descriptor that enforces a specific type."""

    def __init__(self, expected_type: type):
        self.expected_type = expected_type
        self.storage_name = None

    def __set_name__(self, owner, name):
        self.storage_name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self.storage_name)

    def __set__(self, instance, value):
        # TODO: Raise TypeError if value is not instance of self.expected_type
        # Use: isinstance(value, self.expected_type)
        # Otherwise store in instance.__dict__[self.storage_name]
        pass


class Person:
    name = Typed(str)
    age = Typed(int)

    def __init__(self, name, age):
        self.name = name
        self.age = age


# Test Exercise 3
person = Person("Alice", 30)
assert person.name == "Alice"
assert person.age == 30

person.name = "Bob"
assert person.name == "Bob"

try:
    person.name = 123  # Wrong type
    assert False, "Should not allow int for name"
except TypeError:
    pass

try:
    person.age = "thirty"  # Wrong type
    assert False, "Should not allow str for age"
except TypeError:
    pass

print("    Exercise 3 passed: Type-checking descriptor")


# =============================================================================
# Exercise 4: Overriding Descriptor Behavior
# =============================================================================
# Demonstrate that overriding descriptors always intercept access.


class Overriding:
    """Overriding descriptor (has __set__)."""

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return f"Overriding.get:{instance.__dict__.get(self.name, 'NOT SET')}"

    def __set__(self, instance, value):
        instance.__dict__[self.name] = f"SET:{value}"


class TestOverriding:
    attr = Overriding()


# Test Exercise 4
obj = TestOverriding()

# Initial get (nothing set yet)
result = obj.attr
assert "NOT SET" in result

# Set through descriptor
obj.attr = 42
assert obj.__dict__['attr'] == "SET:42"

# Get goes through descriptor, not direct dict access
result = obj.attr
assert "SET:42" in result

# Even direct dict modification doesn't bypass descriptor on read
obj.__dict__['attr'] = "DIRECT"
result = obj.attr
assert "DIRECT" in result  # Descriptor still reads from dict

print("    Exercise 4 passed: Overriding descriptor behavior")


# =============================================================================
# Exercise 5: Nonoverriding Descriptor
# =============================================================================
# Demonstrate that nonoverriding descriptors can be shadowed.


class NonOverriding:
    """Nonoverriding descriptor (no __set__)."""

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return f"NonOverriding.get"


class TestNonOverriding:
    attr = NonOverriding()

    def __init__(self):
        pass  # Don't set attr


# Test Exercise 5
obj = TestNonOverriding()

# Initially, descriptor __get__ is called
assert obj.attr == "NonOverriding.get"

# Direct assignment creates instance attribute (no __set__ to intercept)
obj.attr = "shadowed"

# Now instance attribute shadows the descriptor
assert obj.attr == "shadowed"

# Delete instance attribute
del obj.attr

# Descriptor is back
assert obj.attr == "NonOverriding.get"

print("    Exercise 5 passed: Nonoverriding descriptor")


# =============================================================================
# Exercise 6: Read-Only Descriptor
# =============================================================================
# Create a descriptor that only allows setting once.


class ReadOnlyAfterSet:
    """Descriptor that becomes read-only after first set."""

    def __set_name__(self, owner, name):
        self.storage_name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self.storage_name)

    def __set__(self, instance, value):
        # TODO: If self.storage_name already in instance.__dict__,
        # raise AttributeError(f'{self.storage_name} is read-only')
        # Otherwise store the value
        pass


class Config:
    setting = ReadOnlyAfterSet()

    def __init__(self, setting):
        self.setting = setting


# Test Exercise 6
config = Config("production")
assert config.setting == "production"

try:
    config.setting = "development"
    assert False, "Should not allow modification"
except AttributeError:
    pass

assert config.setting == "production"

print("    Exercise 6 passed: Read-only descriptor")


# =============================================================================
# Exercise 7: Validated ABC with Template Method
# =============================================================================
# Create an abstract descriptor base class using template method pattern.


class Validated(abc.ABC):
    """Abstract descriptor with validation template method."""

    def __set_name__(self, owner, name):
        self.storage_name = name

    def __set__(self, instance, value):
        # TODO: Call self.validate(value) to get validated value
        # Store validated value in instance.__dict__[self.storage_name]
        pass

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self.storage_name)

    @abc.abstractmethod
    def validate(self, value) -> Any:
        """Validate and return the value, or raise ValueError."""


class PositiveNumber(Validated):
    """Validates positive numbers."""

    def validate(self, value):
        # TODO: Raise ValueError if value <= 0
        # Return value otherwise
        pass


class NonEmptyString(Validated):
    """Validates non-empty strings."""

    def validate(self, value):
        # TODO: Strip whitespace, raise ValueError if empty
        # Return stripped value
        pass


class Order:
    customer = NonEmptyString()
    amount = PositiveNumber()

    def __init__(self, customer, amount):
        self.customer = customer
        self.amount = amount


# Test Exercise 7
order = Order("  Alice  ", 100)
assert order.customer == "Alice"  # Whitespace stripped
assert order.amount == 100

try:
    order.customer = "   "
    assert False, "Should not allow blank customer"
except ValueError:
    pass

try:
    order.amount = -50
    assert False, "Should not allow negative amount"
except ValueError:
    pass

print("    Exercise 7 passed: Validated ABC")


# =============================================================================
# Exercise 8: Caching Descriptor
# =============================================================================
# Create a nonoverriding descriptor that caches computed values.

computation_count = 0


class Cached:
    """Nonoverriding descriptor that caches the result."""

    def __init__(self, func):
        self.func = func
        self.name = None

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        # TODO: If instance is None, return self
        # Otherwise:
        #   1. Call self.func(instance) to compute value
        #   2. Store in instance.__dict__[self.name] (this shadows descriptor)
        #   3. Return the value
        pass


class DataAnalysis:
    def __init__(self, data):
        self._data = data

    @Cached
    def total(self):
        global computation_count
        computation_count += 1
        return sum(self._data)


# Test Exercise 8
computation_count = 0
da = DataAnalysis([1, 2, 3, 4, 5])

# First access computes
result1 = da.total
assert result1 == 15
assert computation_count == 1

# Second access uses cache (descriptor shadowed)
result2 = da.total
assert result2 == 15
assert computation_count == 1  # No additional computation

# Cache is in __dict__
assert 'total' in da.__dict__

print("    Exercise 8 passed: Caching descriptor")


# =============================================================================
# Exercise 9: Descriptor with Default Value
# =============================================================================
# Create a descriptor that provides a default value.


class WithDefault:
    """Descriptor with a default value."""

    def __init__(self, default):
        self.default = default
        self.storage_name = None

    def __set_name__(self, owner, name):
        self.storage_name = name

    def __get__(self, instance, owner):
        # TODO: If instance is None, return self
        # Return value from instance.__dict__, or self.default if not present
        pass

    def __set__(self, instance, value):
        instance.__dict__[self.storage_name] = value


class Settings:
    theme = WithDefault("light")
    language = WithDefault("en")


# Test Exercise 9
s = Settings()
assert s.theme == "light"  # Default
assert s.language == "en"  # Default

s.theme = "dark"
assert s.theme == "dark"  # Set value
assert s.language == "en"  # Still default

print("    Exercise 9 passed: Descriptor with default")


# =============================================================================
# Exercise 10: Range Validator Descriptor
# =============================================================================
# Create a descriptor that validates values are within a range.


class InRange:
    """Descriptor that validates value is within [min_val, max_val]."""

    def __init__(self, min_val: float, max_val: float):
        self.min_val = min_val
        self.max_val = max_val
        self.storage_name = None

    def __set_name__(self, owner, name):
        self.storage_name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self.storage_name)

    def __set__(self, instance, value):
        # TODO: Raise ValueError if value < min_val or value > max_val
        # Include storage_name in error message
        # Otherwise store value
        pass


class Student:
    grade = InRange(0, 100)
    age = InRange(5, 100)

    def __init__(self, name, grade, age):
        self.name = name
        self.grade = grade
        self.age = age


# Test Exercise 10
student = Student("Alice", 85, 20)
assert student.grade == 85
assert student.age == 20

student.grade = 100
assert student.grade == 100

try:
    student.grade = 105
    assert False, "Should not allow grade > 100"
except ValueError as e:
    assert "grade" in str(e).lower()

try:
    student.age = 3
    assert False, "Should not allow age < 5"
except ValueError as e:
    assert "age" in str(e).lower()

print("    Exercise 10 passed: Range validator")


# =============================================================================
# Exercise 11: Methods as Descriptors
# =============================================================================
# Demonstrate that functions are descriptors.


class MyClass:
    def method(self):
        return "method called"


# Test Exercise 11
obj = MyClass()

# Function has __get__
assert hasattr(MyClass.method, '__get__')

# Via class: returns function
func = MyClass.method
assert callable(func)
assert 'function' in str(type(func))

# Via instance: returns bound method
bound = obj.method
assert 'method' in str(type(bound))

# Bound method has __self__ and __func__
assert bound.__self__ is obj
assert bound.__func__ is MyClass.method

# Calling bound method
assert bound() == "method called"

# Manual binding via __get__
manually_bound = MyClass.method.__get__(obj, MyClass)
assert manually_bound() == "method called"

print("    Exercise 11 passed: Methods as descriptors")


# =============================================================================
# Exercise 12: Descriptor that Transforms Values
# =============================================================================
# Create a descriptor that transforms values on get and set.


class Transformed:
    """Descriptor that applies transformations."""

    def __init__(self, on_set=None, on_get=None):
        self.on_set = on_set or (lambda x: x)
        self.on_get = on_get or (lambda x: x)
        self.storage_name = None

    def __set_name__(self, owner, name):
        self.storage_name = name

    def __get__(self, instance, owner):
        # TODO: If instance is None, return self
        # Get value from instance.__dict__
        # Apply self.on_get transformation and return
        pass

    def __set__(self, instance, value):
        # TODO: Apply self.on_set transformation to value
        # Store transformed value in instance.__dict__
        pass


class Document:
    # Store lowercase, display uppercase
    title = Transformed(
        on_set=lambda s: s.lower(),
        on_get=lambda s: s.upper()
    )

    def __init__(self, title):
        self.title = title


# Test Exercise 12
doc = Document("Hello World")
assert doc.__dict__['title'] == "hello world"  # Stored lowercase
assert doc.title == "HELLO WORLD"  # Retrieved uppercase

doc.title = "New Title"
assert doc.__dict__['title'] == "new title"
assert doc.title == "NEW TITLE"

print("    Exercise 12 passed: Transforming descriptor")


# =============================================================================
# Exercise 13: Descriptor with Delete Support
# =============================================================================
# Create a descriptor that handles deletion.

deleted_items: list[str] = []


class Deletable:
    """Descriptor that handles deletion."""

    def __set_name__(self, owner, name):
        self.storage_name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        if self.storage_name not in instance.__dict__:
            raise AttributeError(f'{self.storage_name} not set')
        return instance.__dict__[self.storage_name]

    def __set__(self, instance, value):
        instance.__dict__[self.storage_name] = value

    def __delete__(self, instance):
        # TODO: Append self.storage_name to deleted_items list
        # Delete from instance.__dict__
        pass


class Resource:
    name = Deletable()

    def __init__(self, name):
        self.name = name


# Test Exercise 13
deleted_items.clear()
r = Resource("test_resource")
assert r.name == "test_resource"

del r.name
assert "name" in deleted_items

try:
    _ = r.name
    assert False, "Should raise AttributeError after deletion"
except AttributeError:
    pass

print("    Exercise 13 passed: Descriptor with delete")


# =============================================================================
# Exercise 14: Class Attribute Access
# =============================================================================
# Properly handle class-level access in descriptors.


class InspectableDescriptor:
    """Descriptor that can be inspected at class level."""

    def __init__(self, doc="No documentation"):
        self.doc = doc
        self.storage_name = None

    def __set_name__(self, owner, name):
        self.storage_name = name

    def __get__(self, instance, owner):
        # TODO: If instance is None, return self (for class-level access)
        # Otherwise return from instance.__dict__
        pass

    def __set__(self, instance, value):
        instance.__dict__[self.storage_name] = value


class Model:
    field1 = InspectableDescriptor("First field")
    field2 = InspectableDescriptor("Second field")

    def __init__(self, field1, field2):
        self.field1 = field1
        self.field2 = field2


# Test Exercise 14
m = Model("value1", "value2")
assert m.field1 == "value1"
assert m.field2 == "value2"

# Class-level access returns descriptor
desc = Model.field1
assert isinstance(desc, InspectableDescriptor)
assert desc.doc == "First field"

desc2 = Model.field2
assert desc2.doc == "Second field"

print("    Exercise 14 passed: Class attribute access")


# =============================================================================
# Exercise 15: Multiple Descriptor Inheritance
# =============================================================================
# Create descriptors using inheritance hierarchy.


class BaseValidator:
    """Base validator descriptor."""

    def __set_name__(self, owner, name):
        self.storage_name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self.storage_name)

    def __set__(self, instance, value):
        self.validate(value)
        instance.__dict__[self.storage_name] = value

    def validate(self, value):
        pass  # Override in subclasses


class StringValidator(BaseValidator):
    """Validates that value is a string."""

    def validate(self, value):
        # TODO: Raise TypeError if not a string
        pass


class LengthValidator(StringValidator):
    """Validates string with length constraints."""

    def __init__(self, min_len=0, max_len=None):
        self.min_len = min_len
        self.max_len = max_len

    def validate(self, value):
        # TODO: Call super().validate(value) first
        # Then check length constraints
        pass


class Form:
    username = LengthValidator(min_len=3, max_len=20)
    bio = LengthValidator(max_len=100)

    def __init__(self, username, bio=""):
        self.username = username
        self.bio = bio


# Test Exercise 15
form = Form("alice", "Hello, I'm Alice!")
assert form.username == "alice"
assert form.bio == "Hello, I'm Alice!"

try:
    form.username = "ab"  # Too short
    assert False, "Should not allow username < 3 chars"
except ValueError:
    pass

try:
    form.username = "a" * 25  # Too long
    assert False, "Should not allow username > 20 chars"
except ValueError:
    pass

try:
    form.username = 123  # Not a string
    assert False, "Should not allow non-string"
except TypeError:
    pass

print("    Exercise 15 passed: Descriptor inheritance")


# =============================================================================
print("\n" + "=" * 60)
print("Congratulations! All Chapter 22 exercises completed!")
print("=" * 60)
