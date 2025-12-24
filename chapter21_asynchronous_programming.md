# Asynchronous Programming - Practical Memo

## Overview

Asynchronous programming with `asyncio` enables concurrent I/O operations in a single thread. Key constructs: `async def`, `await`, `async with`, and `async for`.

> "You rewrite all your code so none of it blocks or you're just wasting your time."
> — Alvaro Videla and Jason J. W. Williams, RabbitMQ in Action

---

## Coroutine Types

| Type | Definition | Notes |
|------|------------|-------|
| **Native coroutine** | Defined with `async def` | Use `await` to delegate; cannot use `yield from` |
| **Classic coroutine** | Generator using `.send()` | Deprecated for asyncio |
| **Asynchronous generator** | `async def` with `yield` | Returns `AsyncIterator`, driven by `async for` |

---

## Basic asyncio Pattern

```python
import asyncio

async def fetch_data(url: str) -> str:
    """A native coroutine."""
    await asyncio.sleep(1)  # Simulate I/O
    return f"Data from {url}"

async def main() -> None:
    result = await fetch_data("example.com")
    print(result)

# Entry point - drives the event loop
asyncio.run(main())
```

**Guido's Trick**: Squint and pretend `async` and `await` aren't there. Coroutines read like sequential functions that magically never block.

---

## Awaitables

Objects that work with `await`:

1. **Native coroutine objects** - from calling `async def` functions
2. **asyncio.Task** - from `asyncio.create_task()`
3. **asyncio.Future** - low-level, implements `__await__`

```python
# Coroutine object (awaitable)
coro = fetch_data("example.com")
result = await coro

# Task - scheduled for concurrent execution
task = asyncio.create_task(fetch_data("example.com"))
result = await task
```

---

## Running Multiple Coroutines

### asyncio.gather - Wait for All

```python
async def main():
    # Run concurrently, get results in submission order
    results = await asyncio.gather(
        fetch_data("url1"),
        fetch_data("url2"),
        fetch_data("url3"),
    )
    # results is a list in the same order as arguments
```

### asyncio.as_completed - Process as Done

```python
async def main():
    coros = [fetch_data(url) for url in urls]

    # Yields coroutines as they complete (not submission order)
    for coro in asyncio.as_completed(coros):
        result = await coro
        print(result)
```

### asyncio.create_task - Fire and Forget

```python
async def main():
    # Schedule for concurrent execution
    task1 = asyncio.create_task(fetch_data("url1"))
    task2 = asyncio.create_task(fetch_data("url2"))

    # Do other work...

    # Collect results when needed
    result1 = await task1
    result2 = await task2
```

---

## Asynchronous Context Managers

Objects implementing `__aenter__` and `__aexit__` as coroutines:

```python
import httpx

async def download(url: str) -> bytes:
    async with httpx.AsyncClient() as client:  # async context manager
        response = await client.get(url)
        return response.content
```

### Creating with @asynccontextmanager

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def open_db():
    conn = await create_connection()
    try:
        yield conn  # Value available after 'as'
    finally:
        await conn.close()

# Usage
async with open_db() as conn:
    await conn.execute("SELECT 1")
```

---

## Asynchronous Iteration

### async for

```python
async def main():
    async for row in fetch_rows():  # async for with async iterator
        print(row)
```

### Asynchronous Generators

```python
async def fetch_pages(urls: list[str]) -> AsyncIterator[str]:
    """Asynchronous generator function."""
    for url in urls:
        data = await fetch(url)
        yield data  # Makes this an async generator

# Driven by async for
async for page in fetch_pages(urls):
    process(page)
```

### Async Comprehensions

```python
# Async list comprehension
results = [await fetch(url) async for url in async_url_generator()]

# Async generator expression
gen = (await fetch(url) async for url in async_url_generator())
```

---

## Throttling with Semaphores

Control concurrent operations:

```python
async def download_one(url: str, semaphore: asyncio.Semaphore) -> bytes:
    async with semaphore:  # Blocks if counter is 0
        return await fetch(url)

async def download_many(urls: list[str], max_concurrent: int = 10):
    semaphore = asyncio.Semaphore(max_concurrent)
    tasks = [download_one(url, semaphore) for url in urls]
    return await asyncio.gather(*tasks)
```

**How it works:**
- Semaphore has an internal counter (initialized to `max_concurrent`)
- `acquire()` decrements counter; blocks if counter is 0
- `release()` increments counter
- `async with semaphore:` handles acquire/release automatically

---

## Delegating to Executors

Run blocking code without freezing the event loop:

### asyncio.to_thread (Python 3.9+)

```python
async def save_file(data: bytes, path: str):
    # Run blocking I/O in thread pool
    await asyncio.to_thread(write_file, data, path)
```

### loop.run_in_executor (Python 3.7+)

```python
async def save_file(data: bytes, path: str):
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, write_file, data, path)
    # None = use default ThreadPoolExecutor
```

### ProcessPoolExecutor for CPU-bound Tasks

```python
from concurrent.futures import ProcessPoolExecutor

async def compute_heavy(data):
    loop = asyncio.get_running_loop()
    with ProcessPoolExecutor() as pool:
        result = await loop.run_in_executor(pool, cpu_intensive_func, data)
    return result
```

---

## HTTP Client with HTTPX

```python
import httpx

async def fetch_flags(codes: list[str]) -> list[bytes]:
    async with httpx.AsyncClient() as client:
        tasks = [fetch_one(client, code) for code in codes]
        return await asyncio.gather(*tasks)

