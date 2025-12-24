"""
Chapter 18: Concurrency Models in Python - Exercises
=====================================================

Practice threading, multiprocessing, and asyncio basics.

Run this file to check your implementations.
"""

import asyncio
import time
from threading import Thread, Event, Lock
from multiprocessing import Process, Queue as MPQueue
from queue import Queue
from typing import Any, Callable
import itertools

# =============================================================================
# Exercise 1: Basic Thread Creation
# =============================================================================
# Create a function that runs in a separate thread and appends results to a list.
# The function should compute squares of numbers from 0 to n-1.
#
# IMPORTANT: Use a lock to safely append to the shared list!

def compute_squares_threaded(n: int, results: list, lock: Lock) -> None:
    """Compute squares of 0 to n-1 and append to results list."""
    # TODO: Loop through range(n), compute square, and safely append to results
    pass


# Test Exercise 1
results: list = []
lock = Lock()
threads = [Thread(target=compute_squares_threaded, args=(5, results, lock)) for _ in range(3)]

for t in threads:
    t.start()
for t in threads:
    t.join()

# Each thread adds 5 squares, so 15 total (order may vary)
assert len(results) == 15, f"Expected 15 results, got {len(results)}"
assert set(results) == {0, 1, 4, 9, 16}, f"Wrong squares computed"
print("✓ Exercise 1 passed: Basic threaded computation with lock")


# =============================================================================
# Exercise 2: Thread Communication with Event
# =============================================================================
# Implement a producer that generates numbers and a consumer that sums them.
# Use an Event to signal when the producer is done.

def producer(numbers: list, done: Event, count: int) -> None:
    """Add numbers 1 to count to the list, then set the done event."""
    # TODO: Append numbers 1 to count, then signal done
    pass


def consumer(numbers: list, done: Event) -> int:
    """Wait for producer to finish, then return sum of numbers."""
    # TODO: Wait for done event, then return sum
    pass


# Test Exercise 2
numbers: list = []
done = Event()

prod_thread = Thread(target=producer, args=(numbers, done, 10))
prod_thread.start()

# Consumer runs in main thread
total = consumer(numbers, done)
prod_thread.join()

assert total == 55, f"Expected sum 55, got {total}"
print("✓ Exercise 2 passed: Thread communication with Event")


# =============================================================================
# Exercise 3: Thread-Safe Counter
# =============================================================================
# Implement a thread-safe counter class that can be incremented from multiple threads.

class ThreadSafeCounter:
    def __init__(self):
        self._value = 0
        # TODO: Add a lock

    def increment(self) -> None:
        """Increment the counter by 1, thread-safely."""
        # TODO: Use lock to safely increment
        pass

    @property
    def value(self) -> int:
        return self._value


# Test Exercise 3
counter = ThreadSafeCounter()


def increment_many(counter: ThreadSafeCounter, times: int) -> None:
    for _ in range(times):
        counter.increment()


threads = [Thread(target=increment_many, args=(counter, 1000)) for _ in range(10)]
for t in threads:
    t.start()
for t in threads:
    t.join()

assert counter.value == 10000, f"Expected 10000, got {counter.value}"
print("✓ Exercise 3 passed: Thread-safe counter")


# =============================================================================
# Exercise 4: Thread with Queue
# =============================================================================
# Implement a worker that processes items from a queue until it receives None.

def queue_worker(q: Queue, results: list) -> None:
    """Process items from queue, append doubled values to results.
    Stop when None is received."""
    # TODO: Loop getting items from queue
    # Double each item and append to results
    # Stop when you get None
    pass


# Test Exercise 4
q: Queue = Queue()
results = []

worker = Thread(target=queue_worker, args=(q, results))
worker.start()

for i in range(5):
    q.put(i)
q.put(None)  # Signal to stop

worker.join()

assert results == [0, 2, 4, 6, 8], f"Expected [0, 2, 4, 6, 8], got {results}"
print("✓ Exercise 4 passed: Thread with Queue")


# =============================================================================
# Exercise 5: Basic Asyncio Coroutine
# =============================================================================
# Implement an async function that simulates fetching data with a delay.

async def fetch_data(item_id: int, delay: float) -> dict:
    """Simulate fetching data: wait for delay seconds, return dict with id and data."""
    # TODO: await asyncio.sleep for the delay
    # Return {"id": item_id, "data": f"Data for {item_id}"}
    pass


# Test Exercise 5
async def test_fetch():
    start = time.perf_counter()
    result = await fetch_data(42, 0.1)
    elapsed = time.perf_counter() - start
    assert result == {"id": 42, "data": "Data for 42"}
    assert 0.09 < elapsed < 0.2, f"Should take ~0.1s, took {elapsed}"
    return True

