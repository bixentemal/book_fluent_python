"""
Chapter 2: An Array of Sequences - Exercises
=============================================

Complete each exercise by replacing the `None` or `...` placeholders.
Run this file to check your answers with the assertions.
"""

from collections import deque
from array import array

# =============================================================================
# Exercise 1: List Comprehensions
# =============================================================================
# Use list comprehensions to transform data

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# TODO: Create a list of squares of all numbers
squares = None

# TODO: Create a list of only even numbers
evens = None

# TODO: Create a list of squares of only even numbers
even_squares = None

assert squares == [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
assert evens == [2, 4, 6, 8, 10]
assert even_squares == [4, 16, 36, 64, 100]
print("✓ Exercise 1 passed: List Comprehensions")


# =============================================================================
# Exercise 2: Cartesian Product
# =============================================================================
# Use nested list comprehension for combinations

colors = ['red', 'blue']
sizes = ['S', 'M', 'L']

# TODO: Create all combinations as tuples (color, size)
# Order: all sizes for first color, then all sizes for second color
# Expected: [('red', 'S'), ('red', 'M'), ('red', 'L'), ('blue', 'S'), ...]
combinations = None

assert combinations == [
    ('red', 'S'), ('red', 'M'), ('red', 'L'),
    ('blue', 'S'), ('blue', 'M'), ('blue', 'L')
]
print("✓ Exercise 2 passed: Cartesian Product")


# =============================================================================
# Exercise 3: Nested List Comprehension - Flatten
# =============================================================================
# Flatten a nested list

matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

# TODO: Flatten to [1, 2, 3, 4, 5, 6, 7, 8, 9]
# Hint: [x for row in matrix for x in row]
flat = None

# TODO: Transpose the matrix (swap rows and columns)
# [[1, 4, 7], [2, 5, 8], [3, 6, 9]]
transposed = None

assert flat == [1, 2, 3, 4, 5, 6, 7, 8, 9]
assert transposed == [[1, 4, 7], [2, 5, 8], [3, 6, 9]]
print("✓ Exercise 3 passed: Flatten and Transpose")


# =============================================================================
# Exercise 4: Generator Expressions
# =============================================================================
# Use generator expressions instead of list comprehensions

# TODO: Calculate sum of squares from 1 to 1000 using a generator expression
# (Don't build a list in memory)
sum_of_squares = None

# TODO: Create a tuple of ASCII codes for uppercase letters in 'Hello World'
# Use a generator expression with tuple()
ascii_codes = None

assert sum_of_squares == sum(x**2 for x in range(1, 1001))
assert ascii_codes == (72, 87)  # H and W
print("✓ Exercise 4 passed: Generator Expressions")


# =============================================================================
# Exercise 5: Tuple Unpacking
# =============================================================================
# Practice various unpacking patterns

# TODO: Swap these variables without using a temp variable
a = 1
b = 2
# Your code here (one line)
...

assert a == 2 and b == 1, f"a should be 2, b should be 1, got a={a}, b={b}"

# TODO: Unpack the coordinates
point3d = (10, 20, 30)
x = y = z = None  # Replace with unpacking
...

assert x == 10 and y == 20 and z == 30

# TODO: Unpack first, last, and middle elements
numbers = [1, 2, 3, 4, 5]
first = None
middle = None
last = None
# Your code here (use * for middle)
...

assert first == 1
assert middle == [2, 3, 4]
assert last == 5

print("✓ Exercise 5 passed: Tuple Unpacking")


# =============================================================================
# Exercise 6: Nested Unpacking
# =============================================================================
# Unpack nested structures

metro_areas = [
    ('Tokyo', 'JP', 36.9, (35.68, 139.69)),
    ('Delhi', 'IN', 28.5, (28.61, 77.20)),
    ('Shanghai', 'CN', 25.5, (31.23, 121.47)),
]

# TODO: Extract city names and their latitudes using nested unpacking
# Result: [('Tokyo', 35.68), ('Delhi', 28.61), ('Shanghai', 31.23)]
city_lats = None

# Hint: for name, _, _, (lat, _) in metro_areas: ...

assert city_lats == [('Tokyo', 35.68), ('Delhi', 28.61), ('Shanghai', 31.23)]
print("✓ Exercise 6 passed: Nested Unpacking")


# =============================================================================
# Exercise 7: Slicing
# =============================================================================
# Practice slicing operations

s = "Hello, World!"

# TODO: Get the last 6 characters
last_six = None

# TODO: Reverse the string
reversed_s = None

# TODO: Get every other character starting from index 0
every_other = None

# TODO: Get characters from index 2 to 8 (exclusive)
middle = None

assert last_six == "World!"
assert reversed_s == "!dlroW ,olleH"
assert every_other == "Hlo ol!"
assert middle == "llo, W"
print("✓ Exercise 7 passed: Slicing")


# =============================================================================
# Exercise 8: Slice Assignment
# =============================================================================
# Modify lists using slice assignment

numbers = list(range(10))  # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

# TODO: Replace elements at index 2, 3, 4 with [20, 30]
# Result: [0, 1, 20, 30, 5, 6, 7, 8, 9]
numbers[2:5] = None  # Fix this

assert numbers == [0, 1, 20, 30, 5, 6, 7, 8, 9], f"Got {numbers}"

# Reset
numbers = list(range(10))

# TODO: Insert [100, 200] between index 2 and 3 (without replacing anything)
# Result: [0, 1, 2, 100, 200, 3, 4, 5, 6, 7, 8, 9]
# Hint: Use an empty slice
...

assert numbers == [0, 1, 2, 100, 200, 3, 4, 5, 6, 7, 8, 9], f"Got {numbers}"
print("✓ Exercise 8 passed: Slice Assignment")


# =============================================================================
# Exercise 9: Sequence Repetition Pitfall
# =============================================================================
# Understand the difference between correct and incorrect list multiplication

# WRONG way - creates references to the same list
wrong_board = [[' '] * 3] * 3

# Modify one cell
wrong_board[0][0] = 'X'

# TODO: What does wrong_board look like now?
# (All rows share the same list!)
expected_wrong = None

assert wrong_board == expected_wrong

# TODO: Create a 3x3 board the CORRECT way using list comprehension
# Each row should be an independent list
correct_board = None

# Modify one cell
correct_board[0][0] = 'X'

assert correct_board == [['X', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
print("✓ Exercise 9 passed: Sequence Repetition Pitfall")


# =============================================================================
# Exercise 10: Using deque
# =============================================================================
# Implement a simple task queue using deque

from collections import deque

class TaskQueue:
    """A simple FIFO task queue."""

    def __init__(self, maxlen=None):
        # TODO: Initialize a deque with optional maxlen
        self._queue = None

    def add_task(self, task):
        """Add task to the end of the queue."""
        # TODO: Implement
        ...
        pass

    def get_task(self):
        """Get and remove the first task. Return None if empty."""
        # TODO: Implement using popleft
        ...
        pass

    def __len__(self):
        return len(self._queue)


queue = TaskQueue()
queue.add_task("task1")
queue.add_task("task2")
queue.add_task("task3")

assert len(queue) == 3
assert queue.get_task() == "task1"
assert queue.get_task() == "task2"
assert len(queue) == 1
assert queue.get_task() == "task3"
assert queue.get_task() is None  # Empty queue returns None

# Test with maxlen
limited_queue = TaskQueue(maxlen=2)
limited_queue.add_task("a")
limited_queue.add_task("b")
limited_queue.add_task("c")  # "a" should be dropped
assert len(limited_queue) == 2
assert limited_queue.get_task() == "b"

print("✓ Exercise 10 passed: Using deque")


# =============================================================================
# Exercise 11: Rotating a deque
# =============================================================================
# Use deque.rotate for circular operations

def rotate_list(items, n):
    """
    Rotate items by n positions.
    Positive n: rotate right (last items move to front)
    Negative n: rotate left (first items move to end)

    Example:
        rotate_list([1, 2, 3, 4, 5], 2) == [4, 5, 1, 2, 3]
        rotate_list([1, 2, 3, 4, 5], -2) == [3, 4, 5, 1, 2]

    TODO: Implement using deque.rotate
    """
    ...
    pass


assert rotate_list([1, 2, 3, 4, 5], 2) == [4, 5, 1, 2, 3]
assert rotate_list([1, 2, 3, 4, 5], -2) == [3, 4, 5, 1, 2]
assert rotate_list([1, 2, 3], 0) == [1, 2, 3]
assert rotate_list([1, 2, 3], 3) == [1, 2, 3]  # Full rotation
print("✓ Exercise 11 passed: Rotating a deque")


# =============================================================================
# Exercise 12: Sorting with Multiple Keys
# =============================================================================
# Sort data using multiple criteria

students = [
    ('Alice', 'B', 22),
    ('Bob', 'A', 20),
    ('Charlie', 'B', 21),
    ('Diana', 'A', 22),
    ('Eve', 'A', 20),
]

# TODO: Sort by grade (ascending), then by age (ascending), then by name
# Expected: [('Bob', 'A', 20), ('Eve', 'A', 20), ('Diana', 'A', 22),
#            ('Charlie', 'B', 21), ('Alice', 'B', 22)]
sorted_students = None

expected = [
    ('Bob', 'A', 20),
    ('Eve', 'A', 20),
    ('Diana', 'A', 22),
    ('Charlie', 'B', 21),
    ('Alice', 'B', 22),
]
assert sorted_students == expected
print("✓ Exercise 12 passed: Sorting with Multiple Keys")


# =============================================================================
# Exercise 13: Using array.array
# =============================================================================
# Work with memory-efficient numeric arrays

from array import array

# TODO: Create an array of unsigned integers containing [1, 2, 3, 4, 5]
# Type code: 'I' for unsigned int
int_array = None

# TODO: Append the value 6 to the array
...

# TODO: Convert to bytes and back
array_bytes = None  # Get bytes from int_array
restored_array = None  # Create new array and load from bytes

assert list(int_array) == [1, 2, 3, 4, 5, 6]
assert list(restored_array) == [1, 2, 3, 4, 5, 6]
print("✓ Exercise 13 passed: Using array.array")


# =============================================================================
# Exercise 14: Practical - Sliding Window
# =============================================================================
# Implement a sliding window function

def sliding_window(sequence, window_size):
    """
    Generate sliding windows over a sequence.

    Example:
        list(sliding_window([1, 2, 3, 4, 5], 3))
        # [(1, 2, 3), (2, 3, 4), (3, 4, 5)]

    TODO: Implement using deque with maxlen
    """
    ...
    pass


result = list(sliding_window([1, 2, 3, 4, 5], 3))
assert result == [(1, 2, 3), (2, 3, 4), (3, 4, 5)]

result = list(sliding_window("abcde", 2))
assert result == [('a', 'b'), ('b', 'c'), ('c', 'd'), ('d', 'e')]

result = list(sliding_window([1, 2], 3))
assert result == []  # Window larger than sequence

print("✓ Exercise 14 passed: Sliding Window")


# =============================================================================
# Exercise 15: Practical - Chunk Iterator
# =============================================================================
# Split a sequence into chunks

def chunks(sequence, chunk_size):
    """
    Split sequence into chunks of given size.

    Example:
        list(chunks([1, 2, 3, 4, 5, 6, 7], 3))
        # [[1, 2, 3], [4, 5, 6], [7]]

    TODO: Implement using slicing
    """
    ...
    pass


result = list(chunks([1, 2, 3, 4, 5, 6, 7], 3))
assert result == [[1, 2, 3], [4, 5, 6], [7]]

result = list(chunks([1, 2, 3, 4], 2))
assert result == [[1, 2], [3, 4]]

result = list(chunks([1, 2, 3], 5))
assert result == [[1, 2, 3]]

result = list(chunks([], 3))
assert result == []

print("✓ Exercise 15 passed: Chunk Iterator")


# =============================================================================
# All exercises completed!
# =============================================================================
print("\n" + "=" * 60)
print("🎉 Congratulations! All Chapter 2 exercises passed!")
print("=" * 60)
