"""
Chapter 5: Data Class Builders - Exercises
==========================================

Complete each exercise by replacing the `None` or `...` placeholders.
Run this file to check your answers with the assertions.
"""

from collections import namedtuple
from typing import NamedTuple
from dataclasses import dataclass, field, asdict, astuple, replace, fields

# =============================================================================
# Exercise 1: collections.namedtuple Basics
# =============================================================================
# Create and use a simple namedtuple

# TODO: Create a namedtuple called 'Point' with fields 'x' and 'y'
Point = None

# TODO: Create an instance with x=3, y=4
p = None

# TODO: Access the fields
x_value = None
y_value = None

# TODO: Convert to dict using _asdict()
point_dict = None

# TODO: Create a new point with x replaced by 10 (use _replace)
new_point = None

assert Point is not None
assert p.x == 3 and p.y == 4
assert x_value == 3 and y_value == 4
assert point_dict == {'x': 3, 'y': 4}
assert new_point.x == 10 and new_point.y == 4
print("✓ Exercise 1 passed: namedtuple Basics")


# =============================================================================
# Exercise 2: namedtuple with Defaults
# =============================================================================
# Create a namedtuple with default values

# TODO: Create a namedtuple 'HTTPResponse' with:
# - status (int) - no default
# - body (str) - default: ''
# - headers (no default value is tricky, we'll make it optional)
# Use the defaults parameter
HTTPResponse = None

# TODO: Create an instance with just status=200
response = None

# TODO: Create an instance with status=404, body='Not Found'
error_response = None

assert response.status == 200
assert response.body == ''
assert error_response.status == 404
assert error_response.body == 'Not Found'
print("✓ Exercise 2 passed: namedtuple with Defaults")


# =============================================================================
# Exercise 3: typing.NamedTuple with Methods
# =============================================================================
# Create a NamedTuple using class syntax with custom methods

# TODO: Create a NamedTuple class 'Vector' with:
# - x: float
# - y: float
# - A method 'magnitude' that returns sqrt(x^2 + y^2)
# - A method '__str__' that returns 'Vector(x, y)' format

import math

class Vector(NamedTuple):
    # TODO: Define fields and methods
    ...
    pass


v = Vector(3.0, 4.0)
assert v.x == 3.0
assert v.y == 4.0
assert v.magnitude() == 5.0
assert str(v) == 'Vector(3.0, 4.0)'
assert isinstance(v, tuple)  # Still a tuple!
print("✓ Exercise 3 passed: typing.NamedTuple with Methods")


# =============================================================================
# Exercise 4: Basic @dataclass
# =============================================================================
# Create a simple dataclass

# TODO: Create a dataclass 'Book' with:
# - title: str
# - author: str
# - year: int
# - pages: int (default 0)

@dataclass
class Book:
    # TODO: Define fields
    ...
    pass


book = Book('Fluent Python', 'Luciano Ramalho', 2022)
assert book.title == 'Fluent Python'
assert book.author == 'Luciano Ramalho'
assert book.year == 2022
assert book.pages == 0  # Default value

book.pages = 500  # Should be mutable
assert book.pages == 500
print("✓ Exercise 4 passed: Basic @dataclass")


# =============================================================================
# Exercise 5: Frozen Dataclass
# =============================================================================
# Create an immutable dataclass

# TODO: Create a frozen dataclass 'Config' with:
# - host: str
# - port: int (default 8080)
# - debug: bool (default False)

@dataclass(frozen=True)
class Config:
    # TODO: Define fields
    ...
    pass


config = Config('localhost')
assert config.host == 'localhost'
assert config.port == 8080
assert config.debug == False

# Verify it's immutable
try:
    config.port = 9000
    is_frozen = False
except Exception:
    is_frozen = True

# Verify it's hashable
try:
    hash(config)
    is_hashable = True
except TypeError:
    is_hashable = False

