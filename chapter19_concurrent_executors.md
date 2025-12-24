# Concurrent Executors - Practical Memo

## Overview

The `concurrent.futures` module provides a high-level interface for asynchronously executing callables using:
- **ThreadPoolExecutor** - for I/O-bound tasks
- **ProcessPoolExecutor** - for CPU-bound tasks

Key insight: "Spawning a bunch of independent threads and collecting the results in a queue is everything one needs to know." — Michele Simionato

---

## The Executor Interface

Both executor classes implement the same `Executor` interface:

```python
from concurrent import futures

# ThreadPoolExecutor for I/O-bound tasks
with futures.ThreadPoolExecutor(max_workers=5) as executor:
    results = executor.map(func, items)

# ProcessPoolExecutor for CPU-bound tasks
with futures.ProcessPoolExecutor(max_workers=4) as executor:
    results = executor.map(func, items)
```

### Key Methods

| Method | Description |
|--------|-------------|
| `executor.map(fn, *iterables)` | Apply fn to each item, return iterator of results (in order) |
| `executor.submit(fn, *args)` | Schedule fn with args, return a Future |
| `executor.shutdown(wait=True)` | Signal to free resources (called by `__exit__`) |

---

## Using executor.map

The simplest way to run tasks concurrently:

```python
from concurrent import futures

def download_one(url: str) -> bytes:
    """Download a single URL."""
    resp = httpx.get(url)
    return resp.content

def download_many(urls: list[str]) -> list[bytes]:
    with futures.ThreadPoolExecutor() as executor:
        # map returns results in the SAME ORDER as inputs
        results = executor.map(download_one, urls)
        return list(results)
```

**Key points:**
- Results are returned in the same order as inputs
- If any call raises an exception, it's raised when iterating results
- Blocks until all results are available (when converting to list)

---

## Understanding Futures

A `Future` represents a deferred computation that may or may not have completed.

### Future Lifecycle

```
Created → Pending → Running → Finished (with result or exception)
```

### Future Methods

| Method | Description |
|--------|-------------|
| `future.done()` | Returns `True` if completed (non-blocking) |
| `future.result(timeout=None)` | Get result (blocks if not done) |
| `future.exception(timeout=None)` | Get exception if raised |
| `future.add_done_callback(fn)` | Call fn(future) when done |
| `future.cancel()` | Attempt to cancel (may not succeed) |

### Creating Futures with submit()

```python
from concurrent import futures

def download_one(cc: str) -> str:
    # ... download logic ...
    return cc

with futures.ThreadPoolExecutor(max_workers=3) as executor:
    to_do: list[futures.Future] = []

    for cc in sorted(country_codes):
        future = executor.submit(download_one, cc)
        to_do.append(future)
        print(f'Scheduled: {future}')  # <Future state=pending>

    # Process results as they complete (not in submission order!)
    for future in futures.as_completed(to_do):
        result = future.result()  # Won't block - future is done
        print(f'Completed: {result}')
```

---

## map vs submit + as_completed

### executor.map

```python
# Results in ORDER of inputs
results = executor.map(func, items)
for result in results:
    process(result)
```

**Use when:** You need results in the same order as inputs.

### executor.submit + as_completed

```python
# Results in ORDER OF COMPLETION (fastest first)
futures_list = [executor.submit(func, item) for item in items]
for future in futures.as_completed(futures_list):
    result = future.result()
    process(result)
```

**Use when:** You want to process results as soon as they're available.

---

## ThreadPoolExecutor Details

### Default max_workers

Since Python 3.8:
```python
max_workers = min(32, os.cpu_count() + 4)
```

Rationale:
- At least 5 workers for I/O-bound tasks
- At most 32 cores for CPU-bound tasks
- Avoids excessive resource usage on many-core machines

### When to Use

- Network I/O (HTTP requests, database queries)
- File I/O (reading/writing files)
- Any task that spends time waiting

```python
# Great for I/O-bound tasks
with futures.ThreadPoolExecutor() as executor:
    results = executor.map(fetch_url, urls)
```

---

## ProcessPoolExecutor Details

### Default max_workers

```python
max_workers = os.cpu_count()  # Number of CPU cores
```

### When to Use

- CPU-intensive calculations
- Tasks that need to bypass the GIL
- Heavy data processing

```python
# Great for CPU-bound tasks
with futures.ProcessPoolExecutor() as executor:
    results = executor.map(is_prime, numbers)
```

### Caveats

- Higher startup cost than threads
- Arguments must be picklable (serializable)
- More memory usage (each process has own memory space)

---

## Practical Example: Multicore Prime Checker

```python
from concurrent import futures
from typing import NamedTuple

class PrimeResult(NamedTuple):
    n: int
    is_prime: bool
    elapsed: float

def check(n: int) -> PrimeResult:
    t0 = time.perf_counter()
    result = is_prime(n)
    return PrimeResult(n, result, time.perf_counter() - t0)

def main():
    numbers = [2, 142702110479723, 299593572317531, ...]

    with futures.ProcessPoolExecutor() as executor:
        for result in executor.map(check, numbers):
            label = 'P' if result.is_prime else ' '
            print(f'{result.n:16} {label} {result.elapsed:9.6f}s')
```

---

## Error Handling

### With executor.map

Exceptions are raised when iterating over results:

```python
def might_fail(x):
    if x == 3:
        raise ValueError("Bad value")
    return x * 2

with futures.ThreadPoolExecutor() as executor:
    results = executor.map(might_fail, [1, 2, 3, 4, 5])

    for result in results:  # Raises ValueError when reaching item 3
        print(result)
```

### With submit + as_completed

Check each future individually:

