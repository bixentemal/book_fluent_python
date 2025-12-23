"""
Chapter 16: Operator Overloading - Exercises
=============================================

Practice operator overloading: unary operators, infix operators,
comparison operators, and augmented assignment.

Run this file to check your implementations.
"""

import itertools
import math
from collections import abc
from typing import Iterator

# =============================================================================
# Exercise 1: Unary Operators - __neg__ and __pos__
# =============================================================================
# Implement a Vector class with unary operators:
# - __neg__: Return new Vector with all components negated
# - __pos__: Return a copy of the Vector
# - __abs__: Return the magnitude (Euclidean length) as a float
#
# The Vector should store components as a list internally.

class Vector:
    def __init__(self, components):
        self._components = list(components)

    def __repr__(self):
        return f"Vector({self._components})"

    def __len__(self):
        return len(self._components)

    def __iter__(self) -> Iterator[float]:
        return iter(self._components)

    def __getitem__(self, index):
        return self._components[index]

    def __neg__(self):
        # TODO: Return new Vector with negated components
        pass

    def __pos__(self):
        # TODO: Return a copy of self
        pass

    def __abs__(self):
        # TODO: Return magnitude using math.hypot
        pass


# Test Exercise 1
v1 = Vector([3, 4])
assert -v1 == Vector([-3, -4]), "__neg__ should negate all components"
assert +v1 == Vector([3, 4]), "__pos__ should return a copy"
assert +v1 is not v1, "__pos__ should return a NEW Vector"
assert abs(v1) == 5.0, "__abs__ should return magnitude (3-4-5 triangle)"
assert abs(Vector([1, 2, 2])) == 3.0, "__abs__ should work with 3D vectors"
print("✓ Exercise 1 passed: Unary operators")


# =============================================================================
# Exercise 2: Basic __eq__ for Vector
# =============================================================================
# Implement __eq__ for the Vector class:
# - Two Vectors are equal if they have the same length and components
# - Return NotImplemented for non-Vector types
#
# Add this method to the Vector class above.

# We need to add __eq__ to Vector for tests to work
# Add this to the Vector class:

def _vector_eq(self, other):
    # TODO: Implement equality check
    # Return NotImplemented if other is not a Vector
    pass

Vector.__eq__ = _vector_eq


# Test Exercise 2
v1 = Vector([1, 2, 3])
v2 = Vector([1, 2, 3])
v3 = Vector([1, 2, 4])
v4 = Vector([1, 2])
assert v1 == v2, "Vectors with same components should be equal"
assert not (v1 == v3), "Vectors with different components should not be equal"
assert not (v1 == v4), "Vectors with different lengths should not be equal"
assert not (v1 == [1, 2, 3]), "Vector should not equal a list"
assert not (v1 == (1, 2, 3)), "Vector should not equal a tuple"
print("✓ Exercise 2 passed: __eq__ implementation")


# =============================================================================
# Exercise 3: __add__ with Duck Typing
# =============================================================================
# Implement __add__ for Vector:
# - Add corresponding components
# - If vectors have different lengths, pad shorter with zeros
# - Use duck typing (try/except) to handle type errors
# - Return NotImplemented on TypeError

def _vector_add(self, other):
    # TODO: Use itertools.zip_longest with fillvalue=0
    # Catch TypeError and return NotImplemented
    pass

Vector.__add__ = _vector_add


# Test Exercise 3
v1 = Vector([1, 2, 3])
v2 = Vector([4, 5, 6])
assert v1 + v2 == Vector([5, 7, 9]), "Basic addition should work"

v3 = Vector([1, 2])
assert v1 + v3 == Vector([2, 4, 3]), "Different lengths should pad with zeros"
assert v3 + v1 == Vector([2, 4, 3]), "Order shouldn't matter for padding"

# Duck typing: adding tuple should work
assert v1 + (10, 20, 30) == Vector([11, 22, 33]), "Should work with tuples"
print("✓ Exercise 3 passed: __add__ with duck typing")


# =============================================================================
# Exercise 4: __radd__ for Reversed Addition
# =============================================================================
# Implement __radd__ so that tuple + Vector works.
# Hint: Addition is commutative, so just delegate to __add__.

def _vector_radd(self, other):
    # TODO: Delegate to __add__
    pass

Vector.__radd__ = _vector_radd


# Test Exercise 4
v1 = Vector([1, 2, 3])
assert (10, 20, 30) + v1 == Vector([11, 22, 33]), "tuple + Vector should work"
assert [5, 5, 5] + v1 == Vector([6, 7, 8]), "list + Vector should work"
print("✓ Exercise 4 passed: __radd__ implementation")


