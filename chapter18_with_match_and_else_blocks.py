"""
Chapter 17: with, match, and else Blocks - Exercises
=====================================================

Practice context managers, pattern matching, and else clauses.

Run this file to check your implementations.
"""

import contextlib
import sys
from io import StringIO
from typing import Any, Iterator

# =============================================================================
# Exercise 1: Basic Context Manager Class
# =============================================================================
# Implement a Timer context manager that:
# - Records the start time in __enter__
# - Calculates elapsed time in __exit__
# - Stores elapsed time in self.elapsed (in seconds)
#
# Use time.perf_counter() for timing.

import time

class Timer:
    def __init__(self):
        self.elapsed: float = 0.0

    def __enter__(self):
        # TODO: Record start time, return self
        pass

    def __exit__(self, exc_type, exc_value, traceback):
        # TODO: Calculate and store elapsed time
        pass


# Test Exercise 1
with Timer() as t:
    time.sleep(0.1)
assert 0.09 < t.elapsed < 0.2, f"Timer should measure ~0.1s, got {t.elapsed}"
print("✓ Exercise 1 passed: Basic Timer context manager")


# =============================================================================
# Exercise 2: Context Manager with Exception Handling
# =============================================================================
# Implement a Suppress context manager that:
# - Takes exception types to suppress in __init__
# - Suppresses (ignores) those exceptions
# - Lets other exceptions propagate
#
# Similar to contextlib.suppress()

class Suppress:
    def __init__(self, *exceptions):
        # TODO: Store exception types to suppress
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        # TODO: Return True if exception should be suppressed
        pass


# Test Exercise 2
# Should suppress ValueError
with Suppress(ValueError):
    int("not a number")

# Should suppress multiple exception types
with Suppress(ValueError, TypeError):
    raise TypeError("test")

# Should NOT suppress KeyError
try:
    with Suppress(ValueError):
        raise KeyError("oops")
    assert False, "KeyError should propagate"
except KeyError:
    pass

print("✓ Exercise 2 passed: Suppress context manager")


# =============================================================================
# Exercise 3: @contextmanager Decorator
# =============================================================================
# Implement a 'redirect_print' context manager using @contextmanager.
# It should capture all print() output to a StringIO buffer.
# The buffer should be yielded so the caller can access captured output.

@contextlib.contextmanager
def redirect_print():
    # TODO: Redirect sys.stdout to a StringIO
    # yield the buffer
    # Restore original stdout
    pass


# Test Exercise 3
with redirect_print() as output:
    print("Hello, World!")
    print("Line 2")

captured = output.getvalue()
assert "Hello, World!" in captured, "Should capture first print"
assert "Line 2" in captured, "Should capture second print"
print("✓ Exercise 3 passed: @contextmanager redirect_print")


# =============================================================================
# Exercise 4: Context Manager with Cleanup
# =============================================================================
# Implement a TempValue context manager that:
# - Temporarily changes an attribute on an object
# - Restores the original value on exit (even if exception)
#
# Usage: with TempValue(obj, 'attr', new_value): ...

class TempValue:
    def __init__(self, obj: Any, attr: str, value: Any):
        # TODO: Store obj, attr, value, and original value
        pass

    def __enter__(self):
        # TODO: Set the temporary value
        pass

    def __exit__(self, exc_type, exc_value, traceback):
        # TODO: Restore original value
        pass


# Test Exercise 4
class Config:
    debug = False
    level = 1

config = Config()
assert config.debug == False

with TempValue(config, 'debug', True):
    assert config.debug == True, "Should have temporary value"

assert config.debug == False, "Should restore original value"

# Should restore even on exception
try:
    with TempValue(config, 'level', 99):
        assert config.level == 99
        raise RuntimeError("test")
except RuntimeError:
    pass

assert config.level == 1, "Should restore on exception"
print("✓ Exercise 4 passed: TempValue context manager")


# =============================================================================
# Exercise 5: @contextmanager with Exception Handling
# =============================================================================
# Implement 'transaction' context manager that:
# - Makes a backup of a list before the block
# - If an exception occurs, restores the list to its backup
# - If successful, keeps the changes

@contextlib.contextmanager
def transaction(the_list: list):
    # TODO: Make backup, yield, restore on exception
    pass


# Test Exercise 5
data = [1, 2, 3]

with transaction(data):
    data.append(4)
    data.append(5)

assert data == [1, 2, 3, 4, 5], "Changes should persist on success"

# Now test rollback on exception
data = [1, 2, 3]
try:
    with transaction(data):
        data.append(4)
        raise ValueError("abort!")
except ValueError:
    pass

assert data == [1, 2, 3], "Should rollback on exception"
print("✓ Exercise 5 passed: transaction context manager")


# =============================================================================
# Exercise 6: Pattern Matching - Literals and Captures
# =============================================================================
# Implement 'parse_command' using match/case that handles:
# - "quit" or "exit" -> return ("quit", None)
# - "hello NAME" -> return ("greet", NAME)
# - "add X Y" -> return ("add", (int(X), int(Y)))
# - anything else -> return ("unknown", command)

