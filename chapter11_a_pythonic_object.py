"""
Chapter 11: A Pythonic Object - Exercises
==========================================

Complete each exercise by replacing the `None` or `...` placeholders.
Run this file to check your answers with the assertions.
"""

from __future__ import annotations
from array import array
import math


# =============================================================================
# Exercise 1: Implement __repr__ and __str__
# =============================================================================
# Create a Point class with proper string representations

class Point:
    """A 2D point with x and y coordinates."""

    def __init__(self, x: float, y: float):
        self.x = float(x)
        self.y = float(y)

    def __repr__(self) -> str:
        """
        Return unambiguous representation for debugging.
        Format: Point(x, y) where x and y show their repr

        TODO: Implement
        Hint: Use type(self).__name__ to get class name
        """
        ...
        pass

    def __str__(self) -> str:
        """
        Return human-readable representation.
        Format: (x, y)

        TODO: Implement
        """
        ...
        pass


p = Point(3, 4)
assert repr(p) == "Point(3.0, 4.0)", f"Got: {repr(p)}"
assert str(p) == "(3.0, 4.0)", f"Got: {str(p)}"

# repr should work for recreating the object
p_clone = eval(repr(p))
assert p_clone.x == p.x and p_clone.y == p.y

print("✓ Exercise 1 passed: __repr__ and __str__")


# =============================================================================
# Exercise 2: Make Object Iterable
# =============================================================================
# Implement __iter__ to support unpacking and iteration

class Vector2d:
    """A 2D vector."""

    def __init__(self, x: float, y: float):
        self.x = float(x)
        self.y = float(y)

    def __repr__(self) -> str:
        return f"Vector2d({self.x!r}, {self.y!r})"

    def __iter__(self):
        """
        Make Vector2d iterable, yielding x then y.

        TODO: Implement
        Hint: Use a generator expression or yield statements
        """
        ...
        pass


v = Vector2d(3, 4)

# Test unpacking
x, y = v
assert x == 3.0 and y == 4.0, f"Unpacking failed: got {x}, {y}"

# Test conversion to tuple/list
assert tuple(v) == (3.0, 4.0)
assert list(v) == [3.0, 4.0]

# Test iteration
components = [c for c in v]
assert components == [3.0, 4.0]

print("✓ Exercise 2 passed: Make Object Iterable")


# =============================================================================
# Exercise 3: Implement __abs__ and __bool__
# =============================================================================
# Add magnitude and boolean behavior

class Vector2d_v2:
    """A 2D vector with magnitude and boolean support."""

    def __init__(self, x: float, y: float):
        self.x = float(x)
        self.y = float(y)

    def __repr__(self) -> str:
        return f"Vector2d_v2({self.x!r}, {self.y!r})"

    def __iter__(self):
        return iter((self.x, self.y))

    def __abs__(self) -> float:
        """
        Return the magnitude (length) of the vector.

        TODO: Implement
        Hint: Use math.hypot(x, y) for the hypotenuse
        """
        ...
        pass

    def __bool__(self) -> bool:
        """
        Return True if vector has non-zero magnitude.

        TODO: Implement
        Hint: Zero vector should be falsy
        """
        ...
        pass


v1 = Vector2d_v2(3, 4)
assert abs(v1) == 5.0, f"Expected 5.0, got {abs(v1)}"
assert bool(v1) == True

v0 = Vector2d_v2(0, 0)
assert abs(v0) == 0.0
assert bool(v0) == False

# Test in boolean context
if v1:
    passed = True
else:
    passed = False
assert passed, "Non-zero vector should be truthy"

print("✓ Exercise 3 passed: __abs__ and __bool__")


# =============================================================================
# Exercise 4: Implement __eq__ and __hash__
# =============================================================================
# Make the object hashable for use in sets and as dict keys

class Vector2d_v3:
    """A hashable 2D vector."""

    def __init__(self, x: float, y: float):
        self._x = float(x)  # Use "private" attributes
        self._y = float(y)

    @property
    def x(self) -> float:
        return self._x

    @property
    def y(self) -> float:
        return self._y

    def __repr__(self) -> str:
        return f"Vector2d_v3({self.x!r}, {self.y!r})"

    def __iter__(self):
        return iter((self.x, self.y))

    def __eq__(self, other) -> bool:
        """
        Two vectors are equal if their components match.

        TODO: Implement
        Hint: Compare as tuples for simplicity
        """
        ...
        pass

    def __hash__(self) -> int:
        """
        Return hash based on components.

        TODO: Implement
        Hint: Hash the tuple of components
        """
        ...
        pass


