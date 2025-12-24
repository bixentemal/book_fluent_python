"""
Chapter 20: Asynchronous Programming - Exercises
=================================================

Practice using asyncio, native coroutines, async/await,
asynchronous context managers, and asynchronous iteration.

Run this file to check your implementations.
"""

import asyncio
import time
from typing import Any
from collections.abc import AsyncIterator

# =============================================================================
# Exercise 1: Basic Native Coroutine
# =============================================================================
# Create a native coroutine that simulates an async operation.


async def delayed_greeting(name: str, delay: float) -> str:
    """Return a greeting after waiting `delay` seconds.

    Use asyncio.sleep to simulate async I/O.
    """
    # TODO: await asyncio.sleep for `delay` seconds
    # TODO: Return f"Hello, {name}!"
    pass


# Test Exercise 1
async def test_exercise_1():
    start = time.perf_counter()
    result = await delayed_greeting("Alice", 0.1)
    elapsed = time.perf_counter() - start

    assert result == "Hello, Alice!"
    assert elapsed >= 0.1
    print("    Exercise 1 passed: Basic native coroutine")


asyncio.run(test_exercise_1())


# =============================================================================
# Exercise 2: Running Multiple Coroutines with gather
# =============================================================================
# Use asyncio.gather to run multiple coroutines concurrently.


async def fetch_value(value: int, delay: float) -> int:
    """Simulate fetching a value after a delay."""
    await asyncio.sleep(delay)
    return value * 10


async def fetch_all_values(values: list[int]) -> list[int]:
    """Fetch all values concurrently using asyncio.gather.

    Each value should have a delay of 0.05 seconds.
    Results should be in the same order as inputs.
    """
    # TODO: Create coroutines for each value
    # TODO: Use asyncio.gather to run them concurrently
    # TODO: Return the results
    pass


# Test Exercise 2
async def test_exercise_2():
    start = time.perf_counter()
    result = await fetch_all_values([1, 2, 3, 4, 5])
    elapsed = time.perf_counter() - start

    assert result == [10, 20, 30, 40, 50]
    # Should complete in ~0.05s (concurrent), not 0.25s (sequential)
    assert elapsed < 0.15, f"Should be concurrent, took {elapsed}s"
    print("    Exercise 2 passed: asyncio.gather")


asyncio.run(test_exercise_2())


# =============================================================================
# Exercise 3: Processing Results as They Complete
# =============================================================================
# Use asyncio.as_completed to process results as they finish.


async def slow_operation(n: int) -> tuple[int, int]:
    """Sleep for n/100 seconds, return (n, n*n)."""
    await asyncio.sleep(n / 100)
    return (n, n * n)


async def process_as_completed(numbers: list[int]) -> list[tuple[int, int]]:
    """Process numbers and return results in COMPLETION order.

    Hint: Use asyncio.as_completed
    """
    # TODO: Create coroutines for each number
    # TODO: Use asyncio.as_completed to get results as they finish
    # TODO: Return list of (n, n*n) tuples in completion order
    pass


# Test Exercise 3
async def test_exercise_3():
    numbers = [5, 1, 3, 2, 4]
    result = await process_as_completed(numbers)

    # Results should be in completion order (shortest sleep first)
    assert len(result) == 5
    assert result[0] == (1, 1), "Fastest (n=1) should complete first"
    assert result[-1] == (5, 25), "Slowest (n=5) should complete last"
    print("    Exercise 3 passed: asyncio.as_completed")


asyncio.run(test_exercise_3())


# =============================================================================
# Exercise 4: Creating and Awaiting Tasks
# =============================================================================
# Use asyncio.create_task to schedule coroutines for concurrent execution.


async def compute(x: int) -> int:
    """Simulate computation with a delay."""
    await asyncio.sleep(0.02)
    return x ** 2


async def parallel_compute(numbers: list[int]) -> list[int]:
    """Compute squares using create_task.

    1. Create tasks for all numbers
    2. Await all tasks to get results
    3. Return results in the same order as inputs
    """
    # TODO: Create tasks with asyncio.create_task
    # TODO: Await each task and collect results
    pass


