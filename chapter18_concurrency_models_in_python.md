# Concurrency Models in Python - Practical Memo

## Overview

This chapter introduces Python's three native approaches to concurrency:
- **Threads** - via the `threading` module
- **Processes** - via the `multiprocessing` module
- **Coroutines** - via `asyncio` with `async`/`await`

Key insight from Rob Pike: "Concurrency is about dealing with lots of things at once. Parallelism is about doing lots of things at once."

---

## Core Concepts

### Concurrency vs Parallelism

| Concept | Definition | Example |
|---------|------------|---------|
| **Concurrency** | Handling multiple pending tasks, making progress one at a time or in parallel | A single-core CPU running 100 processes via OS scheduling |
| **Parallelism** | Executing multiple computations simultaneously | A 4-core CPU running 4 tasks at the exact same time |

**Key insight:** All parallel systems are concurrent, but not all concurrent systems are parallel.

### Execution Units in Python

| Unit | Description | Communication | Cost |
|------|-------------|---------------|------|
| **Process** | Isolated instance with own memory space | Pipes, sockets, shared memory (must serialize objects) | High |
| **Thread** | Execution unit within a process, shares memory | Shared objects (risk of data corruption) | Medium |
| **Coroutine** | Function that can suspend/resume | Shared objects (single thread, no race conditions) | Low |

---

## Python's Global Interpreter Lock (GIL)

### What is the GIL?

The GIL is a lock that allows only one Python thread to execute Python bytecode at any time.

### Key Facts About the GIL

1. **Only one thread executes Python code at a time** - regardless of CPU cores
2. **GIL is released every ~5ms** - allowing other threads to run
3. **I/O operations release the GIL** - all syscalls (disk, network, `time.sleep()`)
4. **C extensions can release the GIL** - NumPy, zlib, bz2 do this for CPU-intensive work
5. **Threads are great for I/O-bound tasks** - network latency dominates, GIL impact is minimal

### Implications

```python
# CPU-bound: threads DON'T help (GIL blocks parallelism)
# Use multiprocessing instead

# I/O-bound: threads DO help (GIL is released during I/O)
# Threads or asyncio are good choices
```

### Quote to Remember

> "Python threads are great at doing nothing." — David Beazley

(Because I/O-bound threads spend most of their time waiting, and the GIL is released during that wait.)

---

## The Three Spinner Examples

### Common Pattern

All three examples animate a spinner while a "slow" computation runs:
1. Start a spinner in a separate execution unit
2. Run a slow operation (simulated with sleep)
3. Signal the spinner to stop
4. Display the result

### 1. Threading Version

```python
import itertools
import time
from threading import Thread, Event

def spin(msg: str, done: Event) -> None:
    for char in itertools.cycle(r'\|/-'):
        status = f'\r{char} {msg}'
        print(status, end='', flush=True)
        if done.wait(.1):  # Timeout acts as frame rate
            break
    blanks = ' ' * len(status)
    print(f'\r{blanks}\r', end='')

def slow() -> int:
    time.sleep(3)  # Blocks this thread, but GIL is released
    return 42

def supervisor() -> int:
    done = Event()  # Signaling mechanism
    spinner = Thread(target=spin, args=('thinking!', done))
    spinner.start()
    result = slow()
    done.set()  # Signal spinner to stop
    spinner.join()  # Wait for spinner thread to finish
    return result
```

**Key points:**
- `threading.Event` is the simplest signaling mechanism
- `Event.wait(timeout)` returns `True` when set, `False` on timeout
- No API to terminate threads - must send a message (Event, Queue, etc.)
- `time.sleep()` releases the GIL

### 2. Multiprocessing Version

```python
from multiprocessing import Process, Event
from multiprocessing import synchronize

def spin(msg: str, done: synchronize.Event) -> None:
    # Same as threading version
    ...

def supervisor() -> int:
    done = Event()  # multiprocessing.Event (a function, not a class!)
    spinner = Process(target=spin, args=('thinking!', done))
    spinner.start()
    result = slow()
    done.set()
    spinner.join()
    return result
```

**Key differences from threading:**
- Uses `Process` instead of `Thread`
- Each process has its own Python interpreter and GIL
- Can use all CPU cores for CPU-bound work
- Objects crossing process boundaries must be serialized (overhead!)
- `multiprocessing.Event` is a function returning `synchronize.Event`

### 3. Asyncio/Coroutine Version

```python
import asyncio
import itertools

async def spin(msg: str) -> None:
    for char in itertools.cycle(r'\|/-'):
        status = f'\r{char} {msg}'
        print(status, flush=True, end='')
        try:
            await asyncio.sleep(.1)  # Yields control to event loop
        except asyncio.CancelledError:
            break
    blanks = ' ' * len(status)
    print(f'\r{blanks}\r', end='')

async def slow() -> int:
    await asyncio.sleep(3)  # Yields control, doesn't block
    return 42

async def supervisor() -> int:
    spinner = asyncio.create_task(spin('thinking!'))  # Schedule coroutine
    result = await slow()  # Suspend until slow completes
    spinner.cancel()  # Raises CancelledError in spin
    return result

def main() -> None:
    result = asyncio.run(supervisor())  # Entry point
    print(f'Answer: {result}')
```