v1 = Vector2d_v3(3, 4)
v2 = Vector2d_v3(3, 4)
v3 = Vector2d_v3(5, 6)

# Test equality
assert v1 == v2, "Equal vectors should be equal"
assert not (v1 == v3), "Different vectors should not be equal"

# Test hash
assert hash(v1) == hash(v2), "Equal objects must have equal hashes"

# Test use in set
vector_set = {v1, v2, v3}
assert len(vector_set) == 2, f"Set should have 2 unique vectors, got {len(vector_set)}"

# Test use as dict key
vector_dict = {v1: "first", v3: "second"}
assert vector_dict[v2] == "first", "v2 should find v1's value (equal vectors)"

print("✓ Exercise 4 passed: __eq__ and __hash__")


# =============================================================================
# Exercise 5: Read-Only Properties
# =============================================================================
# Make attributes truly read-only using properties with name mangling

class ImmutablePoint:
    """An immutable 2D point."""

    def __init__(self, x: float, y: float):
        # TODO: Store x and y as private attributes using double underscore
        # e.g., self.__x = ...
        ...
        pass

    @property
    def x(self) -> float:
        """
        TODO: Return the private x attribute
        """
        ...
        pass

    @property
    def y(self) -> float:
        """
        TODO: Return the private y attribute
        """
        ...
        pass

    def __repr__(self) -> str:
        return f"ImmutablePoint({self.x!r}, {self.y!r})"

    def __iter__(self):
        return iter((self.x, self.y))

    def __eq__(self, other):
        return tuple(self) == tuple(other)

    def __hash__(self):
        return hash((self.x, self.y))


ip = ImmutablePoint(3, 4)
assert ip.x == 3.0
assert ip.y == 4.0

# Verify that setting raises an error
try:
    ip.x = 10
    assert False, "Should not be able to set x"
except AttributeError:
    pass  # Expected

try:
    ip.y = 10
    assert False, "Should not be able to set y"
except AttributeError:
    pass  # Expected

# Should still be hashable
assert hash(ip) == hash(ImmutablePoint(3, 4))

print("✓ Exercise 5 passed: Read-Only Properties")


# =============================================================================
# Exercise 6: Alternative Constructor with @classmethod
# =============================================================================
# Create alternative constructors for different input formats

class Color:
    """An RGB color."""

    def __init__(self, r: int, g: int, b: int):
        self.r = r
        self.g = g
        self.b = b

    def __repr__(self) -> str:
        return f"Color({self.r}, {self.g}, {self.b})"

    def __eq__(self, other):
        return (self.r, self.g, self.b) == (other.r, other.g, other.b)

    @classmethod
    def from_hex(cls, hex_string: str) -> 'Color':
        """
        Create Color from hex string like '#FF5733' or 'FF5733'.

        TODO: Implement
        Hint: Strip '#' if present, then parse pairs of hex digits
        """
        ...
        pass

    @classmethod
    def from_tuple(cls, rgb: tuple[int, int, int]) -> 'Color':
        """
        Create Color from (r, g, b) tuple.

        TODO: Implement
        """
        ...
        pass

    @classmethod
    def white(cls) -> 'Color':
        """
        Factory method for white color (255, 255, 255).

        TODO: Implement
        """
        ...
        pass

    @classmethod
    def black(cls) -> 'Color':
        """
        Factory method for black color (0, 0, 0).

        TODO: Implement
        """
        ...
        pass


# Test from_hex
c1 = Color.from_hex('#FF5733')
assert c1 == Color(255, 87, 51), f"Got: {c1}"

c2 = Color.from_hex('00FF00')  # Without #
assert c2 == Color(0, 255, 0), f"Got: {c2}"

# Test from_tuple
c3 = Color.from_tuple((128, 128, 128))
assert c3 == Color(128, 128, 128)

# Test factory methods
assert Color.white() == Color(255, 255, 255)
assert Color.black() == Color(0, 0, 0)

# Verify classmethod works with subclasses
class ExtendedColor(Color):
    pass

ec = ExtendedColor.from_hex('#FF0000')
assert isinstance(ec, ExtendedColor), "Should return subclass instance"