assert asyncio.run(test_fetch())
print("✓ Exercise 5 passed: Basic async coroutine")


# =============================================================================
# Exercise 6: Concurrent Coroutines with gather
# =============================================================================
# Use asyncio.gather to run multiple fetch operations concurrently.

async def fetch_all(ids: list[int], delay: float) -> list[dict]:
    """Fetch data for all ids concurrently using asyncio.gather."""
    # TODO: Use asyncio.gather to run fetch_data for each id concurrently
    pass


# Test Exercise 6
async def test_fetch_all():
    start = time.perf_counter()
    results = await fetch_all([1, 2, 3, 4, 5], 0.1)
    elapsed = time.perf_counter() - start

    assert len(results) == 5
    assert results[0] == {"id": 1, "data": "Data for 1"}
    # All 5 should complete in ~0.1s (concurrent), not 0.5s (sequential)
    assert elapsed < 0.3, f"Should be concurrent (~0.1s), took {elapsed}"
    return True

assert asyncio.run(test_fetch_all())
print("✓ Exercise 6 passed: Concurrent coroutines with gather")


# =============================================================================
# Exercise 7: Asyncio Task Creation and Cancellation
# =============================================================================
# Implement a counter that can be cancelled.

async def counting_task(name: str, results: list) -> None:
    """Count from 1, appending to results every 0.05s until cancelled."""
    # TODO: Loop forever, incrementing a counter
    # Append (name, counter) to results
    # Handle CancelledError to exit gracefully
    pass


# Test Exercise 7
async def test_cancellation():
    results: list = []
    task = asyncio.create_task(counting_task("counter", results))

    await asyncio.sleep(0.15)  # Let it count a bit
    task.cancel()

    try:
        await task
    except asyncio.CancelledError:
        pass

    # Should have counted at least twice in 0.15s
    assert len(results) >= 2, f"Should have counted at least twice, got {len(results)}"
    assert results[0] == ("counter", 1)
    return True

assert asyncio.run(test_cancellation())
print("✓ Exercise 7 passed: Task cancellation")


# =============================================================================
# Exercise 8: Async Context Manager
# =============================================================================
# Implement an async context manager for timing async operations.

class AsyncTimer:
    def __init__(self):
        self.elapsed: float = 0.0

    async def __aenter__(self):
        # TODO: Record start time, return self
        pass

    async def __aexit__(self, exc_type, exc_value, traceback):
        # TODO: Calculate elapsed time
        pass


# Test Exercise 8
async def test_async_timer():
    async with AsyncTimer() as timer:
        await asyncio.sleep(0.1)

    assert 0.09 < timer.elapsed < 0.2, f"Should measure ~0.1s, got {timer.elapsed}"
    return True

assert asyncio.run(test_async_timer())
print("✓ Exercise 8 passed: Async context manager")


# =============================================================================
# Exercise 9: Asyncio Queue
# =============================================================================
# Implement producer-consumer pattern with asyncio.Queue.

async def async_producer(queue: asyncio.Queue, items: list) -> None:
    """Put items into queue with small delays, then put None to signal done."""
    # TODO: Put each item with a small delay, then put None
    pass


async def async_consumer(queue: asyncio.Queue) -> list:
    """Consume items from queue until None, return list of processed items."""
    # TODO: Get items, double them, collect until None
    pass


# Test Exercise 9
async def test_async_queue():
    queue: asyncio.Queue = asyncio.Queue()

    # Run producer and consumer concurrently
    producer_task = asyncio.create_task(async_producer(queue, [1, 2, 3, 4, 5]))
    results = await async_consumer(queue)
    await producer_task

    assert results == [2, 4, 6, 8, 10], f"Expected doubled values, got {results}"
    return True

assert asyncio.run(test_async_queue())
print("✓ Exercise 9 passed: Asyncio Queue")


# =============================================================================
# Exercise 10: Asyncio Timeout
# =============================================================================
# Implement a function that times out if operation takes too long.

async def fetch_with_timeout(item_id: int, delay: float, timeout: float) -> dict | None:
    """Fetch data but return None if it takes longer than timeout."""
    # TODO: Use asyncio.wait_for or asyncio.timeout
    # Return the result, or None on timeout
    pass


# Test Exercise 10
async def test_timeout():
    # Should succeed (delay < timeout)
    result = await fetch_with_timeout(1, 0.05, 0.2)
    assert result == {"id": 1, "data": "Data for 1"}

    # Should timeout (delay > timeout)
    result = await fetch_with_timeout(2, 0.3, 0.1)
    assert result is None, "Should return None on timeout"

    return True

