"""
Chapter 12: Special Methods for Sequences - Exercises
======================================================

Complete each exercise by replacing the `None` or `...` placeholders.
Run this file to check your answers with the assertions.
"""

from __future__ import annotations
from array import array
import reprlib
import math
import functools
import operator
from typing import Any


# =============================================================================
# Exercise 1: Basic Sequence Protocol
# =============================================================================
# Implement __len__ and __getitem__ to create a sequence

class Sentence:
    """A sequence of words in a sentence."""

    def __init__(self, text: str):
        self.text = text
        self.words = text.split()

    def __len__(self) -> int:
        """
        Return the number of words.

        TODO: Implement
        """
        ...
        pass

    def __getitem__(self, index: int) -> str:
        """
        Return word at index.

        TODO: Implement
        """
        ...
        pass

    def __repr__(self) -> str:
        return f'Sentence({self.text!r})'


s = Sentence("The quick brown fox jumps over the lazy dog")

# Test __len__
assert len(s) == 9, f"Expected 9 words, got {len(s)}"

# Test __getitem__
assert s[0] == "The"
assert s[4] == "jumps"
assert s[-1] == "dog"

# Test iteration (free with __getitem__)
words = [w for w in s]
assert words == ["The", "quick", "brown", "fox", "jumps", "over", "the", "lazy", "dog"]

# Test containment (free with __getitem__)
assert "fox" in s
assert "cat" not in s

print("✓ Exercise 1 passed: Basic Sequence Protocol")


# =============================================================================
# Exercise 2: Slice-Aware __getitem__
# =============================================================================
# Handle both integer indices and slices

class NumberList:
    """A list of numbers that returns NumberList when sliced."""

    def __init__(self, numbers):
        self._numbers = list(numbers)

    def __len__(self) -> int:
        return len(self._numbers)

    def __repr__(self) -> str:
        return f'NumberList({self._numbers!r})'

    def __eq__(self, other) -> bool:
        return self._numbers == list(other)

    def __getitem__(self, key):
        """
        Return item at index, or new NumberList if sliced.

        TODO: Implement
        Hint:
        - Check if key is a slice using isinstance(key, slice)
        - For slices, return new NumberList with sliced data
        - For integers, use operator.index(key) and return single item
        """
        ...
        pass


