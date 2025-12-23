"""
Chapter 9: Decorators and Closures - Exercises
===============================================

Complete each exercise by replacing the `None` or `...` placeholders.
Run this file to check your answers with the assertions.
"""

import functools
import time


# =============================================================================
# Exercise 1: Understanding Closures
# =============================================================================
# Create a function that returns a closure

def make_counter(start=0):
    """
    Return a counter function that returns successive values starting from `start`.

    Example:
        counter = make_counter(10)
        counter()  # 10
        counter()  # 11
        counter()  # 12

    TODO: Implement using a closure
    Hint: You'll need to use `nonlocal` to modify the count
    """
    ...
    pass


counter = make_counter(0)
assert counter() == 0
assert counter() == 1
assert counter() == 2

counter2 = make_counter(100)
assert counter2() == 100
assert counter2() == 101

# Original counter maintains its own state
assert counter() == 3

print("✓ Exercise 1 passed: Understanding Closures")


# =============================================================================
# Exercise 2: Closure with Multiple Free Variables
# =============================================================================
# Create a more complex closure

def make_running_average():
    """
    Return a function that computes the running average of all values passed to it.

    Example:
        avg = make_running_average()
        avg(10)  # 10.0
        avg(11)  # 10.5
        avg(12)  # 11.0

    TODO: Implement using a closure
    Hint: Track both total and count, use nonlocal for both
    """
    ...
    pass


avg = make_running_average()
assert avg(10) == 10.0
assert avg(11) == 10.5
assert avg(12) == 11.0
assert avg(15) == 12.0  # (10 + 11 + 12 + 15) / 4 = 12.0

# New averager starts fresh
avg2 = make_running_average()
assert avg2(100) == 100.0
assert avg2(200) == 150.0

print("✓ Exercise 2 passed: Closure with Multiple Free Variables")


# =============================================================================
# Exercise 3: Basic Decorator
# =============================================================================
# Create a simple decorator that prints before and after function execution

def trace(func):
    """
    Decorator that prints 'Entering: <func_name>' before the function runs
    and 'Exiting: <func_name>' after it completes.

    TODO: Implement this decorator
    Hint: Use functools.wraps to preserve function metadata
    """
    ...
    pass


@trace
def greet(name):
    """Return a greeting message."""
    return f"Hello, {name}!"


# Capture print output
import io
import sys

old_stdout = sys.stdout
sys.stdout = buffer = io.StringIO()

result = greet("Alice")

output = buffer.getvalue()
sys.stdout = old_stdout

assert result == "Hello, Alice!"
assert "Entering: greet" in output, f"Expected 'Entering: greet' in output, got: {output}"
assert "Exiting: greet" in output, f"Expected 'Exiting: greet' in output, got: {output}"

# Check that metadata is preserved
assert greet.__name__ == "greet", "Decorator should preserve __name__"
assert greet.__doc__ == "Return a greeting message.", "Decorator should preserve __doc__"

print("✓ Exercise 3 passed: Basic Decorator")


# =============================================================================
# Exercise 4: Timing Decorator
# =============================================================================
# Create a decorator that measures execution time

def timer(func):
    """
    Decorator that measures and stores the execution time of a function.
    The time should be stored in an attribute `last_elapsed` on the wrapper.

    TODO: Implement this decorator
    Hint: Use time.perf_counter() for accurate timing
    """
    ...
    pass


@timer
def slow_operation(n):
    """Simulate a slow operation."""
    total = 0
    for i in range(n):
        total += i
    return total


result = slow_operation(100000)
assert result == sum(range(100000))
assert hasattr(slow_operation, 'last_elapsed'), "Should have last_elapsed attribute"
assert slow_operation.last_elapsed >= 0, "Elapsed time should be non-negative"
assert slow_operation.last_elapsed < 1, "Should complete in under a second"
assert slow_operation.__name__ == "slow_operation"