assert asyncio.run(test_timeout())
print("✓ Exercise 10 passed: Asyncio timeout")


# =============================================================================
# Exercise 11: Combining Sync and Async
# =============================================================================
# Run a CPU-bound sync function in a thread pool from async code.

def cpu_intensive(n: int) -> int:
    """Simulate CPU-bound work: sum of squares."""
    total = 0
    for i in range(n):
        total += i * i
    return total


async def run_in_thread(func: Callable, *args) -> Any:
    """Run a sync function in a thread pool executor."""
    # TODO: Use asyncio.get_running_loop().run_in_executor()
    # Pass None as executor to use default thread pool
    pass


# Test Exercise 11
async def test_thread_executor():
    # Run CPU-bound work without blocking event loop
    result = await run_in_thread(cpu_intensive, 1000)
    expected = sum(i * i for i in range(1000))
    assert result == expected
    return True

assert asyncio.run(test_thread_executor())
print("✓ Exercise 11 passed: Run sync function in thread pool")


# =============================================================================
# Exercise 12: Simple Spinner with Threading
# =============================================================================
# Implement the classic spinner example from the chapter.

def spin_thread(msg: str, done: Event) -> None:
    """Display spinning animation until done is set."""
    # TODO: Cycle through r'\|/-' characters
    # Print with carriage return for animation
    # Check done.wait(0.1) to control frame rate
    # Clear the line when done
    pass


def slow_operation() -> int:
    """Simulate slow work."""
    time.sleep(0.3)
    return 42


def run_with_spinner() -> int:
    """Run slow_operation with a spinner."""
    # TODO: Create Event, start spin thread, run slow_operation
    # Signal done, join thread, return result
    pass


# Test Exercise 12
result = run_with_spinner()
assert result == 42
print("✓ Exercise 12 passed: Spinner with threading")


# =============================================================================
# Exercise 13: Simple Spinner with Asyncio
# =============================================================================
# Implement the spinner using asyncio.

async def spin_async(msg: str) -> None:
    """Display spinning animation until cancelled."""
    # TODO: Same animation logic but with await asyncio.sleep
    # Handle CancelledError to clean up
    pass


async def slow_async() -> int:
    """Simulate slow async work."""
    await asyncio.sleep(0.3)
    return 42


async def run_with_spinner_async() -> int:
    """Run slow_async with a spinner."""
    # TODO: Create task for spin_async, await slow_async
    # Cancel the spinner task, return result
    pass


# Test Exercise 13
result = asyncio.run(run_with_spinner_async())
assert result == 42
print("✓ Exercise 13 passed: Spinner with asyncio")


# =============================================================================
# Exercise 14: Async Semaphore for Rate Limiting
# =============================================================================
# Use a semaphore to limit concurrent operations.

async def rate_limited_fetch(
    ids: list[int],
    max_concurrent: int,
    delay: float = 0.05
) -> list[dict]:
    """Fetch data for all ids, but limit concurrent requests."""
    # TODO: Create asyncio.Semaphore(max_concurrent)
    # Create an inner async function that acquires semaphore before fetching
    # Use gather to run all fetches
    pass


# Test Exercise 14
async def test_rate_limiting():
    start = time.perf_counter()
    # 10 items, max 2 concurrent, 0.05s each
    # Should take ~0.25s (5 batches of 2)
    results = await rate_limited_fetch(list(range(10)), max_concurrent=2, delay=0.05)
    elapsed = time.perf_counter() - start

    assert len(results) == 10
    # With max 2 concurrent, should take > 0.2s
    assert elapsed > 0.2, f"Rate limiting not working, took {elapsed}"
    return True

assert asyncio.run(test_rate_limiting())
print("✓ Exercise 14 passed: Semaphore rate limiting")


# =============================================================================
# Exercise 15: Async Generator
# =============================================================================
# Implement an async generator that yields values with delays.

async def async_range(start: int, stop: int, delay: float):
    """Async generator yielding values from start to stop-1 with delays."""
    # TODO: Loop and yield values with await asyncio.sleep between
    pass


# Test Exercise 15
async def test_async_generator():
    results = []
    start_time = time.perf_counter()

    async for value in async_range(0, 5, 0.02):
        results.append(value)

    elapsed = time.perf_counter() - start_time

    assert results == [0, 1, 2, 3, 4]
    assert elapsed > 0.08, "Should have delays between yields"
    return True

assert asyncio.run(test_async_generator())
print("✓ Exercise 15 passed: Async generator")


# =============================================================================
print("\n" + "=" * 60)
print("Congratulations! All Chapter 18 exercises completed!")
print("=" * 60)