# Test Exercise 4
async def test_exercise_4():
    start = time.perf_counter()
    result = await parallel_compute([1, 2, 3, 4, 5])
    elapsed = time.perf_counter() - start

    assert result == [1, 4, 9, 16, 25]
    assert elapsed < 0.1, "Tasks should run concurrently"
    print("    Exercise 4 passed: asyncio.create_task")


asyncio.run(test_exercise_4())


# =============================================================================
# Exercise 5: Timeout Handling
# =============================================================================
# Use asyncio.wait_for to set a timeout on a coroutine.


async def long_operation(duration: float) -> str:
    """Simulate a long operation."""
    await asyncio.sleep(duration)
    return "completed"


async def run_with_timeout(duration: float, timeout: float) -> str | None:
    """Run long_operation with a timeout.

    Return "completed" if successful, None if timeout.
    """
    # TODO: Use asyncio.wait_for to run long_operation with timeout
    # TODO: Return None if asyncio.TimeoutError occurs
    pass


# Test Exercise 5
async def test_exercise_5():
    # Should succeed (0.05s < 0.5s timeout)
    result = await run_with_timeout(0.05, 0.5)
    assert result == "completed"

    # Should timeout (0.5s > 0.1s timeout)
    result = await run_with_timeout(0.5, 0.1)
    assert result is None
    print("    Exercise 5 passed: Timeout handling")


asyncio.run(test_exercise_5())


# =============================================================================
# Exercise 6: Semaphore for Throttling
# =============================================================================
# Use asyncio.Semaphore to limit concurrent operations.

concurrent_count = 0
max_concurrent_seen = 0


async def tracked_operation(semaphore: asyncio.Semaphore, n: int) -> int:
    """Operation that tracks max concurrent executions."""
    global concurrent_count, max_concurrent_seen

    # TODO: Use 'async with semaphore:' to limit concurrency
    # Inside the semaphore block:
    #   - Increment concurrent_count
    #   - Update max_concurrent_seen if needed
    #   - await asyncio.sleep(0.02)
    #   - Decrement concurrent_count
    #   - Return n * 2
    pass


async def throttled_operations(numbers: list[int], max_concurrent: int) -> list[int]:
    """Run operations with limited concurrency."""
    global concurrent_count, max_concurrent_seen
    concurrent_count = 0
    max_concurrent_seen = 0

    # TODO: Create a Semaphore with max_concurrent
    # TODO: Create tasks using tracked_operation
    # TODO: Use asyncio.gather to run them
    pass


# Test Exercise 6
async def test_exercise_6():
    numbers = list(range(20))
    result = await throttled_operations(numbers, max_concurrent=5)

    assert result == [n * 2 for n in numbers]
    assert max_concurrent_seen <= 5, f"Max concurrent was {max_concurrent_seen}"
    print("    Exercise 6 passed: Semaphore throttling")


asyncio.run(test_exercise_6())


# =============================================================================
# Exercise 7: Asynchronous Context Manager
# =============================================================================
# Implement an async context manager class.


class AsyncTimer:
    """Async context manager that measures elapsed time.

    Usage:
        async with AsyncTimer() as timer:
            await some_operation()
        print(timer.elapsed)
    """

    def __init__(self):
        self.start_time: float = 0
        self.elapsed: float = 0

    async def __aenter__(self) -> "AsyncTimer":
        # TODO: Record start time and return self
        pass

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        # TODO: Calculate elapsed time
        pass


# Test Exercise 7
async def test_exercise_7():
    async with AsyncTimer() as timer:
        await asyncio.sleep(0.1)

    assert timer.elapsed >= 0.1
    assert timer.elapsed < 0.2
    print("    Exercise 7 passed: Async context manager")


asyncio.run(test_exercise_7())


# =============================================================================
# Exercise 8: Asynchronous Generator
# =============================================================================
# Create an asynchronous generator that yields values with delays.