print("✓ Exercise 6 passed: Alternative Constructor with @classmethod")


# =============================================================================
# Exercise 7: Implement __format__
# =============================================================================
# Support custom formatting

class Temperature:
    """A temperature value that can be formatted in C or F."""

    def __init__(self, celsius: float):
        self.celsius = float(celsius)

    @property
    def fahrenheit(self) -> float:
        return self.celsius * 9 / 5 + 32

    def __repr__(self) -> str:
        return f"Temperature({self.celsius!r})"

    def __format__(self, fmt_spec: str) -> str:
        """
        Format temperature with optional unit.

        Format spec:
        - Ends with 'c' or 'C': Display in Celsius with "°C" suffix
        - Ends with 'f' or 'F': Display in Fahrenheit with "°F" suffix
        - Otherwise: Display Celsius value only (no suffix)

        The rest of the format spec is applied to the number.

        Examples:
            format(t, '.1c') -> '20.0°C'
            format(t, '.1f') -> '68.0°F' (note: 'f' here means Fahrenheit, not float format)
            format(t, '.2F') -> '68.00°F'
            format(t, '.1') -> '20.0'

        TODO: Implement
        Hint: Check last character, apply remaining spec to the value
        """
        ...
        pass


t = Temperature(20)

# Default format (no spec)
assert format(t, '') == '20.0', f"Got: {format(t, '')}"

# Celsius format
assert format(t, 'c') == '20.0°C', f"Got: {format(t, 'c')}"
assert format(t, '.1c') == '20.0°C', f"Got: {format(t, '.1c')}"
assert format(t, '.0c') == '20°C', f"Got: {format(t, '.0c')}"

# Fahrenheit format
assert format(t, 'f') == '68.0°F', f"Got: {format(t, 'f')}"
assert format(t, '.1f') == '68.0°F', f"Got: {format(t, '.1f')}"

# Works with f-strings
assert f"{t:.1c}" == "20.0°C"
assert f"{t:.0f}" == "68°F"

print("✓ Exercise 7 passed: __format__")


# =============================================================================
# Exercise 8: Implement __bytes__ and frombytes
# =============================================================================
# Support binary serialization

class Vector2d_v4:
    """A 2D vector with binary serialization."""

    typecode = 'd'  # 8-byte double float

    def __init__(self, x: float, y: float):
        self._x = float(x)
        self._y = float(y)

    @property
    def x(self) -> float:
        return self._x

    @property
    def y(self) -> float:
        return self._y

    def __repr__(self) -> str:
        return f"Vector2d_v4({self.x!r}, {self.y!r})"

    def __iter__(self):
        return iter((self.x, self.y))

    def __eq__(self, other):
        return tuple(self) == tuple(other)

    def __bytes__(self) -> bytes:
        """
        Convert to bytes: typecode byte + array bytes.

        TODO: Implement
        Hint:
        - bytes([ord(self.typecode)]) for the first byte
        - bytes(array(self.typecode, self)) for the data
        """
        ...
        pass

    @classmethod
    def frombytes(cls, octets: bytes) -> 'Vector2d_v4':
        """
        Create Vector2d from bytes.

        TODO: Implement
        Hint:
        - First byte is typecode: chr(octets[0])
        - Rest is array data: use memoryview and cast
        """
        ...
        pass


v = Vector2d_v4(3.0, 4.0)

# Test __bytes__
b = bytes(v)
assert isinstance(b, bytes)
assert len(b) == 17  # 1 byte typecode + 16 bytes for two doubles

# Test frombytes
v_copy = Vector2d_v4.frombytes(b)
assert v_copy == v, f"Expected {v}, got {v_copy}"
assert v_copy.x == 3.0
assert v_copy.y == 4.0

# Verify roundtrip
v2 = Vector2d_v4(1.5, 2.5)
assert Vector2d_v4.frombytes(bytes(v2)) == v2

print("✓ Exercise 8 passed: __bytes__ and frombytes")


# =============================================================================
# Exercise 9: __slots__ for Memory Efficiency
# =============================================================================
# Use __slots__ to reduce memory usage

