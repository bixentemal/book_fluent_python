"""
Chapter 13: Interfaces, Protocols, and ABCs - Exercises
========================================================

Complete each exercise by replacing the `None` or `...` placeholders.
Run this file to check your answers with the assertions.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from collections.abc import Sequence, MutableSequence, Sized, Iterable, Iterator
from typing import Protocol, runtime_checkable, Any
import random


# =============================================================================
# Exercise 1: Duck Typing - Minimal Sequence
# =============================================================================
# Implement just __getitem__ and see what you get for free

class Letters:
    """A sequence of letters that only implements __getitem__."""

    def __init__(self, text: str):
        self._text = text

    def __getitem__(self, index: int) -> str:
        """
        Return character at index.

        TODO: Implement
        """
        ...
        pass


letters = Letters("HELLO")

# Test indexing
assert letters[0] == "H", f"Expected 'H', got {letters[0]}"
assert letters[-1] == "O"

# Test iteration (works with just __getitem__!)
result = [c for c in letters]
assert result == ['H', 'E', 'L', 'L', 'O'], f"Iteration failed: {result}"

# Test containment (works with just __getitem__!)
assert 'E' in letters
assert 'X' not in letters

print("✓ Exercise 1 passed: Duck Typing - Minimal Sequence")


# =============================================================================
# Exercise 2: Full Sequence Protocol
# =============================================================================
# Implement __len__ and __getitem__ with proper slice support

class Playlist:
    """A sequence of songs."""

    def __init__(self, songs: list[str]):
        self._songs = list(songs)

    def __len__(self) -> int:
        """
        Return number of songs.

        TODO: Implement
        """
        ...
        pass

    def __getitem__(self, key):
        """
        Return song at index or new Playlist if sliced.

        TODO: Implement
        - Handle both int and slice
        - Return new Playlist for slices
        """
        ...
        pass

    def __repr__(self) -> str:
        return f"Playlist({self._songs!r})"

    def __eq__(self, other) -> bool:
        if isinstance(other, Playlist):
            return self._songs == other._songs
        return False


playlist = Playlist(["Song A", "Song B", "Song C", "Song D"])

# Test __len__
assert len(playlist) == 4

# Test indexing
assert playlist[0] == "Song A"
assert playlist[-1] == "Song D"

# Test slicing returns Playlist
sliced = playlist[1:3]
assert isinstance(sliced, Playlist), f"Expected Playlist, got {type(sliced)}"
assert sliced == Playlist(["Song B", "Song C"])

# Test isinstance with ABC
assert isinstance(playlist, Sized)  # Has __len__

print("✓ Exercise 2 passed: Full Sequence Protocol")


# =============================================================================
# Exercise 3: Goose Typing with ABCs
# =============================================================================
# Use isinstance with ABCs for type checking

def describe_collection(obj) -> str:
    """
    Return a description of what kind of collection obj is.

    TODO: Implement using isinstance checks with ABCs
    - If MutableSequence: return "mutable sequence"
    - Elif Sequence: return "immutable sequence"
    - Elif Iterable: return "iterable"
    - Else: return "not a collection"

    Hint: Check more specific types first!
    """
    ...
    pass


# Test with various types
assert describe_collection([1, 2, 3]) == "mutable sequence"
assert describe_collection((1, 2, 3)) == "immutable sequence"
assert describe_collection("hello") == "immutable sequence"
assert describe_collection({1, 2, 3}) == "iterable"  # Set is Iterable but not Sequence
assert describe_collection(range(10)) == "immutable sequence"
assert describe_collection(42) == "not a collection"

print("✓ Exercise 3 passed: Goose Typing with ABCs")


# =============================================================================
# Exercise 4: Creating an ABC
# =============================================================================
# Define an abstract base class with abstract and concrete methods

class Container(ABC):
    """
    An abstract container that can add, remove, and count items.

    TODO: Implement this ABC with:
    - Abstract method: add(item) -> None
    - Abstract method: remove(item) -> Any (returns removed item)
    - Abstract method: __len__() -> int
    - Concrete method: is_empty() -> bool (returns True if len is 0)
    - Concrete method: clear() -> None (removes all items one by one)
    """

    @abstractmethod
    def add(self, item: Any) -> None:
        """Add an item to the container."""
        ...

    # TODO: Add more abstract methods here
    ...

    def is_empty(self) -> bool:
        """Return True if container is empty."""
        # TODO: Implement using __len__
        ...
        pass

    def clear(self) -> None:
        """Remove all items from the container."""
        # TODO: Implement by calling remove repeatedly
        ...
        pass


# Test that ABC cannot be instantiated
try:
    c = Container()
    assert False, "Should not be able to instantiate ABC"
except TypeError:
    pass  # Expected

print("✓ Exercise 4 passed: Creating an ABC")


# =============================================================================
# Exercise 5: Implementing an ABC
# =============================================================================
# Create a concrete class that implements the Container ABC

class Bag(Container):
    """
    A bag that holds items (allows duplicates).

    TODO: Implement all abstract methods from Container
    """

    def __init__(self):
        self._items: list[Any] = []

    def add(self, item: Any) -> None:
        """Add item to the bag."""
        # TODO: Implement
        ...
        pass

    def remove(self, item: Any) -> Any:
        """
        Remove and return an item equal to the given item.
        Raise LookupError if not found.
        """
        # TODO: Implement
        ...
        pass

    def __len__(self) -> int:
        """Return number of items."""
        # TODO: Implement
        ...
        pass

    def __repr__(self) -> str:
        return f"Bag({self._items!r})"


bag = Bag()
assert bag.is_empty() == True
assert len(bag) == 0

bag.add("apple")
bag.add("banana")
bag.add("apple")  # Duplicates allowed
assert len(bag) == 3
assert bag.is_empty() == False

removed = bag.remove("apple")
assert removed == "apple"
assert len(bag) == 2

bag.clear()
assert bag.is_empty() == True

# Test LookupError
try:
    bag.remove("not there")
    assert False, "Should raise LookupError"
except LookupError:
    pass

print("✓ Exercise 5 passed: Implementing an ABC")


# =============================================================================
# Exercise 6: Virtual Subclass with register
# =============================================================================
# Register a class as a virtual subclass of an ABC

class CardDeck:
    """A deck of cards - will be registered as a virtual Sequence."""

    def __init__(self):
        self._cards = [f"{r}{s}" for s in "♠♥♦♣" for r in "A23456789TJQK"]

    def __len__(self) -> int:
        return len(self._cards)

    def __getitem__(self, position):
        return self._cards[position]


# TODO: Register CardDeck as a virtual subclass of Sequence
# Use: Sequence.register(CardDeck)
# Or: @Sequence.register decorator (already defined, so use the function form)
...


deck = CardDeck()

# After registration, isinstance checks should pass
assert isinstance(deck, Sequence), "CardDeck should be a virtual Sequence"
assert issubclass(CardDeck, Sequence), "CardDeck should be a subclass of Sequence"

# But CardDeck doesn't inherit Sequence methods like .index()
# It just promises to implement the protocol

print("✓ Exercise 6 passed: Virtual Subclass with register")


# =============================================================================
# Exercise 7: Static Protocol
# =============================================================================
# Define a typing.Protocol for static duck typing

@runtime_checkable
class Drawable(Protocol):
    """
    Protocol for objects that can be drawn.

    TODO: Define the protocol with:
    - Method: draw() -> str
    """

    def draw(self) -> str:
        """Draw the object and return a string representation."""
        ...


class Circle:
    """A circle that can be drawn."""

    def __init__(self, radius: float):
        self.radius = radius

    def draw(self) -> str:
        return f"○ (radius={self.radius})"


class Square:
    """A square that can be drawn."""

    def __init__(self, side: float):
        self.side = side

    def draw(self) -> str:
        return f"□ (side={self.side})"


class NotDrawable:
    """This class cannot be drawn."""
    pass


def render(shape: Drawable) -> str:
    """Render a drawable shape."""
    return shape.draw()


# Test the protocol
circle = Circle(5)
square = Square(3)

assert render(circle) == "○ (radius=5)"
assert render(square) == "□ (side=3)"

# Test runtime checking (because of @runtime_checkable)
assert isinstance(circle, Drawable)
assert isinstance(square, Drawable)
assert not isinstance(NotDrawable(), Drawable)

print("✓ Exercise 7 passed: Static Protocol")


# =============================================================================
# Exercise 8: Protocol with Multiple Methods
# =============================================================================
# Define a more complex protocol

@runtime_checkable
class DataSource(Protocol):
    """
    Protocol for data sources.

    TODO: Define with:
    - Method: read() -> str
    - Method: close() -> None
    - Property or attribute: is_open -> bool
    """

    def read(self) -> str:
        ...

    # TODO: Add close() and is_open
    ...


class FileSource:
    """A file-like data source."""

    def __init__(self, content: str):
        self._content = content
        self._is_open = True

    @property
    def is_open(self) -> bool:
        return self._is_open

    def read(self) -> str:
        if not self._is_open:
            raise ValueError("Source is closed")
        return self._content

    def close(self) -> None:
        self._is_open = False


class NetworkSource:
    """A network data source."""

    def __init__(self, data: str):
        self._data = data
        self.is_open = True  # Using attribute, not property

    def read(self) -> str:
        return self._data

    def close(self) -> None:
        self.is_open = False


def read_and_close(source: DataSource) -> str:
    """Read from source and close it."""
    try:
        return source.read()
    finally:
        source.close()


# Test FileSource
fs = FileSource("file data")
assert isinstance(fs, DataSource)
assert fs.is_open == True
result = read_and_close(fs)
assert result == "file data"
assert fs.is_open == False

# Test NetworkSource
ns = NetworkSource("network data")
assert isinstance(ns, DataSource)
result = read_and_close(ns)
assert result == "network data"
assert ns.is_open == False

print("✓ Exercise 8 passed: Protocol with Multiple Methods")


# =============================================================================
# Exercise 9: Defensive Programming - Fail Fast
# =============================================================================
# Implement defensive input handling

def process_items(items) -> list:
    """
    Process items and return as list.

    TODO: Implement defensive programming:
    - Convert items to list immediately (fail fast if not iterable)
    - This catches invalid input at the start, not later
    """
    ...
    pass


# Should work with various iterables
assert process_items([1, 2, 3]) == [1, 2, 3]
assert process_items((1, 2, 3)) == [1, 2, 3]
assert process_items(range(3)) == [0, 1, 2]
assert process_items("abc") == ['a', 'b', 'c']

# Should fail fast with non-iterable
try:
    process_items(42)
    assert False, "Should fail for non-iterable"
except TypeError:
    pass

print("✓ Exercise 9 passed: Defensive Programming - Fail Fast")


# =============================================================================
# Exercise 10: Handle String or Iterable
# =============================================================================
# Duck type handling of different input types

def parse_tags(tags) -> tuple[str, ...]:
    """
    Parse tags from either a comma-separated string or an iterable.

    TODO: Implement
    - If tags is a string: split by comma and strip whitespace
    - Otherwise: assume it's an iterable of strings
    - Return as tuple

    Examples:
        parse_tags("a, b, c") -> ('a', 'b', 'c')
        parse_tags(['a', 'b']) -> ('a', 'b')
    """
    ...
    pass


# Test with string
assert parse_tags("python, java, rust") == ('python', 'java', 'rust')
assert parse_tags("single") == ('single',)

# Test with list
assert parse_tags(['python', 'java']) == ('python', 'java')

# Test with tuple
assert parse_tags(('a', 'b', 'c')) == ('a', 'b', 'c')

# Test with generator
assert parse_tags(x for x in ['a', 'b']) == ('a', 'b')

print("✓ Exercise 10 passed: Handle String or Iterable")


# =============================================================================
# Exercise 11: Custom ABC with __subclasshook__
# =============================================================================
# Create an ABC that automatically recognizes implementing classes

class Closeable(ABC):
    """
    An ABC for objects that can be closed.
    Automatically recognizes any class with a close() method.

    TODO: Implement __subclasshook__ that:
    - Returns True if the class has a 'close' method
    - Returns NotImplemented otherwise
    """

    @classmethod
    def __subclasshook__(cls, C):
        # TODO: Implement
        # Hint: Check if 'close' is in any class's __dict__ in C.__mro__
        ...
        pass

    @abstractmethod
    def close(self) -> None:
        """Close the resource."""
        ...


class Connection:
    """A connection that can be closed."""

    def close(self) -> None:
        print("Connection closed")


class Window:
    """A window with a close method."""

    def close(self) -> None:
        print("Window closed")


class Door:
    """A door - no close method."""

    def shut(self) -> None:
        print("Door shut")


# Test automatic recognition
assert isinstance(Connection(), Closeable), "Connection should be Closeable"
assert isinstance(Window(), Closeable), "Window should be Closeable"
assert not isinstance(Door(), Closeable), "Door should not be Closeable"

# issubclass should also work
assert issubclass(Connection, Closeable)
assert issubclass(Window, Closeable)
assert not issubclass(Door, Closeable)

print("✓ Exercise 11 passed: Custom ABC with __subclasshook__")


# =============================================================================
# Exercise 12: Tombola ABC (Classic Example)
# =============================================================================
# Implement a lottery-style random picker ABC

class Tombola(ABC):
    """
    Abstract base class for a random item picker.

    TODO: Define:
    - Abstract method: load(iterable) -> None - add items
    - Abstract method: pick() -> Any - remove and return random item
    - Concrete method: loaded() -> bool - True if has items
    - Concrete method: inspect() -> tuple - return sorted tuple of items
    """

    @abstractmethod
    def load(self, iterable) -> None:
        """Add items from iterable."""
        ...

    @abstractmethod
    def pick(self) -> Any:
        """Remove and return a random item. Raise LookupError if empty."""
        ...

    def loaded(self) -> bool:
        """Return True if there's at least one item."""
        # TODO: Implement using inspect()
        ...
        pass

    def inspect(self) -> tuple:
        """Return sorted tuple of current items (non-destructive)."""
        # TODO: Implement by picking all items and reloading
        ...
        pass