# =============================================================================
# Exercise 5: __mul__ for Scalar Multiplication
# =============================================================================
# Implement __mul__ for scalar multiplication:
# - Multiply each component by the scalar
# - Try to convert scalar to float
# - Return NotImplemented if conversion fails

def _vector_mul(self, scalar):
    # TODO: Try to convert scalar to float
    # Return NotImplemented on TypeError
    pass

Vector.__mul__ = _vector_mul


# Test Exercise 5
v1 = Vector([1, 2, 3])
assert v1 * 10 == Vector([10, 20, 30]), "Scalar multiplication should work"
assert v1 * 2.5 == Vector([2.5, 5.0, 7.5]), "Float scalar should work"
assert v1 * True == Vector([1, 2, 3]), "Boolean True is 1"
assert v1 * False == Vector([0, 0, 0]), "Boolean False is 0"
print("✓ Exercise 5 passed: __mul__ for scalar multiplication")


# =============================================================================
# Exercise 6: __rmul__ for Reversed Multiplication
# =============================================================================
# Implement __rmul__ so that 10 * Vector works.

def _vector_rmul(self, scalar):
    # TODO: Delegate to __mul__
    pass

Vector.__rmul__ = _vector_rmul


# Test Exercise 6
v1 = Vector([1, 2, 3])
assert 10 * v1 == Vector([10, 20, 30]), "scalar * Vector should work"
assert 0.5 * v1 == Vector([0.5, 1.0, 1.5]), "float * Vector should work"
print("✓ Exercise 6 passed: __rmul__ implementation")


# =============================================================================
# Exercise 7: __matmul__ for Dot Product
# =============================================================================
# Implement __matmul__ (@ operator) for dot product:
# - Both operands must be sized and iterable
# - Both must have the same length
# - Return sum of component-wise products
# - Raise ValueError for length mismatch
# - Return NotImplemented for invalid types

def _vector_matmul(self, other):
    # TODO: Check if other is Sized and Iterable (use abc.Sized, abc.Iterable)
    # Check lengths match
    # Return dot product
    pass

Vector.__matmul__ = _vector_matmul


# Test Exercise 7
v1 = Vector([1, 2, 3])
v2 = Vector([4, 5, 6])
assert v1 @ v2 == 32, "1*4 + 2*5 + 3*6 = 32"
assert [1, 2, 3] @ v2 == 32, "list @ Vector should work"

try:
    Vector([1, 2]) @ Vector([1, 2, 3])
    assert False, "Should raise ValueError for mismatched lengths"
except ValueError:
    pass
print("✓ Exercise 7 passed: __matmul__ for dot product")


# =============================================================================
# Exercise 8: __rmatmul__ for Reversed Dot Product
# =============================================================================

def _vector_rmatmul(self, other):
    # TODO: Delegate to __matmul__
    pass

Vector.__rmatmul__ = _vector_rmatmul


# Test Exercise 8
v1 = Vector([1, 2, 3])
assert [4, 5, 6] @ v1 == 32, "list @ Vector should work via __rmatmul__"
assert (4, 5, 6) @ v1 == 32, "tuple @ Vector should work via __rmatmul__"
print("✓ Exercise 8 passed: __rmatmul__ implementation")


# =============================================================================
# Exercise 9: Rich Comparison Operators
# =============================================================================
# Implement comparison operators for Vector based on magnitude:
# - __lt__: self magnitude < other magnitude
# - __le__: self magnitude <= other magnitude
# - __gt__: self magnitude > other magnitude
# - __ge__: self magnitude >= other magnitude
#
# Return NotImplemented if other is not a Vector.

def _vector_lt(self, other):
    # TODO: Compare magnitudes
    pass

def _vector_le(self, other):
    # TODO: Compare magnitudes
    pass

def _vector_gt(self, other):
    # TODO: Compare magnitudes
    pass

def _vector_ge(self, other):
    # TODO: Compare magnitudes
    pass

Vector.__lt__ = _vector_lt
Vector.__le__ = _vector_le
Vector.__gt__ = _vector_gt
Vector.__ge__ = _vector_ge


# Test Exercise 9
v_small = Vector([1, 1])  # magnitude ≈ 1.41
v_medium = Vector([3, 4])  # magnitude = 5
v_large = Vector([6, 8])  # magnitude = 10
v_medium2 = Vector([4, 3])  # magnitude = 5

assert v_small < v_medium, "Smaller magnitude should be less"
assert v_large > v_medium, "Larger magnitude should be greater"
assert v_medium <= v_medium2, "Equal magnitudes should be <="
assert v_medium >= v_medium2, "Equal magnitudes should be >="
assert not (v_medium < v_medium2), "Equal magnitudes should not be <"
print("✓ Exercise 9 passed: Rich comparison operators")