async def async_countdown(start: int, delay: float) -> AsyncIterator[int]:
    """Async generator that counts down from start to 1.

    Yields each number after waiting `delay` seconds.
    """
    # TODO: Loop from start down to 1
    # TODO: await asyncio.sleep(delay) before each yield
    # TODO: yield the current number
    pass


# Test Exercise 8
async def test_exercise_8():
    results = []
    start = time.perf_counter()

    async for n in async_countdown(5, 0.02):
        results.append(n)

    elapsed = time.perf_counter() - start

    assert results == [5, 4, 3, 2, 1]
    assert elapsed >= 0.1  # 5 * 0.02 = 0.1s
    print("    Exercise 8 passed: Async generator")


asyncio.run(test_exercise_8())


# =============================================================================
# Exercise 9: async for with Processing
# =============================================================================
# Use async for to consume an async generator and process items.


async def async_range(start: int, stop: int, delay: float) -> AsyncIterator[int]:
    """Async generator similar to range."""
    for i in range(start, stop):
        await asyncio.sleep(delay)
        yield i


async def sum_async_range(start: int, stop: int) -> int:
    """Sum all values from async_range with delay=0.01."""
    # TODO: Use async for to iterate over async_range
    # TODO: Sum all values and return the total
    pass


# Test Exercise 9
async def test_exercise_9():
    result = await sum_async_range(1, 6)  # 1+2+3+4+5 = 15
    assert result == 15

    result = await sum_async_range(0, 10)  # 0+1+...+9 = 45
    assert result == 45
    print("    Exercise 9 passed: async for processing")


asyncio.run(test_exercise_9())


# =============================================================================
# Exercise 10: Async Comprehension
# =============================================================================
# Use async comprehensions to build lists from async generators.


async def async_values(items: list[int], delay: float) -> AsyncIterator[int]:
    """Yield items with delay."""
    for item in items:
        await asyncio.sleep(delay)
        yield item


async def collect_doubled(items: list[int]) -> list[int]:
    """Collect doubled values using an async comprehension.

    Use delay=0.01.
    Hint: [expr async for x in async_gen]
    """
    # TODO: Use async list comprehension to collect doubled values
    pass


# Test Exercise 10
async def test_exercise_10():
    result = await collect_doubled([1, 2, 3, 4, 5])
    assert result == [2, 4, 6, 8, 10]
    print("    Exercise 10 passed: Async comprehension")


asyncio.run(test_exercise_10())


# =============================================================================
# Exercise 11: Error Handling in Coroutines
# =============================================================================
# Handle exceptions properly in async code.


class FetchError(Exception):
    """Custom error for fetch operations."""
    pass


async def maybe_fail(n: int) -> int:
    """Raise FetchError for negative numbers."""
    await asyncio.sleep(0.01)
    if n < 0:
        raise FetchError(f"Cannot process negative: {n}")
    return n * 2


async def safe_fetch_all(numbers: list[int]) -> dict[int, int | str]:
    """Fetch all numbers, handling errors gracefully.

    Returns dict mapping input to result or error message.
    For errors, the value should be "Error: <message>"
    """
    # TODO: Use asyncio.gather with return_exceptions=True
    # OR: Create tasks and handle exceptions individually
    pass


# Test Exercise 11
async def test_exercise_11():
    result = await safe_fetch_all([1, -2, 3, -4, 5])

    assert result[1] == 2
    assert result[3] == 6
    assert result[5] == 10
    assert "Error" in result[-2]
    assert "Error" in result[-4]
    print("    Exercise 11 passed: Error handling")


asyncio.run(test_exercise_11())


# =============================================================================
# Exercise 12: Cancellation Handling
# =============================================================================
# Handle task cancellation properly.

cleanup_called = False


async def cancellable_operation() -> str:
    """Operation that handles cancellation gracefully."""
    global cleanup_called
    try:
        await asyncio.sleep(10)  # Long operation
        return "completed"
    except asyncio.CancelledError:
        # TODO: Set cleanup_called to True
        # TODO: Re-raise the CancelledError
        pass