class LotteryBlower(Tombola):
    """A lottery blower implementation."""

    def __init__(self, iterable=None):
        self._balls = []
        if iterable:
            self.load(iterable)

    def load(self, iterable) -> None:
        self._balls.extend(iterable)

    def pick(self) -> Any:
        if not self._balls:
            raise LookupError("pick from empty LotteryBlower")
        position = random.randrange(len(self._balls))
        return self._balls.pop(position)


# Test the implementation
blower = LotteryBlower([1, 2, 3, 4, 5])
assert blower.loaded() == True
assert set(blower.inspect()) == {1, 2, 3, 4, 5}

picked = blower.pick()
assert picked in [1, 2, 3, 4, 5]
assert len(blower.inspect()) == 4

# Empty it
while blower.loaded():
    blower.pick()

assert blower.loaded() == False

try:
    blower.pick()
    assert False, "Should raise LookupError"
except LookupError:
    pass

print("✓ Exercise 12 passed: Tombola ABC")


# =============================================================================
# Exercise 13: Using Sized ABC
# =============================================================================
# Understand how Sized recognizes classes with __len__

class Counter:
    """A simple counter with length."""

    def __init__(self, count: int):
        self._count = count

    def __len__(self) -> int:
        return self._count


class NoLength:
    """A class without __len__."""
    pass