# =============================================================================
# Exercise 10: MutableVector with __iadd__
# =============================================================================
# Create a MutableVector class that supports in-place addition:
# - __iadd__ modifies self in place
# - __iadd__ must return self
# - __add__ returns a new MutableVector (don't modify operands)

class MutableVector:
    def __init__(self, components):
        self._components = list(components)

    def __repr__(self):
        return f"MutableVector({self._components})"

    def __eq__(self, other):
        if isinstance(other, MutableVector):
            return self._components == other._components
        return NotImplemented

    def __iter__(self):
        return iter(self._components)

    def __len__(self):
        return len(self._components)

    def __add__(self, other):
        # TODO: Return NEW MutableVector with sum of components
        # Use zip_longest with fillvalue=0
        pass

    def __iadd__(self, other):
        # TODO: Modify self in place
        # Extend self if other is longer
        # MUST return self
        pass


# Test Exercise 10
mv1 = MutableVector([1, 2, 3])
mv1_id = id(mv1)
mv1 += MutableVector([4, 5, 6])
assert mv1 == MutableVector([5, 7, 9]), "__iadd__ should add components"
assert id(mv1) == mv1_id, "__iadd__ should modify in place, not create new"

# __add__ should create new object
mv2 = MutableVector([1, 2])
mv3 = mv2 + MutableVector([3, 4])
assert mv2 == MutableVector([1, 2]), "__add__ should not modify original"
assert mv3 == MutableVector([4, 6]), "__add__ should return sum"
assert id(mv2) != id(mv3), "__add__ should create new object"
print("✓ Exercise 10 passed: MutableVector with __iadd__")


# =============================================================================
# Exercise 11: __imul__ for In-Place Scalar Multiplication
# =============================================================================
# Add __imul__ to MutableVector for in-place scalar multiplication.

def _mutable_imul(self, scalar):
    # TODO: Multiply all components in place
    # Return self
    pass

MutableVector.__imul__ = _mutable_imul


# Test Exercise 11
mv = MutableVector([1, 2, 3])
mv_id = id(mv)
mv *= 10
assert mv == MutableVector([10, 20, 30]), "__imul__ should multiply components"
assert id(mv) == mv_id, "__imul__ should modify in place"
print("✓ Exercise 11 passed: __imul__ implementation")


# =============================================================================
# Exercise 12: Money Class with Operator Overloading
# =============================================================================
# Create a Money class that supports:
# - Addition of Money with same currency
# - Scalar multiplication
# - Comparison
# - Return NotImplemented for different currencies

class Money:
    def __init__(self, amount: float, currency: str = "USD"):
        self.amount = amount
        self.currency = currency

    def __repr__(self):
        return f"Money({self.amount}, '{self.currency}')"

    def __eq__(self, other):
        if isinstance(other, Money):
            return self.amount == other.amount and self.currency == other.currency
        return NotImplemented

    def __add__(self, other):
        # TODO: Add Money with same currency only
        # Return NotImplemented for different currencies
        pass

    def __radd__(self, other):
        # Handle sum() which starts with 0
        if other == 0:
            return self
        return self + other

    def __mul__(self, scalar):
        # TODO: Multiply amount by scalar
        pass

    def __rmul__(self, scalar):
        return self * scalar

    def __lt__(self, other):
        # TODO: Compare amounts (same currency only)
        pass


# Test Exercise 12
m1 = Money(100, "USD")
m2 = Money(50, "USD")
m3 = Money(100, "EUR")

assert m1 + m2 == Money(150, "USD"), "Same currency addition should work"
assert m1 * 2 == Money(200, "USD"), "Scalar multiplication should work"
assert 3 * m2 == Money(150, "USD"), "Reversed multiplication should work"
assert m2 < m1, "Comparison should work"

# Different currencies should return NotImplemented
result = m1.__add__(m3)
assert result is NotImplemented, "Different currencies should return NotImplemented"

# sum() should work
total = sum([Money(10, "USD"), Money(20, "USD"), Money(30, "USD")])
assert total == Money(60, "USD"), "sum() should work with Money"
print("✓ Exercise 12 passed: Money class with operators")


# =============================================================================
# Exercise 13: Bitwise Operators for a Flags Class
# =============================================================================
# Create a Flags class that uses bitwise operators:
# - __or__ (|): Combine flags
# - __and__ (&): Intersect flags
# - __invert__ (~): Invert flags (within a mask)
#
# Flags wraps an integer value.

class Flags:
    def __init__(self, value: int = 0, mask: int = 0xFF):
        self.value = value & mask
        self.mask = mask

    def __repr__(self):
        return f"Flags(0b{self.value:08b})"

    def __eq__(self, other):
        if isinstance(other, Flags):
            return self.value == other.value
        return NotImplemented

    def __or__(self, other):
        # TODO: Return new Flags with OR of values
        pass

    def __and__(self, other):
        # TODO: Return new Flags with AND of values
        pass

    def __invert__(self):
        # TODO: Return new Flags with inverted bits (within mask)
        pass