**Key concepts:**
- No `Event` needed - use `Task.cancel()` instead
- `asyncio.CancelledError` for graceful shutdown
- Everything runs in one thread (no GIL issues between coroutines)

---

## Three Ways to Run Coroutines

| Method | Use Case | Returns |
|--------|----------|---------|
| `asyncio.run(coro())` | Entry point from sync code | Return value of coro |
| `asyncio.create_task(coro())` | Schedule from within async code | `Task` object |
| `await coro()` | Call from within async code | Return value of coro |

**Important:** `coro()` returns a coroutine object immediately. The body only runs when driven by the event loop.

---

## Critical Mistake: Blocking the Event Loop

```python
# WRONG - blocks the entire event loop!
async def slow() -> int:
    time.sleep(3)  # Blocking call - freezes everything
    return 42

# CORRECT - yields control during sleep
async def slow() -> int:
    await asyncio.sleep(3)  # Non-blocking
    return 42
```

**Rule:** Never use `time.sleep()` in asyncio coroutines. Use `await asyncio.sleep()`.

---

## Comparison Summary

| Aspect | Threading | Multiprocessing | Asyncio |
|--------|-----------|-----------------|---------|
| **GIL impact** | Limited to 1 Python thread at a time | Each process has own GIL | N/A (single thread) |
| **Best for** | I/O-bound tasks | CPU-bound tasks | I/O-bound with many connections |
| **Startup cost** | Medium | High | Very low |
| **Memory** | Shared (risk of corruption) | Isolated (serialization needed) | Shared (no races in single thread) |
| **Cancellation** | Manual signaling | Manual signaling | Built-in (`Task.cancel()`) |
| **Preemption** | Preemptive (OS scheduler) | Preemptive (OS scheduler) | Cooperative (`await` points) |

---

## Multitasking Types

### Preemptive Multitasking (Threads & Processes)

- OS scheduler can suspend execution at any time
- A frozen thread/process won't freeze the system
- Risk of race conditions

### Cooperative Multitasking (Coroutines)

- Coroutines explicitly yield control with `await`
- Blocking code freezes the entire event loop
- No race conditions (execution points are predictable)

---

## Data Structures for Concurrency

### Queues

| Module | Class | Use Case |
|--------|-------|----------|
| `queue` | `Queue`, `LifoQueue`, `PriorityQueue` | Thread communication |
| `multiprocessing` | `Queue` | Process communication |
| `asyncio` | `Queue`, `LifoQueue`, `PriorityQueue` | Coroutine communication |

### Locks

- **Mutex (mutual exclusion)**: Ensures only one execution unit accesses shared data
- Implementation varies by module: `threading.Lock`, `multiprocessing.Lock`, `asyncio.Lock`

---

## When to Use What

```
Task is I/O-bound?
├── Yes → Many concurrent connections?
│         ├── Yes → asyncio (scales to thousands)
│         └── No → threading (simpler for few connections)
└── No (CPU-bound) → multiprocessing (bypasses GIL)
```

### Guidelines

1. **Start simple** - sometimes sequential is fast enough
2. **Profile first** - identify the actual bottleneck
3. **I/O-bound → threads or asyncio** - GIL is released during I/O
4. **CPU-bound → multiprocessing** - true parallelism across cores
5. **High concurrency (1000s of connections) → asyncio** - lower overhead per connection

---

## Best Practices

### Threading

1. Use `Event` or `Queue` for communication
2. Don't share mutable state without locks
3. Keep critical sections (locked code) short

### Multiprocessing

1. Minimize data passed between processes (serialization cost)
2. Use `multiprocessing.shared_memory` for large data
3. Consider `ProcessPoolExecutor` for simpler API

### Asyncio

1. Never use blocking calls (`time.sleep`, sync I/O)
2. Use `await asyncio.sleep()` for delays
3. Handle `CancelledError` for graceful shutdown
4. Use `asyncio.create_task()` to run coroutines concurrently

---

## Quick Reference

```python
# Threading
from threading import Thread, Event
thread = Thread(target=func, args=(arg,))
thread.start()
thread.join()

# Multiprocessing
from multiprocessing import Process
process = Process(target=func, args=(arg,))
process.start()
process.join()

# Asyncio
import asyncio

async def main():
    task = asyncio.create_task(coro())
    result = await other_coro()
    task.cancel()

asyncio.run(main())
```

---

## Summary

1. **Concurrency** is about structure; **parallelism** is about execution
2. **GIL** limits Python threads to one at a time for Python code
3. **Threads** work well for I/O-bound tasks (GIL released during I/O)
4. **Processes** bypass the GIL for CPU-bound parallelism
5. **Coroutines** are lightweight and ideal for high-concurrency I/O
6. **Never block the event loop** in asyncio - use `await` for all waiting
7. Choose based on workload: I/O-bound → threads/asyncio, CPU-bound → multiprocessing