assert is_frozen, "Config should be immutable"
assert is_hashable, "Frozen dataclass should be hashable"
print("✓ Exercise 5 passed: Frozen Dataclass")


# =============================================================================
# Exercise 6: Dataclass with field()
# =============================================================================
# Use field() for mutable defaults and options

# TODO: Create a dataclass 'ShoppingCart' with:
# - customer: str
# - items: list[str] - default empty list (use field(default_factory=list))
# - discount: float - default 0.0
# - _internal_id: str - default '', hidden from repr

@dataclass
class ShoppingCart:
    # TODO: Define fields
    ...
    pass


cart1 = ShoppingCart('Alice')
cart2 = ShoppingCart('Bob')

cart1.items.append('Widget')

# Each cart should have its own list
assert cart1.items == ['Widget']
assert cart2.items == []  # Should NOT be ['Widget']!

# Internal field should not appear in repr
repr_str = repr(cart1)
assert '_internal_id' not in repr_str
print("✓ Exercise 6 passed: Dataclass with field()")


# =============================================================================
# Exercise 7: __post_init__ for Validation
# =============================================================================
# Use __post_init__ to validate and compute fields

# TODO: Create a dataclass 'Rectangle' with:
# - width: float
# - height: float
# - area: float (not in __init__, computed in __post_init__)
# Validate that width and height are positive

@dataclass
class Rectangle:
    # TODO: Define fields and __post_init__
    ...
    pass


rect = Rectangle(3.0, 4.0)
assert rect.width == 3.0
assert rect.height == 4.0
assert rect.area == 12.0

# Test validation
try:
    bad_rect = Rectangle(-1.0, 4.0)
    validation_works = False
except ValueError:
    validation_works = True

assert validation_works, "Should raise ValueError for negative dimensions"
print("✓ Exercise 7 passed: __post_init__ Validation")


# =============================================================================
# Exercise 8: Dataclass with Ordering
# =============================================================================
# Create a dataclass that can be sorted

# TODO: Create a dataclass 'Version' with:
# - major: int
# - minor: int
# - patch: int (default 0)
# Enable ordering with order=True

@dataclass(order=True)
class Version:
    # TODO: Define fields
    ...
    pass


v1 = Version(1, 0, 0)
v2 = Version(1, 0, 1)
v3 = Version(2, 0, 0)

assert v1 < v2 < v3
assert sorted([v3, v1, v2]) == [v1, v2, v3]
print("✓ Exercise 8 passed: Dataclass with Ordering")


# =============================================================================
# Exercise 9: Dataclass Utility Functions
# =============================================================================
# Use asdict, astuple, replace, and fields

@dataclass
class User:
    name: str
    email: str
    active: bool = True


user = User('Alice', 'alice@example.com')

# TODO: Convert to dict
user_dict = None

# TODO: Convert to tuple
user_tuple = None

# TODO: Create a copy with email changed to 'newalice@example.com'
updated_user = None

# TODO: Get field names as a list
field_names = None

assert user_dict == {'name': 'Alice', 'email': 'alice@example.com', 'active': True}
assert user_tuple == ('Alice', 'alice@example.com', True)
assert updated_user.email == 'newalice@example.com'
assert updated_user.name == 'Alice'  # Other fields unchanged
assert field_names == ['name', 'email', 'active']
print("✓ Exercise 9 passed: Dataclass Utility Functions")


# =============================================================================
# Exercise 10: Dataclass Inheritance
# =============================================================================
# Create dataclasses with inheritance

# TODO: Create a base dataclass 'Person' with name: str, age: int
# TODO: Create a derived dataclass 'Employee' that adds:
# - employee_id: str
# - department: str (default 'General')

@dataclass
class Person:
    # TODO: Define fields
    ...
    pass


@dataclass
class Employee(Person):
    # TODO: Define fields
    ...
    pass


emp = Employee('Alice', 30, 'E123')
assert emp.name == 'Alice'
assert emp.age == 30
assert emp.employee_id == 'E123'
assert emp.department == 'General'