def parse_command(command: str) -> tuple[str, Any]:
    parts = command.split()
    # TODO: Use match/case on parts
    match parts:
        case _:
            pass
    return ("unknown", command)


# Test Exercise 6
assert parse_command("quit") == ("quit", None)
assert parse_command("exit") == ("quit", None)
assert parse_command("hello Alice") == ("greet", "Alice")
assert parse_command("add 3 5") == ("add", (3, 5))
assert parse_command("unknown command") == ("unknown", "unknown command")
print("✓ Exercise 6 passed: Pattern matching - commands")


# =============================================================================
# Exercise 7: Pattern Matching - Sequence Patterns
# =============================================================================
# Implement 'analyze_sequence' using match/case that returns:
# - "empty" for []
# - "single: X" for [X]
# - "pair: X, Y" for [X, Y]
# - "first: X, rest count: N" for longer sequences

def analyze_sequence(seq: list) -> str:
    # TODO: Use match/case with sequence patterns
    match seq:
        case _:
            pass
    return "unknown"


# Test Exercise 7
assert analyze_sequence([]) == "empty"
assert analyze_sequence([42]) == "single: 42"
assert analyze_sequence([1, 2]) == "pair: 1, 2"
assert analyze_sequence([1, 2, 3, 4, 5]) == "first: 1, rest count: 4"
print("✓ Exercise 7 passed: Pattern matching - sequences")


# =============================================================================
# Exercise 8: Pattern Matching - Class Patterns
# =============================================================================
# Create Point class and implement 'describe_point' using match/case:
# - Point at origin (0, 0) -> "origin"
# - Point on x-axis (x, 0) -> "on x-axis at X"
# - Point on y-axis (0, y) -> "on y-axis at Y"
# - Any other point -> "at (X, Y)"

class Point:
    # TODO: Add __match_args__ = ('x', 'y')
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y


def describe_point(point: Point) -> str:
    # TODO: Use match/case with class patterns
    match point:
        case _:
            pass
    return "unknown"


# Test Exercise 8
assert describe_point(Point(0, 0)) == "origin"
assert describe_point(Point(5, 0)) == "on x-axis at 5"
assert describe_point(Point(0, 3)) == "on y-axis at 3"
assert describe_point(Point(2, 4)) == "at (2, 4)"
print("✓ Exercise 8 passed: Pattern matching - class patterns")


# =============================================================================
# Exercise 9: Pattern Matching - Mapping Patterns
# =============================================================================
# Implement 'process_action' that handles dict actions:
# - {"type": "message", "text": T} -> f"Message: {T}"
# - {"type": "user", "name": N, "age": A} -> f"User {N}, age {A}"
# - {"type": "error", "code": C, **rest} -> f"Error {C}"
# - Any other dict with "type" key -> f"Unknown type: {type}"
# - No "type" key -> "Invalid action"

def process_action(action: dict) -> str:
    # TODO: Use match/case with mapping patterns
    match action:
        case _:
            pass
    return "Invalid action"


# Test Exercise 9
assert process_action({"type": "message", "text": "Hello"}) == "Message: Hello"
assert process_action({"type": "user", "name": "Bob", "age": 25}) == "User Bob, age 25"
assert process_action({"type": "error", "code": 404, "details": "..."}) == "Error 404"
assert process_action({"type": "other"}) == "Unknown type: other"
assert process_action({"no_type": "here"}) == "Invalid action"
print("✓ Exercise 9 passed: Pattern matching - mapping patterns")


# =============================================================================
# Exercise 10: Pattern Matching - Guards
# =============================================================================
# Implement 'categorize_number' using match/case with guards:
# - Negative numbers -> "negative"
# - Zero -> "zero"
# - 1 to 10 -> "small positive"
# - 11 to 100 -> "medium positive"
# - > 100 -> "large positive"

def categorize_number(n: int | float) -> str:
    # TODO: Use match/case with guards (if conditions)
    match n:
        case _:
            pass
    return "unknown"


# Test Exercise 10
assert categorize_number(-5) == "negative"
assert categorize_number(0) == "zero"
assert categorize_number(7) == "small positive"
assert categorize_number(50) == "medium positive"
assert categorize_number(500) == "large positive"
print("✓ Exercise 10 passed: Pattern matching - guards")


# =============================================================================
# Exercise 11: for/else Pattern
# =============================================================================
# Implement 'find_first_even' using for/else:
# - Return the first even number in the list
# - If no even number found, raise ValueError("No even number found")
#
# You MUST use the for/else pattern (not just return in loop)

def find_first_even(numbers: list[int]) -> int:
    # TODO: Use for/else pattern
    pass


# Test Exercise 11
assert find_first_even([1, 3, 4, 5]) == 4
assert find_first_even([2, 4, 6]) == 2

try:
    find_first_even([1, 3, 5, 7])
    assert False, "Should raise ValueError"
except ValueError as e:
    assert "No even number found" in str(e)

print("✓ Exercise 11 passed: for/else pattern")


# =============================================================================
# Exercise 12: while/else Pattern
# =============================================================================
# Implement 'find_in_tree' that searches a simple tree structure.
# The tree is represented as nested dicts with 'value' and 'children' keys.
# Return the path (list of indices) to the target value.
# If not found, return None.
#
# Use while/else pattern.

