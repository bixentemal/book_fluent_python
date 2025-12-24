"""
Chapter 23: Class Metaprogramming - Exercises
==============================================

Practice using class factories, __init_subclass__, class
decorators, and metaclasses for dynamic class creation.

Run this file to check your implementations.
"""

from typing import Any, get_type_hints
from collections import OrderedDict
import abc

# =============================================================================
# Exercise 1: Create a Class with type()
# =============================================================================
# Use type() to dynamically create a class.


def create_point_class() -> type:
    """Create a Point class using type().

    The class should have:
    - __init__(self, x, y) that sets self.x and self.y
    - __repr__(self) that returns "Point(x=<x>, y=<y>)"
    """
    # TODO: Define __init__ function
    # TODO: Define __repr__ function
    # TODO: Use type() to create and return the class
    pass


# Test Exercise 1
Point = create_point_class()
p = Point(3, 4)
assert p.x == 3
assert p.y == 4
assert repr(p) == "Point(x=3, y=4)"

print("    Exercise 1 passed: Create class with type()")


# =============================================================================
# Exercise 2: Simple Class Factory
# =============================================================================
# Create a factory function that generates record-like classes.


def record_factory(cls_name: str, field_names: str) -> type:
    """Create a simple record class.

    Args:
        cls_name: Name of the class
        field_names: Space-separated field names

    Returns:
        A new class with __init__, __repr__, and __iter__
    """
    fields = tuple(field_names.split())

    # TODO: Define __init__ that accepts *args and sets each field
    # TODO: Define __repr__ that shows class name and field=value pairs
    # TODO: Define __iter__ that yields field values
    # TODO: Create class with __slots__ = fields
    pass


# Test Exercise 2
Dog = record_factory('Dog', 'name weight owner')
rex = Dog('Rex', 30, 'Bob')
assert rex.name == 'Rex'
assert rex.weight == 30
assert rex.owner == 'Bob'
assert repr(rex) == "Dog(name='Rex', weight=30, owner='Bob')"
assert list(rex) == ['Rex', 30, 'Bob']

# __slots__ should prevent arbitrary attributes
try:
    rex.age = 5
    assert False, "Should not allow setting undefined attributes"
except AttributeError:
    pass

print("    Exercise 2 passed: Record factory")


# =============================================================================
# Exercise 3: Basic __init_subclass__
# =============================================================================
# Use __init_subclass__ to register subclasses.

registered_plugins: dict[str, type] = {}


class Plugin:
    """Base class that registers all subclasses."""

    def __init_subclass__(cls, **kwargs):
        # TODO: Call super().__init_subclass__(**kwargs)
        # TODO: Add cls to registered_plugins using cls.__name__ as key
        pass


class AudioPlugin(Plugin):
    pass


class VideoPlugin(Plugin):
    pass


# Test Exercise 3
assert 'AudioPlugin' in registered_plugins
assert 'VideoPlugin' in registered_plugins
assert registered_plugins['AudioPlugin'] is AudioPlugin
assert registered_plugins['VideoPlugin'] is VideoPlugin

print("    Exercise 3 passed: __init_subclass__ registration")


# =============================================================================
# Exercise 4: __init_subclass__ with Parameters
# =============================================================================
# Use __init_subclass__ with keyword arguments.

tagged_classes: dict[str, type] = {}


class Tagged:
    """Base class that accepts a 'tag' parameter."""

    def __init_subclass__(cls, tag: str = None, **kwargs):
        # TODO: Call super().__init_subclass__(**kwargs)
        # TODO: If tag is provided, add to tagged_classes
        # TODO: Also set cls.tag = tag
        pass


class Important(Tagged, tag='priority'):
    pass


class Archived(Tagged, tag='old'):
    pass


class Untagged(Tagged):
    pass


# Test Exercise 4
assert tagged_classes.get('priority') is Important
assert tagged_classes.get('old') is Archived
assert Important.tag == 'priority'
assert Archived.tag == 'old'
assert getattr(Untagged, 'tag', None) is None

print("    Exercise 4 passed: __init_subclass__ with parameters")


# =============================================================================
# Exercise 5: __init_subclass__ for Validation
# =============================================================================
# Use __init_subclass__ to validate subclass definitions.


class RequiredMethods:
    """Base class that requires subclasses to implement certain methods."""

    required = ['process', 'validate']

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        # TODO: Check if all methods in cls.required are defined in cls
        # TODO: Raise TypeError if any required method is missing
        # Hint: Use hasattr() or check cls.__dict__
        pass


# Test Exercise 5
try:
    class Incomplete(RequiredMethods):
        def process(self):
            pass
        # Missing validate!
    assert False, "Should raise TypeError for missing method"
except TypeError:
    pass


class Complete(RequiredMethods):
    def process(self):
        return "processing"

    def validate(self):
        return True


assert Complete().process() == "processing"
assert Complete().validate() is True

print("    Exercise 5 passed: __init_subclass__ validation")


# =============================================================================
# Exercise 6: Simple Class Decorator
# =============================================================================
# Create a class decorator that adds a method.


