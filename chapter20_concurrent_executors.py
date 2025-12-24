"""
Chapter 19: Concurrent Executors - Exercises
=============================================

Practice using ThreadPoolExecutor and ProcessPoolExecutor
from the concurrent.futures module.

Run this file to check your implementations.
"""

import time
import os
from concurrent import futures
from typing import Any, Callable
from collections.abc import Iterator

# =============================================================================
# Exercise 1: Basic ThreadPoolExecutor with map
# =============================================================================
# Use ThreadPoolExecutor.map to compute squares of numbers concurrently.

def compute_square(n: int) -> int:
    """Simulate slow computation of square."""
    time.sleep(0.05)  # Simulate work
    return n * n


def parallel_squares(numbers: list[int]) -> list[int]:
    """Compute squares using ThreadPoolExecutor.map."""
    # TODO: Use ThreadPoolExecutor with map to compute squares
    # Return results as a list
    pass


# Test Exercise 1
start = time.perf_counter()
result = parallel_squares(list(range(10)))
elapsed = time.perf_counter() - start

assert result == [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
# Should be much faster than sequential (0.5s)
assert elapsed < 0.3, f"Should be concurrent, took {elapsed}s"
print("✓ Exercise 1 passed: ThreadPoolExecutor.map")


# =============================================================================
# Exercise 2: Using submit and result
# =============================================================================
# Use executor.submit to submit tasks and collect futures.

def parallel_squares_submit(numbers: list[int]) -> list[int]:
    """Compute squares using submit and collecting results."""
    # TODO: Use executor.submit for each number
    # Collect futures in a list
    # Return results in the same order as inputs
    pass


# Test Exercise 2
result = parallel_squares_submit(list(range(10)))
assert result == [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
print("✓ Exercise 2 passed: submit and result")


# =============================================================================
# Exercise 3: as_completed for Fast Results
# =============================================================================
# Use as_completed to process results as they become available.

def slow_task(n: int) -> tuple[int, int]:
    """Sleep for n/100 seconds, return (n, n*n)."""
    time.sleep(n / 100)
    return (n, n * n)


def process_as_completed(numbers: list[int]) -> list[tuple[int, int]]:
    """Process numbers and return results in completion order."""
    # TODO: Use executor.submit for each number
    # Use futures.as_completed to get results as they finish
    # Return list of (n, n*n) tuples in COMPLETION order
    pass


# Test Exercise 3
# Numbers with varying "difficulty" (sleep time)
numbers = [5, 1, 3, 2, 4]
result = process_as_completed(numbers)

# Results should be in completion order, not input order
# [1, 2, 3, 4, 5] order of completion based on sleep times
assert len(result) == 5
assert result[0] == (1, 1), "Fastest (1) should complete first"
assert result[-1] == (5, 25), "Slowest (5) should complete last"
print("✓ Exercise 3 passed: as_completed")


# =============================================================================
# Exercise 4: Future with Callback
# =============================================================================
# Add a callback to be executed when a future completes.

completed_results: list[int] = []


def on_complete(future: futures.Future) -> None:
    """Callback that appends result to completed_results."""
    # TODO: Get the result from the future and append to completed_results
    pass


def run_with_callbacks(numbers: list[int]) -> None:
    """Submit tasks with callbacks."""
    # TODO: Submit each number to compute_square
    # Add on_complete as a callback to each future
    # Wait for all to complete
    pass


# Test Exercise 4
completed_results.clear()
run_with_callbacks([1, 2, 3, 4, 5])
time.sleep(0.2)  # Wait for callbacks

assert sorted(completed_results) == [1, 4, 9, 16, 25]
print("✓ Exercise 4 passed: Callbacks")


# =============================================================================
# Exercise 5: Error Handling with Futures
# =============================================================================
# Handle exceptions raised by tasks.

def might_fail(n: int) -> int:
    """Raise ValueError for negative numbers."""
    if n < 0:
        raise ValueError(f"Negative number: {n}")
    time.sleep(0.02)
    return n * 2


def safe_parallel_process(numbers: list[int]) -> dict[int, int | str]:
    """Process numbers, handling errors gracefully.

    Returns dict mapping input to result or error message.
    """
    # TODO: Submit all numbers
    # Collect results, catching exceptions
    # Return {input: result} or {input: "Error: message"}
    pass


# Test Exercise 5
result = safe_parallel_process([1, -2, 3, -4, 5])

assert result[1] == 2
assert result[3] == 6
assert result[5] == 10
assert "Error" in result[-2]
assert "Error" in result[-4]
print("✓ Exercise 5 passed: Error handling")


# =============================================================================
# Exercise 6: Timeout Handling
# =============================================================================
# Handle timeouts when waiting for results.

def slow_operation(n: int) -> int:
    """Sleep for n/10 seconds, return n*10."""
    time.sleep(n / 10)
    return n * 10


def get_with_timeout(n: int, timeout: float) -> int | None:
    """Run slow_operation with a timeout. Return None on timeout."""
    # TODO: Submit slow_operation
    # Use future.result(timeout=...) to wait
    # Return None if TimeoutError occurs
    pass


# Test Exercise 6
# Should succeed (0.1s < 0.5s timeout)
result = get_with_timeout(1, 0.5)
assert result == 10

# Should timeout (0.5s > 0.2s timeout)
result = get_with_timeout(5, 0.2)
assert result is None
print("✓ Exercise 6 passed: Timeout handling")


# =============================================================================
# Exercise 7: ProcessPoolExecutor for CPU-bound Tasks
# =============================================================================
# Use ProcessPoolExecutor for CPU-intensive work.

def is_prime(n: int) -> bool:
    """Check if n is prime (CPU-intensive for large n)."""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(n ** 0.5) + 1, 2):
        if n % i == 0:
            return False
    return True


def check_primes_parallel(numbers: list[int]) -> dict[int, bool]:
    """Check primality of numbers using ProcessPoolExecutor."""
    # TODO: Use ProcessPoolExecutor with map
    # Return dict mapping number to is_prime result
    pass


# Test Exercise 7
numbers = [2, 17, 18, 19, 20, 97, 100]
result = check_primes_parallel(numbers)

assert result[2] == True
assert result[17] == True
assert result[18] == False
assert result[19] == True
assert result[20] == False
assert result[97] == True
assert result[100] == False
print("✓ Exercise 7 passed: ProcessPoolExecutor")


# =============================================================================
# Exercise 8: Controlling max_workers
# =============================================================================
# Compare performance with different numbers of workers.

def timed_parallel_run(numbers: list[int], max_workers: int) -> float:
    """Run compute_square on numbers with specified max_workers.

    Returns elapsed time.
    """
    # TODO: Create ThreadPoolExecutor with specific max_workers
    # Map compute_square over numbers
    # Return elapsed time
    pass


# Test Exercise 8
numbers = list(range(20))

# With 1 worker (sequential)
time_1 = timed_parallel_run(numbers, max_workers=1)

# With 10 workers (concurrent)
time_10 = timed_parallel_run(numbers, max_workers=10)

# Concurrent should be faster
assert time_10 < time_1 / 2, "10 workers should be at least 2x faster than 1"
print("✓ Exercise 8 passed: Controlling max_workers")


# =============================================================================
# Exercise 9: Mapping with Multiple Arguments
# =============================================================================
# Use executor.map with multiple iterables.

def add(a: int, b: int) -> int:
    """Add two numbers with simulated delay."""
    time.sleep(0.02)
    return a + b


def parallel_add(list_a: list[int], list_b: list[int]) -> list[int]:
    """Add corresponding elements from two lists in parallel."""
    # TODO: Use executor.map with two iterables
    # map(func, iter1, iter2) calls func(iter1[0], iter2[0]), etc.
    pass


# Test Exercise 9
result = parallel_add([1, 2, 3, 4, 5], [10, 20, 30, 40, 50])
assert result == [11, 22, 33, 44, 55]
print("✓ Exercise 9 passed: Map with multiple arguments")


# =============================================================================
# Exercise 10: wait() for Controlling Completion
# =============================================================================
# Use futures.wait to wait for specific conditions.

def get_first_result(numbers: list[int]) -> tuple[int, int]:
    """Return the first completed (input, result) pair."""
    # TODO: Submit slow_task for each number
    # Use futures.wait with return_when=FIRST_COMPLETED
    # Return the result from the first completed future
    # Cancel remaining futures
    pass


# Test Exercise 10
# 1 should complete first (0.01s sleep)
result = get_first_result([5, 3, 1, 4, 2])
assert result == (1, 1), "Task with n=1 should complete first"
print("✓ Exercise 10 passed: wait with FIRST_COMPLETED")


# =============================================================================
# Exercise 11: Custom Future-to-Input Mapping
# =============================================================================
# Track which input each future corresponds to.

def parallel_with_tracking(items: list[str]) -> dict[str, str]:
    """Process items and return {item: result} mapping."""

    def process(item: str) -> str:
        time.sleep(0.02)
        return item.upper()

    # TODO: Create dict mapping future -> item
    # Submit all items
    # Use as_completed and the mapping to build result dict
    pass


# Test Exercise 11
items = ["apple", "banana", "cherry"]
result = parallel_with_tracking(items)

assert result == {"apple": "APPLE", "banana": "BANANA", "cherry": "CHERRY"}
print("✓ Exercise 11 passed: Future-to-input tracking")


# =============================================================================
# Exercise 12: Executor as Context Manager vs Manual
# =============================================================================
# Understand the difference between context manager and manual shutdown.

def run_with_context_manager(numbers: list[int]) -> list[int]:
    """Use executor as context manager."""
    # TODO: Use 'with' statement
    # The executor.shutdown(wait=True) is called automatically
    pass


def run_with_manual_shutdown(numbers: list[int]) -> list[int]:
    """Create executor manually and shutdown explicitly."""
    # TODO: Create executor without 'with'
    # Remember to call shutdown(wait=True)
    pass


# Test Exercise 12
result1 = run_with_context_manager([1, 2, 3])
result2 = run_with_manual_shutdown([1, 2, 3])

assert result1 == [1, 4, 9]
assert result2 == [1, 4, 9]
print("✓ Exercise 12 passed: Context manager vs manual shutdown")


# =============================================================================
# Exercise 13: Chaining Futures
# =============================================================================
# Chain operations: result of one future feeds into another.

def double(n: int) -> int:
    time.sleep(0.02)
    return n * 2


def square(n: int) -> int:
    time.sleep(0.02)
    return n * n


def chain_operations(n: int) -> int:
    """Double n, then square the result, using futures."""
    # TODO: Submit double(n)
    # When done, submit square(result)
    # Return final result
    # Hint: Use callbacks or wait for first then submit second
    pass


# Test Exercise 13
result = chain_operations(5)
assert result == 100, f"double(5)=10, square(10)=100, got {result}"
print("✓ Exercise 13 passed: Chaining futures")


# =============================================================================
# Exercise 14: Batch Processing with Executor
# =============================================================================
# Process items in batches to control memory usage.

def process_item(item: int) -> int:
    """Process a single item."""
    time.sleep(0.01)
    return item * 2


def batch_process(items: list[int], batch_size: int) -> list[int]:
    """Process items in batches of batch_size."""
    # TODO: Split items into batches
    # Process each batch with executor.map
    # Combine results from all batches
    pass


# Test Exercise 14
items = list(range(25))
result = batch_process(items, batch_size=10)

assert result == [i * 2 for i in range(25)]
print("✓ Exercise 14 passed: Batch processing")


# =============================================================================
# Exercise 15: Comparing Thread vs Process Executor Performance
# =============================================================================
# Measure performance difference for I/O-bound vs CPU-bound tasks.

def io_bound_task(n: int) -> int:
    """I/O-bound: mostly waiting."""
    time.sleep(0.05)
    return n


def cpu_bound_task(n: int) -> int:
    """CPU-bound: heavy computation."""
    total = 0
    for i in range(100000):
        total += i * n
    return total


def compare_executors(
    task: Callable[[int], int],
    numbers: list[int]
) -> tuple[float, float]:
    """Run task with both executors, return (thread_time, process_time)."""
    # TODO: Run task on numbers with ThreadPoolExecutor, measure time
    # TODO: Run task on numbers with ProcessPoolExecutor, measure time
    # Return (thread_time, process_time)
    pass


# Test Exercise 15
numbers = list(range(8))

# I/O-bound: threads should be similar or faster than processes
io_thread, io_process = compare_executors(io_bound_task, numbers)
assert io_thread < io_process * 2, "Threads shouldn't be much slower for I/O"

# CPU-bound: processes may be faster (depends on cores)
# We just verify both work correctly
cpu_thread, cpu_process = compare_executors(cpu_bound_task, numbers)
assert cpu_thread > 0 and cpu_process > 0

print("✓ Exercise 15 passed: Comparing executors")
print(f"  I/O-bound: threads={io_thread:.3f}s, processes={io_process:.3f}s")
print(f"  CPU-bound: threads={cpu_thread:.3f}s, processes={cpu_process:.3f}s")


# =============================================================================
print("\n" + "=" * 60)
print("Congratulations! All Chapter 19 exercises completed!")
print("=" * 60)