class SlottedVector:
    """
    A memory-efficient vector using __slots__.

    TODO: Add __slots__ = ('_x', '_y') as a class attribute
    """
    # TODO: Define __slots__ here
    ...

    def __init__(self, x: float, y: float):
        self._x = float(x)
        self._y = float(y)

    @property
    def x(self) -> float:
        return self._x

    @property
    def y(self) -> float:
        return self._y

    def __repr__(self) -> str:
        return f"SlottedVector({self.x!r}, {self.y!r})"


sv = SlottedVector(3, 4)
assert sv.x == 3.0
assert sv.y == 4.0

# Verify __slots__ is defined
assert hasattr(SlottedVector, '__slots__'), "Class should have __slots__"

# Verify no __dict__ on instances (key benefit of __slots__)
assert not hasattr(sv, '__dict__'), "Slotted instance should not have __dict__"

# Verify cannot add arbitrary attributes
try:
    sv.z = 5
    assert False, "Should not be able to add arbitrary attributes"
except AttributeError:
    pass  # Expected

print("✓ Exercise 9 passed: __slots__ for Memory Efficiency")


# =============================================================================
# Exercise 10: __match_args__ for Pattern Matching
# =============================================================================
# Support positional pattern matching

class Point3D:
    """
    A 3D point supporting positional pattern matching.

    TODO: Add __match_args__ = ('x', 'y', 'z')
    """
    # TODO: Define __match_args__ here
    ...

    def __init__(self, x: float, y: float, z: float):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    def __repr__(self) -> str:
        return f"Point3D({self.x!r}, {self.y!r}, {self.z!r})"


# Verify __match_args__ is defined
assert hasattr(Point3D, '__match_args__'), "Class should have __match_args__"
assert Point3D.__match_args__ == ('x', 'y', 'z'), f"Got: {Point3D.__match_args__}"

# Test pattern matching (Python 3.10+)
def classify_point(p: Point3D) -> str:
    match p:
        case Point3D(0, 0, 0):
            return "origin"
        case Point3D(_, 0, 0):
            return "on x-axis"
        case Point3D(0, _, 0):
            return "on y-axis"
        case Point3D(0, 0, _):
            return "on z-axis"
        case Point3D(x, y, 0):
            return "on xy-plane"
        case _:
            return "general"


assert classify_point(Point3D(0, 0, 0)) == "origin"
assert classify_point(Point3D(5, 0, 0)) == "on x-axis"
assert classify_point(Point3D(0, 3, 0)) == "on y-axis"
assert classify_point(Point3D(0, 0, 7)) == "on z-axis"
assert classify_point(Point3D(1, 2, 0)) == "on xy-plane"
assert classify_point(Point3D(1, 2, 3)) == "general"

print("✓ Exercise 10 passed: __match_args__ for Pattern Matching")


# =============================================================================
# Exercise 11: Complete Pythonic Class
# =============================================================================
# Build a complete Pythonic class with all the features

class Money:
    """
    A Pythonic money class with currency.

    Features to implement:
    - __repr__, __str__
    - __iter__ (yield amount, currency)
    - __eq__, __hash__
    - __bool__ (zero amount is falsy)
    - __format__ (support currency symbol prefix)
    - Read-only properties
    - @classmethod alternative constructors
    """

    __slots__ = ('_amount', '_currency')
    __match_args__ = ('amount', 'currency')

    # Currency symbols
    SYMBOLS = {'USD': '$', 'EUR': '€', 'GBP': '£', 'JPY': '¥'}

    def __init__(self, amount: float, currency: str = 'USD'):
        # TODO: Store as private attributes
        ...
        pass

    @property
    def amount(self) -> float:
        # TODO: Implement
        ...
        pass

    @property
    def currency(self) -> str:
        # TODO: Implement
        ...
        pass

    def __repr__(self) -> str:
        """Format: Money(100.0, 'USD')"""
        # TODO: Implement
        ...
        pass

    def __str__(self) -> str:
        """Format: 100.00 USD"""
        # TODO: Implement
        ...
        pass

    def __iter__(self):
        """Yield amount, then currency."""
        # TODO: Implement
        ...
        pass

    def __eq__(self, other) -> bool:
        """Equal if same amount and currency."""
        # TODO: Implement
        ...
        pass

    def __hash__(self) -> int:
        # TODO: Implement
        ...
        pass

    def __bool__(self) -> bool:
        """Falsy if amount is zero."""
        # TODO: Implement
        ...
        pass

    def __format__(self, fmt_spec: str) -> str:
        """
        Format money.
        - If fmt_spec ends with 's', use currency symbol prefix
        - Rest of spec applies to amount

        Examples:
            format(m, '.2f') -> '100.00'
            format(m, '.2fs') -> '$100.00'
        """
        # TODO: Implement
        ...
        pass

    @classmethod
    def dollars(cls, amount: float) -> 'Money':
        """Create USD money."""
        # TODO: Implement
        ...
        pass

    @classmethod
    def euros(cls, amount: float) -> 'Money':
        """Create EUR money."""
        # TODO: Implement
        ...
        pass


