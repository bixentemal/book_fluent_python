"""
Chapter 1: The Python Data Model - Exercises
=============================================

Complete each exercise by replacing the `None` or `...` placeholders.
Run this file to check your answers with the assertions.
"""

# =============================================================================
# Exercise 1: Implement __repr__ and __str__
# =============================================================================
# Create a Book class with proper string representations

class Book:
    def __init__(self, title, author, year):
        self.title = title
        self.author = author
        self.year = year

    def __repr__(self):
        """
        Return unambiguous representation for debugging.
        Format: Book('Title', 'Author', Year)

        TODO: Implement this method
        """
        ...
        pass

    def __str__(self):
        """
        Return human-readable representation.
        Format: 'Title' by Author (Year)

        TODO: Implement this method
        """
        ...
        pass


book = Book("Fluent Python", "Luciano Ramalho", 2022)
assert repr(book) == "Book('Fluent Python', 'Luciano Ramalho', 2022)"
assert str(book) == "'Fluent Python' by Luciano Ramalho (2022)"
print("✓ Exercise 1 passed: __repr__ and __str__")


# =============================================================================
# Exercise 2: Implement __len__ and __getitem__
# =============================================================================
# Create a Playlist class that behaves like a sequence

class Playlist:
    def __init__(self, name, songs):
        self.name = name
        self._songs = list(songs)

    def __len__(self):
        """Return number of songs in playlist."""
        # TODO: Implement
        ...
        pass

    def __getitem__(self, index):
        """Support indexing and slicing."""
        # TODO: Implement
        ...
        pass


playlist = Playlist("Road Trip", ["Song A", "Song B", "Song C", "Song D", "Song E"])

# Test len
assert len(playlist) == 5, "Playlist should have 5 songs"

# Test indexing
assert playlist[0] == "Song A", "First song should be 'Song A'"
assert playlist[-1] == "Song E", "Last song should be 'Song E'"

# Test slicing (free with __getitem__)
assert playlist[1:3] == ["Song B", "Song C"], "Slicing should work"

# Test iteration (free with __getitem__)
all_songs = [song for song in playlist]
assert all_songs == ["Song A", "Song B", "Song C", "Song D", "Song E"]

# Test 'in' operator (free with __getitem__)
assert "Song C" in playlist, "'in' operator should work"

print("✓ Exercise 2 passed: __len__ and __getitem__")


# =============================================================================
# Exercise 3: Implement __bool__
# =============================================================================
# Create a Task class where completed tasks are "falsy"

class Task:
    def __init__(self, name, completed=False):
        self.name = name
        self.completed = completed

    def __bool__(self):
        """
        Task is truthy if NOT completed (still needs work).
        Task is falsy if completed (no more work needed).

        TODO: Implement
        """
        ...
        pass

    def complete(self):
        self.completed = True


task1 = Task("Write code")
task2 = Task("Review PR", completed=True)

assert bool(task1) == True, "Incomplete task should be truthy"
assert bool(task2) == False, "Completed task should be falsy"

# Test in conditional
pending_tasks = [t for t in [task1, task2] if t]
assert len(pending_tasks) == 1, "Only incomplete tasks should be selected"

task1.complete()
assert bool(task1) == False, "Completed task should now be falsy"

print("✓ Exercise 3 passed: __bool__")


# =============================================================================
# Exercise 4: Implement Arithmetic Operators
# =============================================================================
# Create a Money class with addition and multiplication

class Money:
    def __init__(self, amount, currency="USD"):
        self.amount = amount
        self.currency = currency

    def __repr__(self):
        return f"Money({self.amount}, '{self.currency}')"

    def __add__(self, other):
        """
        Add two Money objects of the same currency.
        Raise ValueError if currencies don't match.

        TODO: Implement
        """
        ...
        pass

    def __mul__(self, scalar):
        """
        Multiply money by a scalar (int or float).

        TODO: Implement
        """
        ...
        pass

    def __rmul__(self, scalar):
        """
        Support scalar * money (reversed multiplication).

        TODO: Implement
        """
        ...
        pass

    def __eq__(self, other):
        """Two Money objects are equal if amount and currency match."""
        if not isinstance(other, Money):
            return NotImplemented
        return self.amount == other.amount and self.currency == other.currency


m1 = Money(100, "USD")
m2 = Money(50, "USD")
m3 = Money(100, "EUR")