emp2 = Employee('Bob', 25, 'E456', 'Engineering')
assert emp2.department == 'Engineering'
print("✓ Exercise 10 passed: Dataclass Inheritance")


# =============================================================================
# Exercise 11: Compare namedtuple vs NamedTuple vs dataclass
# =============================================================================
# Understand the differences

# All three representing the same concept
NT1 = namedtuple('Person1', ['name', 'age'])
class Person2(NamedTuple):
    name: str
    age: int

@dataclass
class Person3:
    name: str
    age: int


p1 = NT1('Alice', 30)
p2 = Person2('Alice', 30)
p3 = Person3('Alice', 30)

# TODO: Which are tuples?
nt1_is_tuple = None  # True or False
person2_is_tuple = None
person3_is_tuple = None

# TODO: Which are mutable?
p1_mutable = None  # Try p1.age = 31
p2_mutable = None
p3_mutable = None

# TODO: Which support indexing like p[0]?
nt1_indexable = None
person2_indexable = None
person3_indexable = None

assert nt1_is_tuple == True
assert person2_is_tuple == True
assert person3_is_tuple == False

assert p1_mutable == False
assert p2_mutable == False
assert p3_mutable == True

assert nt1_indexable == True
assert person2_indexable == True
assert person3_indexable == False
print("✓ Exercise 11 passed: Comparison")


# =============================================================================
# Exercise 12: Practical - JSON-Serializable Dataclass
# =============================================================================
# Create a dataclass that can be easily serialized to JSON

import json
from datetime import datetime

@dataclass
class Event:
    name: str
    timestamp: str  # ISO format string
    data: dict = field(default_factory=dict)

    @classmethod
    def create(cls, name: str, **data) -> 'Event':
        """Factory method to create event with current timestamp."""
        # TODO: Implement - use datetime.now().isoformat() for timestamp
        ...
        pass

    def to_json(self) -> str:
        """Convert to JSON string."""
        # TODO: Implement using asdict and json.dumps
        ...
        pass

    @classmethod
    def from_json(cls, json_str: str) -> 'Event':
        """Create from JSON string."""
        # TODO: Implement using json.loads
        ...
        pass


# Test factory method
event = Event.create('click', x=100, y=200)
assert event.name == 'click'
assert event.data == {'x': 100, 'y': 200}
assert 'T' in event.timestamp  # ISO format has 'T'

# Test serialization
json_str = event.to_json()
parsed = json.loads(json_str)
assert parsed['name'] == 'click'
assert parsed['data']['x'] == 100

# Test deserialization
restored = Event.from_json(json_str)
assert restored.name == event.name
assert restored.data == event.data
print("✓ Exercise 12 passed: JSON-Serializable Dataclass")


# =============================================================================
# Exercise 13: Practical - Immutable Configuration
# =============================================================================
# Create a configuration system using frozen dataclass

@dataclass(frozen=True)
class DatabaseConfig:
    host: str
    port: int = 5432
    database: str = 'default'
    user: str = 'admin'
    password: str = ''

    @classmethod
    def from_dict(cls, config: dict) -> 'DatabaseConfig':
        """Create from dictionary, ignoring unknown keys."""
        # TODO: Implement - only pass known field names
        # Hint: Use fields() to get valid field names
        ...
        pass

    @property
    def connection_string(self) -> str:
        """Generate connection string."""
        # TODO: Return 'postgresql://user:password@host:port/database'
        ...
        pass


# Test from_dict with extra keys
config_dict = {
    'host': 'localhost',
    'port': 5432,
    'database': 'mydb',
    'unknown_key': 'ignored',
}
db_config = DatabaseConfig.from_dict(config_dict)
assert db_config.host == 'localhost'
assert db_config.database == 'mydb'

# Test connection_string property
assert db_config.connection_string == 'postgresql://admin:@localhost:5432/mydb'