# Test Exercise 13
READ = Flags(0b0001)
WRITE = Flags(0b0010)
EXECUTE = Flags(0b0100)

# Combine flags with |
rw = READ | WRITE
assert rw == Flags(0b0011), "OR should combine flags"

# Intersect with &
result = rw & READ
assert result == Flags(0b0001), "AND should intersect flags"

# Invert
not_read = ~READ
assert not_read.value == 0b11111110, "NOT should invert all bits within mask"
print("✓ Exercise 13 passed: Bitwise operators for Flags")


# =============================================================================
# Exercise 14: Complex Number Operations
# =============================================================================
# Implement a simplified Complex class with:
# - __add__: Add complex numbers
# - __mul__: Multiply complex numbers (a+bi)(c+di) = (ac-bd) + (ad+bc)i
# - __abs__: Return magnitude sqrt(real² + imag²)
# - __neg__: Negate both parts
# - __eq__: Compare real and imaginary parts

class Complex:
    def __init__(self, real: float, imag: float = 0):
        self.real = real
        self.imag = imag

    def __repr__(self):
        sign = '+' if self.imag >= 0 else ''
        return f"Complex({self.real}{sign}{self.imag}i)"

    def __eq__(self, other):
        # TODO: Compare real and imaginary parts
        pass

    def __add__(self, other):
        # TODO: Add complex numbers
        pass

    def __mul__(self, other):
        # TODO: Multiply complex numbers
        # (a+bi)(c+di) = (ac-bd) + (ad+bc)i
        pass

    def __abs__(self):
        # TODO: Return magnitude
        pass

    def __neg__(self):
        # TODO: Negate both parts
        pass


# Test Exercise 14
c1 = Complex(3, 4)
c2 = Complex(1, 2)

assert c1 + c2 == Complex(4, 6), "Addition should add parts"
assert c1 * c2 == Complex(-5, 10), "(3+4i)(1+2i) = 3+6i+4i+8i² = 3+10i-8 = -5+10i"
assert abs(c1) == 5.0, "Magnitude of 3+4i is 5"
assert -c1 == Complex(-3, -4), "Negation should negate both parts"

# Multiplication with real number (as Complex)
assert c1 * Complex(2, 0) == Complex(6, 8), "Multiply by real should scale"
print("✓ Exercise 14 passed: Complex number operations")


# =============================================================================
# BONUS Exercise 15: Matrix Class with @ Operator
# =============================================================================
# Implement a simple 2x2 Matrix class:
# - __matmul__: Matrix multiplication
# - __add__: Matrix addition
# - __mul__: Scalar multiplication
#
# Matrix is stored as [[a, b], [c, d]]

class Matrix2x2:
    def __init__(self, rows: list[list[float]]):
        if len(rows) != 2 or len(rows[0]) != 2 or len(rows[1]) != 2:
            raise ValueError("Must be 2x2 matrix")
        self.rows = [list(row) for row in rows]

    def __repr__(self):
        return f"Matrix2x2({self.rows})"

    def __eq__(self, other):
        if isinstance(other, Matrix2x2):
            return self.rows == other.rows
        return NotImplemented

    def __add__(self, other):
        # TODO: Add corresponding elements
        pass

    def __mul__(self, scalar):
        # TODO: Multiply all elements by scalar
        pass

    def __matmul__(self, other):
        # TODO: Matrix multiplication
        # [[a,b],[c,d]] @ [[e,f],[g,h]] = [[ae+bg, af+bh], [ce+dg, cf+dh]]
        pass


# Test Exercise 15
m1 = Matrix2x2([[1, 2], [3, 4]])
m2 = Matrix2x2([[5, 6], [7, 8]])

# Addition
assert m1 + m2 == Matrix2x2([[6, 8], [10, 12]]), "Matrix addition"

# Scalar multiplication
assert m1 * 2 == Matrix2x2([[2, 4], [6, 8]]), "Scalar multiplication"

# Matrix multiplication
# [[1,2],[3,4]] @ [[5,6],[7,8]]
# = [[1*5+2*7, 1*6+2*8], [3*5+4*7, 3*6+4*8]]
# = [[19, 22], [43, 50]]
assert m1 @ m2 == Matrix2x2([[19, 22], [43, 50]]), "Matrix multiplication"

# Identity matrix
identity = Matrix2x2([[1, 0], [0, 1]])
assert m1 @ identity == m1, "Identity matrix multiplication"
print("✓ Exercise 15 passed: Matrix class with @ operator")


# =============================================================================
print("\n" + "=" * 60)
print("Congratulations! All Chapter 16 exercises completed!")
print("=" * 60)