```python
with futures.ThreadPoolExecutor() as executor:
    future_to_item = {executor.submit(process, item): item
                      for item in items}

    for future in futures.as_completed(future_to_item):
        item = future_to_item[future]
        try:
            result = future.result()
        except Exception as e:
            print(f'{item} generated exception: {e}')
        else:
            print(f'{item} returned {result}')
```

---

## Progress Display Pattern

```python
from concurrent import futures
from tqdm import tqdm  # Progress bar library

def download_with_progress(urls: list[str]) -> list[bytes]:
    results = []

    with futures.ThreadPoolExecutor(max_workers=10) as executor:
        # Submit all tasks
        future_to_url = {executor.submit(fetch, url): url
                         for url in urls}

        # Process as completed with progress bar
        done_iter = futures.as_completed(future_to_url)
        for future in tqdm(done_iter, total=len(urls)):
            url = future_to_url[future]
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                print(f'Error fetching {url}: {e}')

    return results
```

---

## Executor.map Behavior Deep Dive

```python
from concurrent import futures
import time

def task(n):
    time.sleep(n)
    return n * 10

# With 3 workers and 5 tasks
with futures.ThreadPoolExecutor(max_workers=3) as executor:
    results = executor.map(task, [3, 2, 1, 4, 5])

    # Results come in ORDER OF SUBMISSION, not completion
    # Even though task(1) finishes first, we wait for task(3)
    for result in results:
        print(result)  # 30, 20, 10, 40, 50
```

**Important:** `executor.map` returns an iterator that yields results in submission order. If the first task takes longest, all results wait for it.

---

## Switching Between Thread and Process Executors

The uniform API makes switching easy:

```python
from concurrent import futures

def process_data(data):
    # Your processing logic
    return result

# I/O-bound: use threads
def run_threaded(items):
    with futures.ThreadPoolExecutor() as executor:
        return list(executor.map(process_data, items))

# CPU-bound: use processes
def run_parallel(items):
    with futures.ProcessPoolExecutor() as executor:
        return list(executor.map(process_data, items))
```

---

## Best Practices

### 1. Use Context Manager

```python
# GOOD - ensures cleanup
with futures.ThreadPoolExecutor() as executor:
    results = executor.map(func, items)

# BAD - must remember to shutdown
executor = futures.ThreadPoolExecutor()
results = executor.map(func, items)
executor.shutdown()
```

### 2. Choose the Right Executor

| Task Type | Executor | Why |
|-----------|----------|-----|
| Network I/O | ThreadPoolExecutor | GIL released during I/O |
| File I/O | ThreadPoolExecutor | GIL released during I/O |
| CPU-intensive | ProcessPoolExecutor | Bypasses GIL |
| Mixed | Depends on bottleneck | Profile first |

### 3. Set Appropriate max_workers

```python
# I/O-bound: can use many workers (100+)
with futures.ThreadPoolExecutor(max_workers=100) as executor:
    ...

# CPU-bound: use number of cores
with futures.ProcessPoolExecutor(max_workers=os.cpu_count()) as executor:
    ...
```

### 4. Handle Exceptions Properly

```python
# Always catch exceptions from futures
try:
    result = future.result()
except Exception as e:
    handle_error(e)
```

---

## Common Patterns

### Pattern 1: Map with Timeout

```python
with futures.ThreadPoolExecutor() as executor:
    results = executor.map(fetch, urls, timeout=30)
    try:
        for result in results:
            process(result)
    except futures.TimeoutError:
        print("Timed out waiting for results")
```

### Pattern 2: First Completed Result

```python
from concurrent.futures import FIRST_COMPLETED, wait

with futures.ThreadPoolExecutor() as executor:
    futures_set = {executor.submit(fetch, url) for url in urls}

    done, pending = wait(futures_set, return_when=FIRST_COMPLETED)

    first_result = done.pop().result()

    # Cancel remaining if not needed
    for future in pending:
        future.cancel()
```

### Pattern 3: Batch Processing

```python
def process_in_batches(items, batch_size=100):
    results = []

    with futures.ThreadPoolExecutor(max_workers=20) as executor:
        for i in range(0, len(items), batch_size):
            batch = items[i:i + batch_size]
            batch_results = list(executor.map(process, batch))
            results.extend(batch_results)

    return results
```

---

## Quick Reference

```python
from concurrent import futures

# ThreadPoolExecutor (I/O-bound)
with futures.ThreadPoolExecutor(max_workers=10) as executor:
    # Option 1: map (results in order)
    results = executor.map(func, items)

    # Option 2: submit + as_completed (results as ready)
    future_list = [executor.submit(func, item) for item in items]
    for future in futures.as_completed(future_list):
        result = future.result()

# ProcessPoolExecutor (CPU-bound)
with futures.ProcessPoolExecutor() as executor:
    results = executor.map(cpu_intensive_func, items)

# Future methods
future = executor.submit(func, arg)
future.done()           # Check if complete
future.result()         # Get result (blocks if not done)
future.result(timeout)  # Get result with timeout
future.exception()      # Get exception if raised
future.cancel()         # Attempt to cancel
future.add_done_callback(callback)  # Call when done
```

---

## Summary

1. **concurrent.futures** provides a simple, high-level API for concurrent execution
2. **ThreadPoolExecutor** is best for I/O-bound tasks (network, file I/O)
3. **ProcessPoolExecutor** is best for CPU-bound tasks (bypasses GIL)
4. **executor.map** returns results in submission order
5. **executor.submit + as_completed** yields results in completion order
6. **Futures** represent pending computations with result/exception access
7. Always use context managers for proper resource cleanup
8. Error handling requires explicit try/except around `future.result()`