# Should be hashable (can use in sets/dict keys)
config_set = {db_config}
assert db_config in config_set
print("✓ Exercise 13 passed: Immutable Configuration")


# =============================================================================
# Exercise 14: Practical - Builder Pattern with Dataclass
# =============================================================================
# Implement a builder pattern for complex object construction

@dataclass
class Email:
    sender: str
    recipients: list = field(default_factory=list)
    cc: list = field(default_factory=list)
    subject: str = ''
    body: str = ''


class EmailBuilder:
    """Builder for constructing Email objects fluently."""

    def __init__(self, sender: str):
        # TODO: Initialize with sender, empty lists for recipients/cc
        ...
        pass

    def to(self, *recipients) -> 'EmailBuilder':
        """Add recipients."""
        # TODO: Add recipients and return self for chaining
        ...
        pass

    def cc(self, *addresses) -> 'EmailBuilder':
        """Add CC addresses."""
        # TODO: Add CC addresses and return self
        ...
        pass

    def with_subject(self, subject: str) -> 'EmailBuilder':
        """Set subject."""
        # TODO: Set subject and return self
        ...
        pass

    def with_body(self, body: str) -> 'EmailBuilder':
        """Set body."""
        # TODO: Set body and return self
        ...
        pass

    def build(self) -> Email:
        """Build the final Email object."""
        # TODO: Create and return Email with all set values
        ...
        pass


# Test fluent builder
email = (EmailBuilder('sender@example.com')
         .to('alice@example.com', 'bob@example.com')
         .cc('manager@example.com')
         .with_subject('Hello')
         .with_body('This is a test email.')
         .build())

assert email.sender == 'sender@example.com'
assert email.recipients == ['alice@example.com', 'bob@example.com']
assert email.cc == ['manager@example.com']
assert email.subject == 'Hello'
assert email.body == 'This is a test email.'
print("✓ Exercise 14 passed: Builder Pattern")


# =============================================================================
# Exercise 15: Practical - Value Object with Validation
# =============================================================================
# Create a validated value object using frozen dataclass

@dataclass(frozen=True)
class Money:
    """
    Immutable money value object.

    Validates:
    - amount must be non-negative
    - currency must be 3 uppercase letters
    """
    amount: float
    currency: str

    def __post_init__(self):
        # TODO: Validate amount >= 0
        # TODO: Validate currency is 3 uppercase letters
        # Note: In frozen dataclass, use object.__setattr__ to set values
        # after normalization if needed
        ...
        pass

    def __add__(self, other: 'Money') -> 'Money':
        """Add two money values of the same currency."""
        # TODO: Implement - raise ValueError if currencies don't match
        ...
        pass

    def __mul__(self, factor: float) -> 'Money':
        """Multiply money by a factor."""
        # TODO: Implement
        ...
        pass


m1 = Money(100.0, 'USD')
m2 = Money(50.0, 'USD')
m3 = m1 + m2
assert m3.amount == 150.0
assert m3.currency == 'USD'

m4 = m1 * 2
assert m4.amount == 200.0

# Test validation
try:
    bad_money = Money(-100, 'USD')
    negative_failed = False
except ValueError:
    negative_failed = True

try:
    bad_currency = Money(100, 'usd')  # lowercase
    currency_failed = False
except ValueError:
    currency_failed = True

try:
    m1 + Money(100, 'EUR')  # Different currencies
    currency_mismatch_failed = False
except ValueError:
    currency_mismatch_failed = True

assert negative_failed, "Should reject negative amounts"
assert currency_failed, "Should reject non-uppercase currency"
assert currency_mismatch_failed, "Should reject adding different currencies"
print("✓ Exercise 15 passed: Validated Value Object")


# =============================================================================
# All exercises completed!
# =============================================================================
print("\n" + "=" * 60)
print("🎉 Congratulations! All Chapter 5 exercises passed!")
print("=" * 60)