print("✓ Exercise 4 passed: Timing Decorator")


# =============================================================================
# Exercise 5: Call Counter Decorator
# =============================================================================
# Create a decorator that counts function calls

def count_calls(func):
    """
    Decorator that counts how many times a function has been called.
    The count should be accessible via a `call_count` attribute.

    TODO: Implement this decorator
    """
    ...
    pass


@count_calls
def add(a, b):
    """Add two numbers."""
    return a + b


assert add.call_count == 0
assert add(1, 2) == 3
assert add.call_count == 1
assert add(3, 4) == 7
assert add.call_count == 2
assert add(10, 20) == 30
assert add.call_count == 3

print("✓ Exercise 5 passed: Call Counter Decorator")


# =============================================================================
# Exercise 6: Registration Decorator
# =============================================================================
# Create a decorator that registers functions in a list

# This list will hold all registered functions
registered_functions = []


def register(func):
    """
    Decorator that adds the function to registered_functions list
    and returns the original function unchanged.

    TODO: Implement this decorator
    Note: This is a "registration" decorator - it doesn't wrap the function
    """
    ...
    pass


@register
def task_one():
    return "Task 1 completed"


@register
def task_two():
    return "Task 2 completed"


def task_three():  # Not decorated
    return "Task 3 completed"


assert len(registered_functions) == 2
assert task_one in registered_functions
assert task_two in registered_functions
assert task_three not in registered_functions
assert task_one() == "Task 1 completed"
assert task_two() == "Task 2 completed"

print("✓ Exercise 6 passed: Registration Decorator")


# =============================================================================
# Exercise 7: Decorator with Validation
# =============================================================================
# Create a decorator that validates function arguments

def validate_positive(func):
    """
    Decorator that raises ValueError if any positional argument is negative.

    TODO: Implement this decorator
    Hint: Check each arg in *args before calling func
    """
    ...
    pass


@validate_positive
def multiply(a, b):
    """Multiply two positive numbers."""
    return a * b


assert multiply(3, 4) == 12
assert multiply(0, 5) == 0  # Zero is allowed

try:
    multiply(-1, 5)
    assert False, "Should have raised ValueError for negative argument"
except ValueError:
    pass  # Expected

try:
    multiply(5, -2)
    assert False, "Should have raised ValueError for negative argument"
except ValueError:
    pass  # Expected

print("✓ Exercise 7 passed: Decorator with Validation")


# =============================================================================
# Exercise 8: Memoization Decorator
# =============================================================================
# Implement a simple memoization decorator

def memoize(func):
    """
    Decorator that caches function results based on arguments.
    If the function is called with the same arguments, return cached result.

    TODO: Implement this decorator
    Hint: Use a dict to store {args: result}
    """
    ...
    pass


call_count = 0


@memoize
def fibonacci(n):
    """Compute the nth Fibonacci number."""
    global call_count
    call_count += 1
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


call_count = 0
result = fibonacci(10)
assert result == 55, f"fibonacci(10) should be 55, got {result}"
# Without memoization, this would be called 177 times
# With memoization, it should be called only 11 times (0-10)
assert call_count == 11, f"Expected 11 calls with memoization, got {call_count}"

# Check cache attribute exists
assert hasattr(fibonacci, 'cache'), "Should have a cache attribute"

print("✓ Exercise 8 passed: Memoization Decorator")


# =============================================================================
# Exercise 9: Parameterized Decorator - Repeat
# =============================================================================
# Create a decorator factory that repeats function execution

def repeat(times):
    """
    Decorator factory that repeats a function `times` times.
    Returns the result of the last call.

    Usage:
        @repeat(3)
        def greet(name):
            print(f"Hello, {name}!")

    TODO: Implement this parameterized decorator
    """
    ...
    pass


execution_count = 0


@repeat(3)
def increment_counter():
    """Increment the counter."""
    global execution_count
    execution_count += 1
    return execution_count