nl = NumberList([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

# Test integer indexing
assert nl[0] == 0
assert nl[-1] == 9
assert nl[5] == 5

# Test slicing returns NumberList
sliced = nl[2:5]
assert isinstance(sliced, NumberList), f"Slice should return NumberList, got {type(sliced)}"
assert sliced == NumberList([2, 3, 4])

# Test various slices
assert nl[::2] == NumberList([0, 2, 4, 6, 8])
assert nl[:3] == NumberList([0, 1, 2])
assert nl[-3:] == NumberList([7, 8, 9])

print("✓ Exercise 2 passed: Slice-Aware __getitem__")


# =============================================================================
# Exercise 3: Dynamic Attribute Access
# =============================================================================
# Use __getattr__ to provide virtual attributes

class Vector:
    """A vector with dynamic x, y, z, t attributes for first 4 components."""

    __match_args__ = ('x', 'y', 'z', 't')

    def __init__(self, components):
        self._components = list(components)

    def __len__(self) -> int:
        return len(self._components)

    def __repr__(self) -> str:
        return f'Vector({self._components!r})'

    def __getitem__(self, key):
        if isinstance(key, slice):
            return Vector(self._components[key])
        return self._components[operator.index(key)]

    def __getattr__(self, name: str):
        """
        Provide x, y, z, t as shortcuts for first 4 components.

        TODO: Implement
        Hint:
        - Get position from __match_args__.index(name)
        - Handle ValueError when name not in __match_args__
        - Check if position is within bounds of _components
        - Raise AttributeError with descriptive message if not found
        """
        ...
        pass


v = Vector([10, 20, 30, 40, 50])

# Test dynamic attributes
assert v.x == 10, f"Expected 10, got {v.x}"
assert v.y == 20
assert v.z == 30
assert v.t == 40

# Test that non-existent attributes raise AttributeError
try:
    v.w
    assert False, "Should raise AttributeError for 'w'"
except AttributeError:
    pass

# Test vector with fewer components
v2 = Vector([1, 2])
assert v2.x == 1
assert v2.y == 2
try:
    v2.z  # Only 2 components, z doesn't exist
    assert False, "Should raise AttributeError"
except AttributeError:
    pass

print("✓ Exercise 3 passed: Dynamic Attribute Access")


# =============================================================================
# Exercise 4: Blocking Attribute Setting
# =============================================================================
# Implement __setattr__ to prevent accidental attribute creation

class ImmutableVector:
    """A vector that prevents setting x, y, z, t attributes."""

    __match_args__ = ('x', 'y', 'z', 't')

    def __init__(self, components):
        # Use super().__setattr__ to bypass our __setattr__
        super().__setattr__('_components', list(components))

    def __len__(self) -> int:
        return len(self._components)

    def __repr__(self) -> str:
        return f'ImmutableVector({self._components!r})'

    def __getitem__(self, key):
        if isinstance(key, slice):
            return ImmutableVector(self._components[key])
        return self._components[operator.index(key)]

    def __getattr__(self, name: str):
        cls = type(self)
        try:
            pos = cls.__match_args__.index(name)
        except ValueError:
            pos = -1
        if 0 <= pos < len(self._components):
            return self._components[pos]
        raise AttributeError(f'{cls.__name__!r} has no attribute {name!r}')

    def __setattr__(self, name: str, value: Any) -> None:
        """
        Block setting of single lowercase letter attributes.

        TODO: Implement
        Hint:
        - If name is single lowercase letter, raise AttributeError
        - Otherwise, call super().__setattr__(name, value)
        """
        ...
        pass


iv = ImmutableVector([1, 2, 3])

# Reading should work
assert iv.x == 1
assert iv.y == 2

# Setting x, y, z, t should fail
try:
    iv.x = 10
    assert False, "Should not be able to set x"
except AttributeError:
    pass

try:
    iv.a = 10  # Any single lowercase letter
    assert False, "Should not be able to set single letter attribute"
except AttributeError:
    pass

# Setting other attributes should work
iv.name = "test"  # Multi-letter attribute is OK
assert iv.name == "test"

print("✓ Exercise 4 passed: Blocking Attribute Setting")


# =============================================================================
# Exercise 5: Hashing with reduce
# =============================================================================
# Implement efficient hashing using functools.reduce and XOR

class HashableVector:
    """A hashable vector using XOR for hash computation."""

    def __init__(self, components):
        self._components = tuple(components)  # Use tuple for immutability

    def __len__(self) -> int:
        return len(self._components)

    def __repr__(self) -> str:
        return f'HashableVector({list(self._components)!r})'

    def __iter__(self):
        return iter(self._components)

    def __eq__(self, other) -> bool:
        return len(self) == len(other) and all(a == b for a, b in zip(self, other))

    def __hash__(self) -> int:
        """
        Compute hash using XOR of component hashes.

        TODO: Implement
        Hint:
        - Create generator: (hash(x) for x in self._components)
        - Use functools.reduce with operator.xor
        - Provide initial value of 0
        """
        ...
        pass


hv1 = HashableVector([1, 2, 3])
hv2 = HashableVector([1, 2, 3])
hv3 = HashableVector([3, 2, 1])

# Test hashing
assert hash(hv1) == hash(hv2), "Equal vectors should have equal hashes"
assert hash(hv1) != hash(hv3), "Different vectors should (usually) have different hashes"

# Test use in set
vector_set = {hv1, hv2, hv3}
assert len(vector_set) == 2, "Set should have 2 unique vectors"

# Test use as dict key
vector_dict = {hv1: "first"}
assert vector_dict[hv2] == "first", "Equal vector should find same key"

print("✓ Exercise 5 passed: Hashing with reduce")


# =============================================================================
# Exercise 6: Efficient Equality
# =============================================================================
# Implement fast equality using zip and all

class EfficientVector:
    """A vector with efficient equality comparison."""

    def __init__(self, components):
        self._components = list(components)

    def __len__(self) -> int:
        return len(self._components)

    def __repr__(self) -> str:
        return f'EfficientVector({self._components!r})'

    def __iter__(self):
        return iter(self._components)

    def __eq__(self, other) -> bool:
        """
        Efficient equality: check length first, then compare elements.

        TODO: Implement
        Hint:
        - First check if lengths are equal (quick rejection)
        - Use zip(self, other) and all() for element comparison
        - all(a == b for a, b in zip(...)) short-circuits on first difference
        """
        ...
        pass


ev1 = EfficientVector([1, 2, 3, 4, 5])
ev2 = EfficientVector([1, 2, 3, 4, 5])
ev3 = EfficientVector([1, 2, 3, 4, 6])  # Last element different
ev4 = EfficientVector([1, 2, 3])  # Different length

assert ev1 == ev2, "Equal vectors should be equal"
assert not (ev1 == ev3), "Vectors with different elements should not be equal"
assert not (ev1 == ev4), "Vectors with different lengths should not be equal"

# Test with list (duck typing)
assert ev1 == [1, 2, 3, 4, 5], "Should be equal to list with same elements"

print("✓ Exercise 6 passed: Efficient Equality")


# =============================================================================
# Exercise 7: Safe Representation with reprlib
# =============================================================================
# Use reprlib for safe repr of large sequences

class LargeVector:
    """A vector that safely represents large data."""

    def __init__(self, components):
        self._components = array('d', components)

    def __len__(self) -> int:
        return len(self._components)

    def __iter__(self):
        return iter(self._components)

    def __repr__(self) -> str:
        """
        Return safe repr that truncates large vectors.

        TODO: Implement
        Hint:
        - Use reprlib.repr(self._components) to get truncated representation
        - Extract just the [...] part from "array('d', [...])"
        - Return f'LargeVector({components})'
        """
        ...
        pass


# Test with small vector
lv_small = LargeVector([1, 2, 3])
assert 'LargeVector(' in repr(lv_small)
assert '1.0' in repr(lv_small)

# Test with large vector - should be truncated
lv_large = LargeVector(range(100))
r = repr(lv_large)
assert 'LargeVector(' in r
assert '...' in r, f"Large vector repr should contain '...': {r}"
assert len(r) < 100, f"Repr should be truncated, got length {len(r)}"

print("✓ Exercise 7 passed: Safe Representation with reprlib")


# =============================================================================
# Exercise 8: Custom Format Method
# =============================================================================
# Implement __format__ with custom format codes

class FormattableVector:
    """A vector with custom formatting support."""

    def __init__(self, components):
        self._components = list(components)

    def __len__(self) -> int:
        return len(self._components)

    def __iter__(self):
        return iter(self._components)

    def __abs__(self) -> float:
        return math.hypot(*self._components)

    def __repr__(self) -> str:
        return f'FormattableVector({self._components!r})'

    def __format__(self, fmt_spec: str) -> str:
        """
        Format vector.

        Format specs:
        - Ends with 'h': hyperspherical format <magnitude, angles...>
        - Otherwise: cartesian format (x, y, z, ...)

        Apply remaining format spec to each component.

        TODO: Implement
        Hint:
        - Check if fmt_spec.endswith('h')
        - For 'h': use abs(self) as first value, then angles (simplified: just use magnitude)
        - For regular: use self._components
        - Join formatted components with ', '
        """
        ...
        pass


fv = FormattableVector([3, 4])

# Cartesian format
assert format(fv, '') == '(3, 4)', f"Got: {format(fv, '')}"
assert format(fv, '.1f') == '(3.0, 4.0)', f"Got: {format(fv, '.1f')}"

# Hyperspherical format (magnitude only for simplicity)
result = format(fv, 'h')
assert result.startswith('<'), f"Hyperspherical should start with '<': {result}"
assert '5' in result, f"Should contain magnitude 5: {result}"

# With format spec
result = format(fv, '.2fh')
assert '<5.00' in result, f"Got: {result}"

print("✓ Exercise 8 passed: Custom Format Method")


# =============================================================================
# Exercise 9: Alternative Constructor
# =============================================================================
# Implement frombytes class method

class ByteVector:
    """A vector that can be serialized to/from bytes."""

    typecode = 'd'

    def __init__(self, components):
        self._components = array(self.typecode, components)

    def __len__(self) -> int:
        return len(self._components)

    def __iter__(self):
        return iter(self._components)

    def __repr__(self) -> str:
        return f'ByteVector({list(self._components)!r})'

    def __eq__(self, other) -> bool:
        return list(self) == list(other)

    def __bytes__(self) -> bytes:
        """
        Convert to bytes: typecode + array data.

        TODO: Implement
        """
        ...
        pass

    @classmethod
    def frombytes(cls, octets: bytes) -> 'ByteVector':
        """
        Create ByteVector from bytes.

        TODO: Implement
        Hint:
        - First byte is typecode: chr(octets[0])
        - Rest is array data: memoryview(octets[1:]).cast(typecode)
        - Return cls(memview)
        """
        ...
        pass


bv = ByteVector([1.0, 2.0, 3.0, 4.0, 5.0])

# Test __bytes__
b = bytes(bv)
assert isinstance(b, bytes)
assert len(b) == 1 + 5 * 8  # 1 typecode + 5 doubles (8 bytes each)

# Test frombytes
bv_copy = ByteVector.frombytes(b)
assert bv_copy == bv, f"Expected {bv}, got {bv_copy}"

# Roundtrip test
bv2 = ByteVector([3.14, 2.71, 1.41])
assert ByteVector.frombytes(bytes(bv2)) == bv2

print("✓ Exercise 9 passed: Alternative Constructor")


# =============================================================================
# Exercise 10: Complete Vector Implementation
# =============================================================================
# Build a complete vector class with all features

class CompleteVector:
    """
    A complete N-dimensional vector with all sequence features.

    Features:
    - Sequence protocol (__len__, __getitem__ with slice support)
    - Dynamic attributes (x, y, z, t)
    - Immutable (blocks setting of single-letter attributes)
    - Hashable (__hash__, __eq__)
    - Iterable
    - Formattable
    - Serializable to bytes
    """

    typecode = 'd'
    __match_args__ = ('x', 'y', 'z', 't')

    def __init__(self, components):
        self._components = array(self.typecode, components)

    # TODO: Implement all the following methods

    def __len__(self) -> int:
        """Return number of components."""
        ...
        pass

    def __iter__(self):
        """Return iterator over components."""
        ...
        pass

    def __repr__(self) -> str:
        """Safe repr using reprlib."""
        ...
        pass

    def __getitem__(self, key):
        """Support indexing and slicing."""
        ...
        pass

    def __getattr__(self, name: str):
        """Provide x, y, z, t as shortcuts."""
        ...
        pass

    def __setattr__(self, name: str, value: Any) -> None:
        """Block single lowercase letter attributes."""
        ...
        pass

    def __eq__(self, other) -> bool:
        """Efficient equality check."""
        ...
        pass

    def __hash__(self) -> int:
        """Hash using XOR of component hashes."""
        ...
        pass

    def __abs__(self) -> float:
        """Return magnitude."""
        ...
        pass

    def __bool__(self) -> bool:
        """False if zero vector."""
        ...
        pass

    def __bytes__(self) -> bytes:
        """Convert to bytes."""
        ...
        pass

    @classmethod
    def frombytes(cls, octets: bytes) -> 'CompleteVector':
        """Create from bytes."""
        ...
        pass


# Test creation
cv = CompleteVector([1, 2, 3, 4, 5])
assert len(cv) == 5

# Test iteration
assert list(cv) == [1.0, 2.0, 3.0, 4.0, 5.0]

# Test repr
assert 'CompleteVector(' in repr(cv)

# Test indexing
assert cv[0] == 1.0
assert cv[-1] == 5.0

# Test slicing
sliced = cv[1:3]
assert isinstance(sliced, CompleteVector)
assert list(sliced) == [2.0, 3.0]

# Test dynamic attributes
assert cv.x == 1.0
assert cv.y == 2.0

# Test immutability
try:
    cv.x = 10
    assert False, "Should not allow setting x"
except AttributeError:
    pass

# Test equality
cv2 = CompleteVector([1, 2, 3, 4, 5])
assert cv == cv2

# Test hashing
assert hash(cv) == hash(cv2)
assert {cv, cv2} == {cv}  # Same in set

# Test abs and bool
assert abs(CompleteVector([3, 4])) == 5.0
assert bool(cv) == True
assert bool(CompleteVector([0, 0, 0])) == False

# Test bytes roundtrip
assert CompleteVector.frombytes(bytes(cv)) == cv

print("✓ Exercise 10 passed: Complete Vector Implementation")


# =============================================================================
# Exercise 11: Slice Object Exploration
# =============================================================================
# Understand how slice objects work

def analyze_slice(s: slice, length: int) -> tuple[int, int, int]:
    """
    Return normalized (start, stop, step) for a slice given a sequence length.

    TODO: Implement using s.indices(length)
    """
    ...
    pass


# Test with various slices
assert analyze_slice(slice(None, None, None), 10) == (0, 10, 1)  # [:]
assert analyze_slice(slice(2, 5, None), 10) == (2, 5, 1)  # [2:5]
assert analyze_slice(slice(None, None, 2), 10) == (0, 10, 2)  # [::2]
assert analyze_slice(slice(-3, None, None), 10) == (7, 10, 1)  # [-3:]
assert analyze_slice(slice(None, 100, None), 5) == (0, 5, 1)  # [:100] on length 5

print("✓ Exercise 11 passed: Slice Object Exploration")


# =============================================================================
# Exercise 12: Reduce Practice
# =============================================================================
# Practice using functools.reduce for various operations

def product(numbers: list[int]) -> int:
    """
    Return product of all numbers using reduce.

    TODO: Implement using functools.reduce and operator.mul
    """
    ...
    pass


def xor_all(numbers: list[int]) -> int:
    """
    Return XOR of all numbers using reduce.

    TODO: Implement using functools.reduce and operator.xor
    """
    ...
    pass


def concatenate(strings: list[str]) -> str:
    """
    Concatenate all strings using reduce.

    TODO: Implement using functools.reduce
    Hint: Use operator.add or a lambda
    """
    ...
    pass


def find_max(numbers: list[int]) -> int:
    """
    Find maximum using reduce (not using max()).

    TODO: Implement using functools.reduce
    Hint: lambda a, b: a if a > b else b
    """
    ...
    pass


assert product([1, 2, 3, 4, 5]) == 120
assert product([2, 3, 4]) == 24
assert xor_all([1, 2, 3]) == 0  # 1 ^ 2 ^ 3 = 0
assert xor_all([5, 3]) == 6  # 5 ^ 3 = 6
assert concatenate(['a', 'b', 'c']) == 'abc'
assert concatenate(['Hello', ' ', 'World']) == 'Hello World'
assert find_max([3, 1, 4, 1, 5, 9, 2, 6]) == 9

print("✓ Exercise 12 passed: Reduce Practice")


# =============================================================================
# All exercises completed!
# =============================================================================
print("\n" + "=" * 60)
print("🎉 Congratulations! All Chapter 12 exercises passed!")
print("=" * 60)