def add_greet(cls: type) -> type:
    """Class decorator that adds a greet() method."""
    # TODO: Define a greet method that returns f"Hello from {cls.__name__}!"
    # TODO: Add the method to the class
    # TODO: Return the class
    pass


@add_greet
class Greeter:
    pass


# Test Exercise 6
g = Greeter()
assert g.greet() == "Hello from Greeter!"

print("    Exercise 6 passed: Simple class decorator")


# =============================================================================
# Exercise 7: Class Decorator with Parameters
# =============================================================================
# Create a parameterized class decorator.


def with_repr(*attrs: str):
    """Class decorator factory that adds __repr__ showing specified attrs."""

    def decorator(cls: type) -> type:
        # TODO: Define __repr__ that shows cls.__name__ and listed attributes
        # TODO: Add __repr__ to the class
        # TODO: Return the class
        pass

    return decorator


@with_repr('name', 'value')
class Config:
    def __init__(self, name, value, secret):
        self.name = name
        self.value = value
        self.secret = secret  # Not shown in repr


# Test Exercise 7
c = Config('debug', True, 'password123')
assert repr(c) == "Config(name='debug', value=True)"
assert 'secret' not in repr(c)
assert 'password' not in repr(c)

print("    Exercise 7 passed: Parameterized class decorator")


# =============================================================================
# Exercise 8: Class Decorator that Adds Validation
# =============================================================================
# Create a decorator that adds type checking based on annotations.


def checked(cls: type) -> type:
    """Decorator that adds type checking to __init__."""
    original_init = cls.__init__

    def new_init(self, **kwargs):
        hints = get_type_hints(cls.__init__)
        for name, value in kwargs.items():
            if name in hints and not isinstance(value, hints[name]):
                raise TypeError(
                    f"{name} must be {hints[name].__name__}, "
                    f"got {type(value).__name__}"
                )
        original_init(self, **kwargs)

    # TODO: Replace cls.__init__ with new_init
    # TODO: Return the class
    pass


@checked
class Person:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age


# Test Exercise 8
p = Person(name="Alice", age=30)
assert p.name == "Alice"
assert p.age == 30

try:
    Person(name="Bob", age="thirty")
    assert False, "Should raise TypeError"
except TypeError as e:
    assert "age" in str(e)

print("    Exercise 8 passed: Type-checking decorator")


# =============================================================================
# Exercise 9: Basic Metaclass
# =============================================================================
# Create a simple metaclass that logs class creation.

created_classes: list[str] = []


class LoggingMeta(type):
    """Metaclass that logs when classes are created."""

    def __new__(mcs, name, bases, namespace):
        # TODO: Append the class name to created_classes
        # TODO: Call super().__new__ and return the result
        pass


class LoggedBase(metaclass=LoggingMeta):
    pass


class LoggedChild(LoggedBase):
    pass


# Test Exercise 9
assert 'LoggedBase' in created_classes
assert 'LoggedChild' in created_classes

print("    Exercise 9 passed: Basic metaclass")


# =============================================================================
# Exercise 10: Metaclass that Adds Methods
# =============================================================================
# Create a metaclass that injects methods into classes.


class AutoMethodsMeta(type):
    """Metaclass that adds automatic methods."""

    def __new__(mcs, name, bases, namespace):
        # TODO: Add a 'describe' method that returns f"I am a {name} instance"
        # TODO: Add a 'classname' classmethod that returns name
        # TODO: Call super().__new__ and return
        pass


class AutoBase(metaclass=AutoMethodsMeta):
    pass


class AutoChild(AutoBase):
    pass


# Test Exercise 10
obj = AutoChild()
assert obj.describe() == "I am a AutoChild instance"
assert AutoChild.classname() == "AutoChild"
assert AutoBase().describe() == "I am a AutoBase instance"

print("    Exercise 10 passed: Metaclass adding methods")


# =============================================================================
# Exercise 11: Metaclass with __prepare__
# =============================================================================
# Use __prepare__ to track attribute definition order.