def find_in_tree(tree: dict, target: Any) -> list[int] | None:
    # TODO: Use while/else with a stack-based search
    # Stack items: (node, path)
    # Return path when found, None if exhausted
    pass


# Test Exercise 12
tree = {
    'value': 1,
    'children': [
        {'value': 2, 'children': []},
        {'value': 3, 'children': [
            {'value': 4, 'children': []},
            {'value': 5, 'children': []}
        ]}
    ]
}

assert find_in_tree(tree, 1) == []  # Root
assert find_in_tree(tree, 2) == [0]  # First child
assert find_in_tree(tree, 4) == [1, 0]  # Second child's first child
assert find_in_tree(tree, 5) == [1, 1]  # Second child's second child
assert find_in_tree(tree, 99) is None  # Not found
print("✓ Exercise 12 passed: while/else pattern")


# =============================================================================
# Exercise 13: try/else Pattern
# =============================================================================
# Implement 'safe_divide_and_log' that:
# - Tries to divide a by b
# - If ZeroDivisionError, returns None and appends "error" to log
# - If successful, appends the result to log and returns it
#
# Use try/else pattern to keep only the risky code in try.

def safe_divide_and_log(a: float, b: float, log: list) -> float | None:
    # TODO: Use try/else pattern
    pass


# Test Exercise 13
log: list = []
result = safe_divide_and_log(10, 2, log)
assert result == 5.0
assert log == [5.0]

result = safe_divide_and_log(10, 0, log)
assert result is None
assert log == [5.0, "error"]

result = safe_divide_and_log(20, 4, log)
assert result == 5.0
assert log == [5.0, "error", 5.0]
print("✓ Exercise 13 passed: try/else pattern")


# =============================================================================
# Exercise 14: Combining Patterns - Simple Expression Evaluator
# =============================================================================
# Implement 'evaluate' for a simple expression language:
# - Numbers evaluate to themselves
# - ["add", x, y] -> x + y
# - ["sub", x, y] -> x - y
# - ["mul", x, y] -> x * y
# - ["neg", x] -> -x
# - ["if", cond, then, else] -> then if cond else else_
#
# Expressions can be nested!

def evaluate(expr) -> int | float | bool:
    # TODO: Use match/case with recursive evaluation
    match expr:
        case _:
            pass
    raise ValueError(f"Unknown expression: {expr}")


# Test Exercise 14
assert evaluate(42) == 42
assert evaluate(["add", 2, 3]) == 5
assert evaluate(["mul", 4, 5]) == 20
assert evaluate(["neg", 10]) == -10
assert evaluate(["sub", 10, 3]) == 7

# Nested
assert evaluate(["add", ["mul", 2, 3], ["sub", 10, 5]]) == 11
assert evaluate(["neg", ["add", 1, 2]]) == -3

# Conditional
assert evaluate(["if", True, 1, 0]) == 1
assert evaluate(["if", False, 1, 0]) == 0
assert evaluate(["if", ["sub", 5, 5], "yes", "no"]) == "no"  # 0 is falsy
print("✓ Exercise 14 passed: Expression evaluator")


# =============================================================================
# BONUS Exercise 15: Full-Featured Context Manager
# =============================================================================
# Implement 'managed_file' that:
# - Opens a file with specified mode
# - Yields a wrapper object with read/write methods
# - Tracks bytes read/written
# - Closes file on exit
# - Logs operations to a provided logger function

@contextlib.contextmanager
def managed_file(path: str, mode: str = 'r', logger=None):
    """
    Context manager for file operations with logging.

    Yields a wrapper object with:
    - read(n=-1) -> str|bytes
    - write(data) -> int
    - bytes_read: int
    - bytes_written: int
    """
    # TODO: Implement file wrapper with tracking

    class FileWrapper:
        def __init__(self, file_obj):
            self._file = file_obj
            self.bytes_read = 0
            self.bytes_written = 0

        def read(self, n=-1):
            # TODO: Read and track bytes
            pass

        def write(self, data):
            # TODO: Write and track bytes
            pass

    pass  # TODO: Implement the context manager


# Test Exercise 15
import tempfile
import os

# Create a temp file for testing
with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
    temp_path = f.name
    f.write("Hello, World!")

logs = []

try:
    # Test reading
    with managed_file(temp_path, 'r', logger=logs.append) as f:
        content = f.read()
        assert content == "Hello, World!"
        assert f.bytes_read == 13

    assert any("open" in str(log).lower() for log in logs), "Should log open"
    assert any("close" in str(log).lower() for log in logs), "Should log close"

    # Test writing
    logs.clear()
    with managed_file(temp_path, 'w', logger=logs.append) as f:
        f.write("New content")
        assert f.bytes_written == 11

    # Verify write
    with open(temp_path) as f:
        assert f.read() == "New content"

finally:
    os.unlink(temp_path)

print("✓ Exercise 15 passed: Full-featured managed_file")


# =============================================================================
print("\n" + "=" * 60)
print("Congratulations! All Chapter 17 exercises completed!")
print("=" * 60)