# Test addition
result = m1 + m2
assert result == Money(150, "USD"), f"Expected Money(150, 'USD'), got {result}"

# Test multiplication
result = m1 * 2
assert result == Money(200, "USD"), f"Expected Money(200, 'USD'), got {result}"

# Test reversed multiplication
result = 3 * m2
assert result == Money(150, "USD"), f"Expected Money(150, 'USD'), got {result}"

# Test currency mismatch
try:
    m1 + m3
    assert False, "Should have raised ValueError for currency mismatch"
except ValueError:
    pass  # Expected

print("✓ Exercise 4 passed: Arithmetic Operators")


# =============================================================================
# Exercise 5: Implement Comparison Operators
# =============================================================================
# Create a Version class that can be compared

from functools import total_ordering

@total_ordering
class Version:
    """
    Semantic version with major.minor.patch format.
    Example: Version(1, 2, 3) represents version 1.2.3
    """

    def __init__(self, major, minor=0, patch=0):
        self.major = major
        self.minor = minor
        self.patch = patch

    def __repr__(self):
        return f"Version({self.major}, {self.minor}, {self.patch})"

    def __str__(self):
        return f"{self.major}.{self.minor}.{self.patch}"

    def __eq__(self, other):
        """
        Two versions are equal if all components match.

        TODO: Implement
        """
        ...
        pass

    def __lt__(self, other):
        """
        Compare versions: 1.0.0 < 1.0.1 < 1.1.0 < 2.0.0
        Hint: Compare as tuples (major, minor, patch)

        TODO: Implement
        """
        ...
        pass


v1 = Version(1, 0, 0)
v2 = Version(1, 0, 1)
v3 = Version(1, 1, 0)
v4 = Version(2, 0, 0)
v5 = Version(1, 0, 0)

# Test equality
assert v1 == v5, "Same version should be equal"
assert not (v1 == v2), "Different versions should not be equal"

# Test less than
assert v1 < v2, "1.0.0 < 1.0.1"
assert v2 < v3, "1.0.1 < 1.1.0"
assert v3 < v4, "1.1.0 < 2.0.0"

# Test other comparisons (from @total_ordering)
assert v2 > v1, "1.0.1 > 1.0.0"
assert v1 <= v5, "1.0.0 <= 1.0.0"
assert v4 >= v3, "2.0.0 >= 1.1.0"

# Test sorting
versions = [v4, v1, v3, v2]
sorted_versions = sorted(versions)
assert sorted_versions == [v1, v2, v3, v4], "Versions should sort correctly"

print("✓ Exercise 5 passed: Comparison Operators")


# =============================================================================
# Exercise 6: Implement __call__
# =============================================================================
# Create a callable Multiplier class

class Multiplier:
    """
    A callable that multiplies its argument by a fixed factor.

    Example:
        double = Multiplier(2)
        double(5)  # Returns 10
    """

    def __init__(self, factor):
        """Store the multiplication factor."""
        # TODO: Implement
        ...
        pass

    def __call__(self, value):
        """Multiply value by the stored factor."""
        # TODO: Implement
        ...
        pass


double = Multiplier(2)
triple = Multiplier(3)

assert double(5) == 10
assert double(0) == 0
assert triple(4) == 12
assert callable(double), "Multiplier should be callable"

# Use with map
numbers = [1, 2, 3, 4, 5]
doubled = list(map(double, numbers))
assert doubled == [2, 4, 6, 8, 10]

print("✓ Exercise 6 passed: __call__")


# =============================================================================
# Exercise 7: Implement __contains__
# =============================================================================
# Create a DateRange class with efficient containment check

from datetime import date, timedelta

class DateRange:
    """
    A range of dates (inclusive).

    Example:
        dr = DateRange(date(2024, 1, 1), date(2024, 1, 31))
        date(2024, 1, 15) in dr  # True
    """

    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __contains__(self, item):
        """
        Check if a date is within the range (inclusive).

        TODO: Implement
        """
        ...
        pass

    def __iter__(self):
        """Iterate over all dates in range."""
        current = self.start
        while current <= self.end:
            yield current
            current += timedelta(days=1)


january = DateRange(date(2024, 1, 1), date(2024, 1, 31))

# Test containment
assert date(2024, 1, 1) in january, "First day should be in range"
assert date(2024, 1, 31) in january, "Last day should be in range"
assert date(2024, 1, 15) in january, "Middle day should be in range"
assert date(2024, 2, 1) not in january, "February should not be in range"
assert date(2023, 12, 31) not in january, "December should not be in range"