class OrderTrackingDict(dict):
    """Dict that tracks insertion order of non-dunder keys."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.order = []

    def __setitem__(self, key, value):
        if not (key.startswith('__') and key.endswith('__')):
            if key not in self:
                self.order.append(key)
        super().__setitem__(key, value)


class OrderedMeta(type):
    """Metaclass that records attribute definition order."""

    @classmethod
    def __prepare__(mcs, name, bases, **kwargs):
        # TODO: Return an OrderTrackingDict instance
        pass

    def __new__(mcs, name, bases, namespace):
        # TODO: Get the order from namespace (if it's OrderTrackingDict)
        # TODO: Add _field_order attribute to the class
        # TODO: Call super().__new__ with dict(namespace)
        pass


class OrderedBase(metaclass=OrderedMeta):
    pass


class Fields(OrderedBase):
    first = 1
    second = 2
    third = 3


# Test Exercise 11
assert hasattr(Fields, '_field_order')
assert Fields._field_order == ['first', 'second', 'third']

print("    Exercise 11 passed: Metaclass with __prepare__")


# =============================================================================
# Exercise 12: Metaclass for Singleton Pattern
# =============================================================================
# Create a metaclass that implements singleton pattern.


class SingletonMeta(type):
    """Metaclass that makes classes singletons."""

    _instances: dict[type, Any] = {}

    def __call__(cls, *args, **kwargs):
        # TODO: If cls not in _instances, create instance with super().__call__
        # TODO: Store in _instances
        # TODO: Return the instance from _instances
        pass


class Singleton(metaclass=SingletonMeta):
    pass


class Database(Singleton):
    def __init__(self, url="default"):
        self.url = url


# Test Exercise 12
db1 = Database("postgres://localhost")
db2 = Database("mysql://localhost")  # Ignored, returns same instance
assert db1 is db2
assert db1.url == "postgres://localhost"  # First call's args used

print("    Exercise 12 passed: Singleton metaclass")


# =============================================================================
# Exercise 13: Metaclass with __slots__ Configuration
# =============================================================================
# Create a metaclass that auto-generates __slots__.


class AutoSlotsMeta(type):
    """Metaclass that creates __slots__ from annotations."""

    def __new__(mcs, name, bases, namespace):
        # Skip if __slots__ already defined
        if '__slots__' in namespace:
            return super().__new__(mcs, name, bases, namespace)

        # TODO: Get __annotations__ from namespace
        # TODO: Create __slots__ tuple from annotation keys
        # TODO: Add __slots__ to namespace
        # TODO: Return super().__new__(...)
        pass


class SlottedBase(metaclass=AutoSlotsMeta):
    __slots__ = ()


class SlottedPoint(SlottedBase):
    x: float
    y: float

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y


# Test Exercise 13
p = SlottedPoint(1.0, 2.0)
assert p.x == 1.0
assert p.y == 2.0
assert SlottedPoint.__slots__ == ('x', 'y')

try:
    p.z = 3.0  # Should fail - no __dict__
    assert False, "Should not allow undefined attributes"
except AttributeError:
    pass

print("    Exercise 13 passed: Auto __slots__ metaclass")


# =============================================================================
# Exercise 14: Combining Metaclass with ABC
# =============================================================================
# Create a metaclass that works with abc.ABC.


class ValidatedABCMeta(abc.ABCMeta):
    """Metaclass combining ABC features with custom validation."""

    def __new__(mcs, name, bases, namespace):
        cls = super().__new__(mcs, name, bases, namespace)

        # TODO: If cls is not abstract (no abstractmethods)
        # Check that 'version' class attribute exists
        # Raise TypeError if missing
        # Hint: Check len(cls.__abstractmethods__) == 0
        pass

        return cls


class VersionedBase(abc.ABC, metaclass=ValidatedABCMeta):
    @abc.abstractmethod
    def process(self):
        pass


# Test Exercise 14
try:
    class MissingVersion(VersionedBase):
        def process(self):
            pass
        # Missing version!
    assert False, "Should raise TypeError"
except TypeError:
    pass


class Versioned(VersionedBase):
    version = "1.0"

    def process(self):
        return f"Processing v{self.version}"


assert Versioned().process() == "Processing v1.0"

print("    Exercise 14 passed: Combined ABC metaclass")


# =============================================================================
# Exercise 15: Class Factory with Descriptors
# =============================================================================
# Create a complete class factory with validation descriptors.


class ValidatedField:
    """Descriptor for type-validated fields."""

    def __init__(self, name: str, field_type: type):
        self.name = name
        self.field_type = field_type
        self.storage_name = f'_{name}'

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance, self.storage_name, None)

    def __set__(self, instance, value):
        if not isinstance(value, self.field_type):
            raise TypeError(
                f"{self.name} must be {self.field_type.__name__}"
            )
        setattr(instance, self.storage_name, value)


def validated_class(cls_name: str, **fields: type) -> type:
    """Create a class with validated fields.

    Args:
        cls_name: Name of the class
        **fields: field_name=field_type pairs

    Returns:
        A new class with ValidatedField descriptors
    """
    # TODO: Create namespace dict
    # TODO: Add ValidatedField for each field
    # TODO: Create __slots__ for storage attributes
    # TODO: Create __init__ that accepts **kwargs and sets each field
    # TODO: Create __repr__
    # TODO: Use type() to create and return the class
    pass


# Test Exercise 15
Person = validated_class('Person', name=str, age=int)
p = Person(name="Alice", age=30)
assert p.name == "Alice"
assert p.age == 30
assert "Person" in repr(p)

try:
    Person(name="Bob", age="thirty")
    assert False, "Should raise TypeError"
except TypeError:
    pass

try:
    p.age = "old"
    assert False, "Should raise TypeError"
except TypeError:
    pass

print("    Exercise 15 passed: Validated class factory")


# =============================================================================
print("\n" + "=" * 60)
print("Congratulations! All Chapter 23 exercises completed!")
print("=" * 60)