execution_count = 0
result = increment_counter()
assert execution_count == 3, f"Function should run 3 times, ran {execution_count} times"
assert result == 3, "Should return result of last call"

# Test with different repeat count
@repeat(5)
def double(x):
    return x * 2

assert double(10) == 20  # Same result regardless of repeats

print("✓ Exercise 9 passed: Parameterized Decorator - Repeat")


# =============================================================================
# Exercise 10: Parameterized Decorator - Retry
# =============================================================================
# Create a decorator factory for retrying failed operations

def retry(max_attempts, exceptions=(Exception,)):
    """
    Decorator factory that retries a function up to max_attempts times
    if it raises one of the specified exceptions.

    Args:
        max_attempts: Maximum number of times to try
        exceptions: Tuple of exception types to catch

    TODO: Implement this parameterized decorator
    """
    ...
    pass


attempt_count = 0


@retry(max_attempts=3, exceptions=(ValueError,))
def flaky_function():
    """Fails twice, then succeeds."""
    global attempt_count
    attempt_count += 1
    if attempt_count < 3:
        raise ValueError("Not yet!")
    return "Success!"


attempt_count = 0
result = flaky_function()
assert result == "Success!"
assert attempt_count == 3


# Test with too many failures
@retry(max_attempts=2, exceptions=(ValueError,))
def always_fails():
    raise ValueError("Always fails!")


try:
    always_fails()
    assert False, "Should have raised ValueError after max attempts"
except ValueError:
    pass  # Expected


# Test that non-specified exceptions are not caught
@retry(max_attempts=3, exceptions=(ValueError,))
def raises_type_error():
    raise TypeError("Wrong type!")


try:
    raises_type_error()
    assert False, "Should have raised TypeError (not in exceptions list)"
except TypeError:
    pass  # Expected

print("✓ Exercise 10 passed: Parameterized Decorator - Retry")


# =============================================================================
# Exercise 11: Class-Based Decorator
# =============================================================================
# Implement a decorator as a class

class Logged:
    """
    Class-based decorator that logs all calls to a function.
    Stores the log as a list of tuples: (args, kwargs, result)

    Usage:
        @Logged
        def my_func(x, y):
            return x + y

        my_func(1, 2)
        my_func.log  # [(((1, 2), {}), 3)]

    TODO: Implement __init__ and __call__ methods
    Hint: Use functools.update_wrapper to preserve metadata
    """

    def __init__(self, func):
        # TODO: Store the function and initialize the log
        ...
        pass

    def __call__(self, *args, **kwargs):
        # TODO: Call the function, log the call, return the result
        ...
        pass


@Logged
def subtract(a, b):
    """Subtract b from a."""
    return a - b


assert subtract.log == []
result1 = subtract(10, 3)
assert result1 == 7
assert len(subtract.log) == 1
assert subtract.log[0] == ((10, 3), {}, 7)

result2 = subtract(5, b=2)
assert result2 == 3
assert len(subtract.log) == 2
assert subtract.log[1] == ((5,), {'b': 2}, 3)

assert subtract.__name__ == "subtract"
assert subtract.__doc__ == "Subtract b from a."

print("✓ Exercise 11 passed: Class-Based Decorator")


# =============================================================================
# Exercise 12: Stacked Decorators
# =============================================================================
# Understand how stacked decorators work

def uppercase(func):
    """Decorator that converts string result to uppercase."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return result.upper()
    return wrapper


def add_greeting(func):
    """Decorator that prepends 'Hello, ' to string result."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return "Hello, " + result
    return wrapper


# TODO: Apply decorators so that:
# 1. get_name("alice") returns "HELLO, ALICE"
# 2. Decorators should be applied in the right order
#
# Hint: Decorators are applied bottom-up, executed top-down
# @dec1
# @dec2
# def f(): ...
# is equivalent to: f = dec1(dec2(f))
# so dec2's wrapper runs first, then dec1's wrapper processes that result