# Test that Sized automatically recognizes __len__
counter = Counter(42)
no_len = NoLength()

# TODO: Fill in the expected values
assert isinstance(counter, Sized) == True  # Does Counter implement Sized?
assert isinstance(no_len, Sized) == False  # Does NoLength implement Sized?

# Sized uses __subclasshook__ to check for __len__
assert len(counter) == 42

print("✓ Exercise 13 passed: Using Sized ABC")


# =============================================================================
# Exercise 14: Iterator Protocol
# =============================================================================
# Implement the iterator protocol

class Countdown:
    """
    An iterator that counts down from n to 1.

    TODO: Implement __iter__ and __next__
    """

    def __init__(self, start: int):
        self.current = start

    def __iter__(self) -> 'Countdown':
        """Return self (iterators return themselves)."""
        # TODO: Implement
        ...
        pass

    def __next__(self) -> int:
        """
        Return next value or raise StopIteration.

        TODO: Implement
        - If current > 0: decrement and return the previous value
        - Otherwise: raise StopIteration
        """
        ...
        pass


# Test countdown
countdown = Countdown(5)
assert isinstance(countdown, Iterator)

result = list(countdown)
assert result == [5, 4, 3, 2, 1], f"Expected [5,4,3,2,1], got {result}"

# Test that it's exhausted
assert list(countdown) == []  # Iterator is exhausted

print("✓ Exercise 14 passed: Iterator Protocol")


# =============================================================================
# All exercises completed!
# =============================================================================
print("\n" + "=" * 60)
print("🎉 Congratulations! All Chapter 13 exercises passed!")
print("=" * 60)