async def fetch_one(client: httpx.AsyncClient, code: str) -> bytes:
    url = f"https://example.com/flags/{code}.gif"
    resp = await client.get(url, timeout=6.1, follow_redirects=True)
    resp.raise_for_status()
    return resp.content
```

---

## TCP Server with asyncio

```python
import asyncio

async def handle_client(
    reader: asyncio.StreamReader,
    writer: asyncio.StreamWriter
) -> None:
    addr = writer.get_extra_info('peername')
    print(f"Connected: {addr}")

    while True:
        data = await reader.readline()
        if not data:
            break

        message = data.decode().strip()
        response = f"Echo: {message}\n"
        writer.write(response.encode())
        await writer.drain()

    writer.close()
    await writer.wait_closed()

async def main():
    server = await asyncio.start_server(
        handle_client, '127.0.0.1', 8888
    )
    async with server:
        await server.serve_forever()

asyncio.run(main())
```

**Key points:**
- `writer.write()` is a regular function (writes to buffer)
- `writer.drain()` is a coroutine (flushes buffer to network)
- `reader.readline()` is a coroutine (waits for data)

---

## The async Console

```bash
$ python -m asyncio
```

Allows `await`, `async for`, `async with` at the top level:

```python
>>> await asyncio.sleep(1, "Hello!")
'Hello!'
>>> async for x in async_generator():
...     print(x)
```

---

## Error Handling

```python
async def fetch_with_retry(url: str, retries: int = 3) -> str:
    for attempt in range(retries):
        try:
            return await fetch(url)
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                raise  # Don't retry 404
            if attempt == retries - 1:
                raise
            await asyncio.sleep(2 ** attempt)  # Exponential backoff
```

---

## Common Patterns

### Pattern 1: Timeout

```python
async def fetch_with_timeout(url: str, timeout: float = 5.0):
    try:
        return await asyncio.wait_for(fetch(url), timeout=timeout)
    except asyncio.TimeoutError:
        return None
```

### Pattern 2: First Completed

```python
async def race(coros):
    """Return result of first completed coroutine."""
    done, pending = await asyncio.wait(
        coros,
        return_when=asyncio.FIRST_COMPLETED
    )

    # Cancel remaining
    for task in pending:
        task.cancel()

    return done.pop().result()
```

### Pattern 3: Background Task

```python
async def main():
    # Start background task
    spinner = asyncio.create_task(spin())

    # Do main work
    result = await slow_operation()

    # Clean up
    spinner.cancel()
    return result
```

---

## Key Differences: Native Coroutines vs Async Generators

| Aspect | Native Coroutine | Async Generator |
|--------|-----------------|-----------------|
| Declaration | `async def` (no yield) | `async def` with `yield` |
| Returns | Any value | Only empty `return` |
| Awaitable | Yes | No |
| Driven by | `await`, `gather`, `create_task` | `async for` |
| Type hint | `Coroutine[...]` | `AsyncIterator[...]` |

---

## Best Practices

### 1. Use async with for Resources

```python
# GOOD
async with httpx.AsyncClient() as client:
    response = await client.get(url)

# BAD - may leak connections
client = httpx.AsyncClient()
response = await client.get(url)
```

### 2. Don't Block the Event Loop

```python
# BAD - blocks everything
def blocking_io():
    time.sleep(1)

# GOOD - run in executor
await asyncio.to_thread(blocking_io)
```

### 3. Limit Concurrency

```python
# BAD - may overwhelm server
tasks = [fetch(url) for url in thousands_of_urls]
await asyncio.gather(*tasks)

# GOOD - use semaphore
semaphore = asyncio.Semaphore(50)
tasks = [fetch_with_semaphore(url, semaphore) for url in urls]
await asyncio.gather(*tasks)
```

### 4. Handle Cancellation

```python
async def cancellable_operation():
    try:
        await long_running_task()
    except asyncio.CancelledError:
        # Cleanup
        await cleanup()
        raise  # Re-raise to propagate cancellation
```

---

## Quick Reference

```python
import asyncio

# Run event loop
asyncio.run(main())

# Get running loop (from inside coroutine)
loop = asyncio.get_running_loop()

# Sleep
await asyncio.sleep(seconds)

# Run concurrently, collect all results
results = await asyncio.gather(coro1, coro2, coro3)

# Process as completed
for coro in asyncio.as_completed(coros):
    result = await coro

# Create task (schedule for background execution)
task = asyncio.create_task(coro)

# Wait with timeout
result = await asyncio.wait_for(coro, timeout=5.0)

# Wait for first/all
done, pending = await asyncio.wait(tasks, return_when=FIRST_COMPLETED)

# Run blocking code in thread
await asyncio.to_thread(blocking_func, arg1, arg2)

# Semaphore for throttling
semaphore = asyncio.Semaphore(10)
async with semaphore:
    await limited_operation()

# TCP server
server = await asyncio.start_server(handler, host, port)
await server.serve_forever()
```

---

## Summary

1. **Native coroutines** (`async def` without `yield`) are the building blocks
2. **await** suspends coroutine until awaitable completes
3. **asyncio.run()** is the main entry point to start the event loop
4. **asyncio.gather()** runs coroutines concurrently, returns results in order
5. **asyncio.as_completed()** yields results as they finish
6. **async with** for asynchronous context managers
7. **async for** for asynchronous iteration
8. **Semaphores** throttle concurrent operations
9. **Executors** run blocking code without freezing the loop
10. All-or-nothing: rewrite I/O code as coroutines, or delegate to executors