print("✓ Exercise 7 passed: __contains__")


# =============================================================================
# Exercise 8: Context Manager with __enter__ and __exit__
# =============================================================================
# Create a context manager that tracks execution time

import time

class Timer:
    """
    A context manager that measures elapsed time.

    Usage:
        with Timer() as t:
            # do something
        print(t.elapsed)  # Time in seconds
    """

    def __init__(self):
        self.start = None
        self.end = None
        self.elapsed = None

    def __enter__(self):
        """
        Start the timer and return self.

        TODO: Implement
        Hint: Use time.perf_counter() for accurate timing
        """
        ...
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Stop the timer and calculate elapsed time.
        Return False to not suppress exceptions.

        TODO: Implement
        """
        ...
        pass


# Test the timer
with Timer() as t:
    total = sum(range(100000))

assert t.elapsed is not None, "elapsed should be set"
assert t.elapsed >= 0, "elapsed should be non-negative"
assert t.elapsed < 1, "Should complete in under a second"

# Test that it doesn't suppress exceptions
try:
    with Timer() as t:
        raise ValueError("test error")
except ValueError:
    pass  # Expected - exception was not suppressed
else:
    assert False, "Exception should not be suppressed"

print("✓ Exercise 8 passed: Context Manager")


# =============================================================================
# Exercise 9: Complete Implementation
# =============================================================================
# Create a comprehensive Fraction class using special methods

class Fraction:
    """
    A simple fraction class demonstrating multiple special methods.

    Supports:
    - repr/str
    - arithmetic (+, *, negation)
    - comparison (==)
    - abs()
    - bool (zero is falsy)
    """

    def __init__(self, numerator, denominator=1):
        if denominator == 0:
            raise ValueError("Denominator cannot be zero")
        # Normalize sign
        if denominator < 0:
            numerator = -numerator
            denominator = -denominator
        self.numerator = numerator
        self.denominator = denominator

    def __repr__(self):
        """Format: Fraction(num, denom)"""
        # TODO: Implement
        ...
        pass

    def __str__(self):
        """Format: num/denom (or just num if denom is 1)"""
        # TODO: Implement
        ...
        pass

    def __add__(self, other):
        """Add two fractions. a/b + c/d = (ad + bc) / bd"""
        # TODO: Implement
        ...
        pass

    def __mul__(self, other):
        """Multiply two fractions. a/b * c/d = ac / bd"""
        # TODO: Implement
        ...
        pass

    def __neg__(self):
        """Negate: -a/b = -a/b"""
        # TODO: Implement
        ...
        pass

    def __abs__(self):
        """Absolute value: |a/b| = |a|/|b|"""
        # TODO: Implement
        ...
        pass

    def __eq__(self, other):
        """Equal if cross products match: a/b == c/d iff a*d == b*c"""
        # TODO: Implement
        ...
        pass

    def __bool__(self):
        """Zero fraction is falsy"""
        # TODO: Implement
        ...
        pass


# Test repr and str
f1 = Fraction(1, 2)
assert repr(f1) == "Fraction(1, 2)"
assert str(f1) == "1/2"

f2 = Fraction(3, 1)
assert str(f2) == "3", "Whole numbers should display without denominator"

# Test addition
f3 = Fraction(1, 4)
result = f1 + f3  # 1/2 + 1/4 = 6/8
assert result == Fraction(6, 8), f"1/2 + 1/4 should equal 6/8, got {result}"

# Test multiplication
result = f1 * f3  # 1/2 * 1/4 = 1/8
assert result == Fraction(1, 8), f"1/2 * 1/4 should equal 1/8"

# Test negation
neg = -f1
assert neg == Fraction(-1, 2)

# Test abs
assert abs(Fraction(-3, 4)) == Fraction(3, 4)

# Test bool
assert bool(Fraction(1, 2)) == True
assert bool(Fraction(0, 5)) == False

# Test equality
assert Fraction(1, 2) == Fraction(2, 4), "1/2 should equal 2/4"
assert Fraction(3, 4) == Fraction(6, 8), "3/4 should equal 6/8"

print("✓ Exercise 9 passed: Complete Fraction Implementation")


# =============================================================================
# All exercises completed!
# =============================================================================
print("\n" + "=" * 60)
print("🎉 Congratulations! All Chapter 1 exercises passed!")
print("=" * 60)