# Uncomment and fix the decorator order:
# @???
# @???
def get_name(name):
    """Return the name."""
    return name


# TODO: Add the correct decorators above to make this work
# The expected flow: get_name("alice") -> "alice" -> "Hello, alice" -> "HELLO, ALICE"

# Uncomment the assertion when you've added the decorators:
# assert get_name("alice") == "HELLO, ALICE", f"Got: {get_name('alice')}"

# For now, let's test with manual application to verify understanding
test_func = uppercase(add_greeting(get_name))
assert test_func("alice") == "HELLO, ALICE", f"Got: {test_func('alice')}"

print("✓ Exercise 12 passed: Stacked Decorators")


# =============================================================================
# Exercise 13: Decorator with Optional Arguments
# =============================================================================
# Create a decorator that works with or without arguments

def debug(func=None, *, prefix='DEBUG'):
    """
    Decorator that prints debug info before each call.
    Can be used with or without arguments:

        @debug
        def f(): ...

        @debug(prefix='INFO')
        def g(): ...

    TODO: Implement this flexible decorator
    Hint: If func is None, return a decorator; otherwise, decorate func
    """
    ...
    pass


@debug
def func_a():
    """Function A."""
    return "A"


@debug(prefix='INFO')
def func_b():
    """Function B."""
    return "B"


# Capture output
old_stdout = sys.stdout
sys.stdout = buffer = io.StringIO()

result_a = func_a()
result_b = func_b()

output = buffer.getvalue()
sys.stdout = old_stdout

assert result_a == "A"
assert result_b == "B"
assert "DEBUG" in output, f"Expected 'DEBUG' in output: {output}"
assert "INFO" in output, f"Expected 'INFO' in output: {output}"
assert func_a.__name__ == "func_a"
assert func_b.__name__ == "func_b"

print("✓ Exercise 13 passed: Decorator with Optional Arguments")


# =============================================================================
# Exercise 14: Closure Introspection
# =============================================================================
# Explore closure internals

def make_multiplier(factor):
    """
    Return a function that multiplies its argument by factor.

    TODO: Implement this closure
    """
    ...
    pass


double = make_multiplier(2)
triple = make_multiplier(3)

assert double(5) == 10
assert triple(5) == 15

# Inspect closure
assert double.__code__.co_freevars == ('factor',), "Should have 'factor' as free variable"
assert double.__closure__ is not None, "Should have a closure"
assert double.__closure__[0].cell_contents == 2, "Closure should contain factor=2"
assert triple.__closure__[0].cell_contents == 3, "Closure should contain factor=3"

print("✓ Exercise 14 passed: Closure Introspection")


# =============================================================================
# Exercise 15: Practical - Rate Limiter Decorator
# =============================================================================
# Create a decorator that limits how often a function can be called

def rate_limit(min_interval):
    """
    Decorator factory that ensures a function can only be called
    once per min_interval seconds. If called too soon, it returns None
    without executing the function.

    Args:
        min_interval: Minimum seconds between calls

    TODO: Implement this decorator
    Hint: Store the last call time in the wrapper function
    """
    ...
    pass


@rate_limit(0.1)  # Max once per 0.1 seconds
def limited_func():
    """A rate-limited function."""
    return "OK"


# First call should work
result1 = limited_func()
assert result1 == "OK", f"First call should work, got {result1}"

# Immediate second call should be blocked
result2 = limited_func()
assert result2 is None, f"Second call too soon should return None, got {result2}"

# Wait and try again
time.sleep(0.15)
result3 = limited_func()
assert result3 == "OK", f"Call after waiting should work, got {result3}"

print("✓ Exercise 15 passed: Rate Limiter Decorator")


# =============================================================================
# All exercises completed!
# =============================================================================
print("\n" + "=" * 60)
print("🎉 Congratulations! All Chapter 9 exercises passed!")
print("=" * 60)