# Test basic creation
m = Money(100, 'USD')
assert m.amount == 100.0
assert m.currency == 'USD'

# Test __repr__ and __str__
assert repr(m) == "Money(100.0, 'USD')", f"Got: {repr(m)}"
assert str(m) == "100.00 USD", f"Got: {str(m)}"

# Test __iter__
amount, currency = m
assert amount == 100.0 and currency == 'USD'

# Test __eq__ and __hash__
m2 = Money(100, 'USD')
m3 = Money(100, 'EUR')
assert m == m2
assert m != m3
assert hash(m) == hash(m2)

# Test in set/dict
money_set = {m, m2, m3}
assert len(money_set) == 2

# Test __bool__
assert bool(Money(100, 'USD')) == True
assert bool(Money(0, 'USD')) == False

# Test __format__
assert format(m, '.2f') == '100.00', f"Got: {format(m, '.2f')}"
assert format(m, '.2fs') == '$100.00', f"Got: {format(m, '.2fs')}"

m_eur = Money(50, 'EUR')
assert format(m_eur, '.2fs') == '€50.00', f"Got: {format(m_eur, '.2fs')}"

# Test class methods
assert Money.dollars(50) == Money(50, 'USD')
assert Money.euros(30) == Money(30, 'EUR')

# Test read-only
try:
    m.amount = 200
    assert False, "Should not be able to set amount"
except AttributeError:
    pass

print("✓ Exercise 11 passed: Complete Pythonic Class")


# =============================================================================
# Exercise 12: Subclass with Modified Behavior
# =============================================================================
# Create a subclass that uses classmethod properly

class Vector2d_v5:
    """Base vector class."""

    typecode = 'd'

    def __init__(self, x: float, y: float):
        self._x = float(x)
        self._y = float(y)

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    def __repr__(self):
        class_name = type(self).__name__
        return f'{class_name}({self.x!r}, {self.y!r})'

    def __iter__(self):
        return iter((self.x, self.y))

    def __eq__(self, other):
        return tuple(self) == tuple(other)

    def __bytes__(self):
        return (bytes([ord(self.typecode)]) +
                bytes(array(self.typecode, self)))

    @classmethod
    def frombytes(cls, octets):
        typecode = chr(octets[0])
        memv = memoryview(octets[1:]).cast(typecode)
        return cls(*memv)


class ShortVector(Vector2d_v5):
    """
    A vector using short floats (4 bytes each) instead of doubles.

    TODO: Override typecode class attribute to 'f' (float, 4 bytes)
    """
    # TODO: Set typecode = 'f'
    ...
    pass


# Test that ShortVector uses less bytes
v_double = Vector2d_v5(3.0, 4.0)
v_short = ShortVector(3.0, 4.0)

bytes_double = bytes(v_double)
bytes_short = bytes(v_short)

assert len(bytes_double) == 17, f"Double: expected 17, got {len(bytes_double)}"  # 1 + 8 + 8
assert len(bytes_short) == 9, f"Short: expected 9, got {len(bytes_short)}"  # 1 + 4 + 4

# Test frombytes returns correct type (thanks to cls parameter)
v_short_copy = ShortVector.frombytes(bytes_short)
assert isinstance(v_short_copy, ShortVector), "frombytes should return ShortVector"
assert type(v_short_copy).__name__ == 'ShortVector'

# Values should be approximately equal (float has less precision)
assert abs(v_short_copy.x - 3.0) < 0.001
assert abs(v_short_copy.y - 4.0) < 0.001

print("✓ Exercise 12 passed: Subclass with Modified Behavior")


# =============================================================================
# All exercises completed!
# =============================================================================
print("\n" + "=" * 60)
print("🎉 Congratulations! All Chapter 11 exercises passed!")
print("=" * 60)