async def run_with_cancellation() -> bool:
    """Start a task, cancel it after 0.05s, return cleanup status."""
    global cleanup_called
    cleanup_called = False

    # TODO: Create task for cancellable_operation
    # TODO: Sleep for 0.05 seconds
    # TODO: Cancel the task
    # TODO: Try to await the task, catching CancelledError
    # TODO: Return cleanup_called
    pass


# Test Exercise 12
async def test_exercise_12():
    result = await run_with_cancellation()
    assert result is True, "Cleanup should have been called"
    print("    Exercise 12 passed: Cancellation handling")


asyncio.run(test_exercise_12())


# =============================================================================
# Exercise 13: wait() with Return Conditions
# =============================================================================
# Use asyncio.wait with different return conditions.


async def timed_task(n: int) -> tuple[int, float]:
    """Task that sleeps n/100 seconds, returns (n, elapsed)."""
    start = time.perf_counter()
    await asyncio.sleep(n / 100)
    return (n, time.perf_counter() - start)


async def get_first_result(numbers: list[int]) -> tuple[int, float]:
    """Return the result of the first completed task.

    Use asyncio.wait with FIRST_COMPLETED.
    Cancel remaining tasks.
    """
    # TODO: Create tasks for each number
    # TODO: Use asyncio.wait with return_when=asyncio.FIRST_COMPLETED
    # TODO: Get result from the completed task
    # TODO: Cancel pending tasks
    pass


# Test Exercise 13
async def test_exercise_13():
    result = await get_first_result([5, 3, 1, 4, 2])
    assert result[0] == 1, "Task with n=1 should complete first"
    print("    Exercise 13 passed: asyncio.wait FIRST_COMPLETED")


asyncio.run(test_exercise_13())


# =============================================================================
# Exercise 14: Running Blocking Code
# =============================================================================
# Use asyncio.to_thread to run blocking code without blocking the loop.


def blocking_computation(n: int) -> int:
    """Simulate blocking CPU-bound computation."""
    time.sleep(0.05)  # Blocking!
    total = sum(i * i for i in range(n))
    return total


async def run_blocking_concurrently(numbers: list[int]) -> list[int]:
    """Run blocking_computation for each number concurrently.

    Use asyncio.to_thread to avoid blocking the event loop.
    """
    # TODO: Create coroutines using asyncio.to_thread
    # TODO: Use asyncio.gather to run them concurrently
    pass


# Test Exercise 14
async def test_exercise_14():
    numbers = [100, 200, 300, 400]
    start = time.perf_counter()
    results = await run_blocking_concurrently(numbers)
    elapsed = time.perf_counter() - start

    expected = [sum(i * i for i in range(n)) for n in numbers]
    assert results == expected
    # Should be concurrent: ~0.05s instead of 0.2s
    assert elapsed < 0.15, f"Should be concurrent, took {elapsed}s"
    print("    Exercise 14 passed: asyncio.to_thread")


asyncio.run(test_exercise_14())


# =============================================================================
# Exercise 15: Producer-Consumer with Queue
# =============================================================================
# Use asyncio.Queue for producer-consumer pattern.


async def producer(queue: asyncio.Queue, items: list[int]) -> None:
    """Put items into queue with small delay."""
    # TODO: For each item, await asyncio.sleep(0.01), then put item in queue
    # TODO: Put None to signal completion
    pass


async def consumer(queue: asyncio.Queue) -> list[int]:
    """Consume items from queue until None received."""
    # TODO: Loop getting items from queue
    # TODO: Break when None is received
    # TODO: Return list of consumed items
    pass


async def producer_consumer_example(items: list[int]) -> list[int]:
    """Run producer and consumer concurrently."""
    # TODO: Create asyncio.Queue
    # TODO: Run producer and consumer with asyncio.gather
    # TODO: Return consumer's result
    pass


# Test Exercise 15
async def test_exercise_15():
    items = [1, 2, 3, 4, 5]
    result = await producer_consumer_example(items)
    assert result == items
    print("    Exercise 15 passed: asyncio.Queue producer-consumer")


asyncio.run(test_exercise_15())


# =============================================================================
print("\n" + "=" * 60)
print("Congratulations! All Chapter 20 exercises completed!")
print("=" * 60)
