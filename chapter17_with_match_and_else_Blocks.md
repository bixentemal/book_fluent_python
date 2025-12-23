# with, match, and else Blocks - Practical Memo

## Overview

This chapter covers three control flow features that are underused in Python:
- The `with` statement and context managers
- Pattern matching with `match/case`
- The `else` clause in `for`, `while`, and `try` statements

---

## Context Managers and the `with` Statement

### What Is a Context Manager?

A context manager is an object that defines `__enter__` and `__exit__` methods to set up and tear down a context for a block of code.

```python
# The most common example: file handling
with open('data.txt') as f:
    content = f.read()
# File is automatically closed here, even if an exception occurred
```

### How `with` Works

```python
with EXPRESSION as TARGET:
    BODY
```

1. `EXPRESSION` is evaluated to get a context manager object
2. `__enter__()` is called on that object
3. The return value of `__enter__()` is bound to `TARGET` (if `as` is used)
4. `BODY` executes
5. `__exit__()` is called, even if `BODY` raised an exception

**Important:** The `TARGET` is the return value of `__enter__()`, NOT the context manager itself!

### Implementing a Context Manager Class

```python
class LookingGlass:
    """Context manager that reverses stdout."""

    def __enter__(self):
        import sys
        self.original_write = sys.stdout.write
        sys.stdout.write = self._reverse_write
        return 'JABBERWOCKY'  # This is what gets bound to TARGET

    def _reverse_write(self, text):
        self.original_write(text[::-1])

    def __exit__(self, exc_type, exc_value, traceback):
        import sys
        sys.stdout.write = self.original_write
        # Handle specific exceptions if needed
        if exc_type is ZeroDivisionError:
            print('Please DO NOT divide by zero!')
            return True  # Suppress the exception
        # Return None/False to propagate exceptions
```

### The `__exit__` Method

```python
def __exit__(self, exc_type, exc_value, traceback):
    # exc_type: Exception class (e.g., ValueError)
    # exc_value: Exception instance
    # traceback: Traceback object

    # If no exception: all three are None
    # Return True to suppress exception
    # Return None/False to propagate exception
```

---

## The @contextmanager Decorator

### Simpler Context Managers with Generators

Instead of a class, use a generator function with `@contextmanager`:

```python
import contextlib
import sys

@contextlib.contextmanager
def looking_glass():
    original_write = sys.stdout.write

    def reverse_write(text):
        original_write(text[::-1])

    sys.stdout.write = reverse_write
    yield 'JABBERWOCKY'  # Value for TARGET
    sys.stdout.write = original_write  # Cleanup
```

### How It Works

1. Everything **before** `yield` runs when entering the `with` block (`__enter__`)
2. The `yield` value is bound to the `as` target
3. Everything **after** `yield` runs when exiting (`__exit__`)

### Exception Handling with @contextmanager

```python
@contextlib.contextmanager
def managed_resource():
    resource = acquire_resource()
    try:
        yield resource
    except SomeException:
        handle_exception()
    finally:
        release_resource()  # Always runs
```

**Key point:** Use `try/finally` around `yield` to ensure cleanup happens!

---

## Useful contextlib Utilities

| Utility | Purpose |
|---------|---------|
| `@contextmanager` | Create context manager from generator |
| `closing(obj)` | Call `obj.close()` on exit |
| `suppress(*exceptions)` | Ignore specified exceptions |
| `redirect_stdout(file)` | Redirect stdout to a file |
| `redirect_stderr(file)` | Redirect stderr to a file |
| `nullcontext(value)` | Do-nothing context manager |
| `ExitStack` | Manage variable number of context managers |

### Examples

```python
from contextlib import closing, suppress, redirect_stdout

# closing - auto-close objects without __exit__
with closing(urlopen('http://example.com')) as page:
    content = page.read()

# suppress - ignore specific exceptions
with suppress(FileNotFoundError):
    os.remove('file.txt')

# redirect_stdout - capture output
from io import StringIO
buffer = StringIO()
with redirect_stdout(buffer):
    print("This goes to buffer")
output = buffer.getvalue()

# ExitStack - dynamic number of context managers
from contextlib import ExitStack
with ExitStack() as stack:
    files = [stack.enter_context(open(f)) for f in filenames]
    # All files will be closed on exit
```

### Parenthesized Context Managers (Python 3.10+)

```python
# Multiple context managers with nice formatting
with (
    open('input.txt') as infile,
    open('output.txt', 'w') as outfile,
):
    outfile.write(infile.read())
```

---

## Pattern Matching with match/case

### Basic Syntax

```python
match subject:
    case pattern1:
        action1
    case pattern2:
        action2
    case _:
        default_action
```

### Pattern Types

```python
# Literal patterns
case 0:
case "hello":
case True:

# Capture patterns (bind to variable)
case x:  # Matches anything, binds to x
case [x, y]:  # Matches 2-element list

# Class patterns
case int(x):  # Match int, bind to x
case Point(x=0, y=y):  # Match Point with x=0

# Sequence patterns
case []:  # Empty list
case [first, *rest]:  # First element + rest
case [_, _, third]:  # Third element only

# Mapping patterns
case {"name": name, "age": age}:

# OR patterns
case "yes" | "y" | "Y":
case int(x) | float(x):

# Guards
case x if x > 0:
case [a, b] if a < b:
```

### Practical Example: Command Parser

```python
def handle_command(command):
    match command.split():
        case ["quit"]:
            return "Goodbye!"
        case ["hello", name]:
            return f"Hello, {name}!"
        case ["add", *numbers]:
            return sum(int(n) for n in numbers)
        case ["load", filename] if filename.endswith('.json'):
            return load_json(filename)
        case _:
            return "Unknown command"
```

### Evaluator Pattern (from lis.py interpreter)

```python
def evaluate(exp, env):
    match exp:
        # Numbers evaluate to themselves
        case int(x) | float(x):
            return x

        # Symbols are looked up in environment
        case str(var):
            return env[var]

        # Quote returns expression unevaluated
        case ['quote', x]:
            return x

        # If expression
        case ['if', test, consequence, alternative]:
            if evaluate(test, env):
                return evaluate(consequence, env)
            else:
                return evaluate(alternative, env)

        # Function call
        case [func_exp, *args]:
            proc = evaluate(func_exp, env)
            values = [evaluate(arg, env) for arg in args]
            return proc(*values)

        case _:
            raise SyntaxError(f"Unknown expression: {exp}")
```

---

## The else Clause Beyond if

### for/else

The `else` block runs only if the loop completes **without** `break`:

```python
# Common pattern: searching for an item
for item in items:
    if item.matches(criteria):
        result = item
        break
else:
    # No match found - loop completed without break
    raise ValueError("No matching item found")
```

**Think of it as:** "for...else (if no break)"

### while/else

Same rule: `else` runs only if loop exits normally (condition became falsy):

```python
while stack:
    item = stack.pop()
    if item.is_target():
        result = item
        break
else:
    # Stack exhausted without finding target
    result = None
```

### try/else

The `else` runs only if **no exception** was raised in `try`:

```python
try:
    result = dangerous_operation()
except SomeError:
    handle_error()
else:
    # Only runs if no exception
    process_result(result)
finally:
    # Always runs
    cleanup()
```

**Why use else?** Keep only potentially dangerous code in `try`:

```python
# BAD: after_call() errors are caught too
try:
    dangerous_call()
    after_call()
except OSError:
    log('OSError...')

# GOOD: Only dangerous_call() errors are caught
try:
    dangerous_call()
except OSError:
    log('OSError...')
else:
    after_call()  # Won't catch errors from here
```

---

## EAFP vs LBYL

### EAFP: Easier to Ask Forgiveness than Permission

```python
# Pythonic style: just try it
try:
    value = my_dict[key]
except KeyError:
    value = default
```

### LBYL: Look Before You Leap

```python
# Less Pythonic, but sometimes appropriate
if key in my_dict:
    value = my_dict[key]
else:
    value = default
```

**EAFP is preferred in Python because:**
- Often faster when exception is rare
- Thread-safe (no race condition between check and action)
- More concise with `try/else`

---

## Best Practices

### Context Managers

1. **Use `with` for resource management** - files, locks, connections
2. **Prefer `@contextmanager`** for simple cases
3. **Use `try/finally` around `yield`** in `@contextmanager`
4. **Return `True` from `__exit__`** only to suppress exceptions intentionally

### Pattern Matching

1. **Order matters** - more specific patterns first
2. **Use guards** for conditions that can't be expressed in patterns
3. **Use `_`** for the catch-all case
4. **Capture with `as`** when needed: `case [*items] as full_list:`

### else Clauses

1. **for/else** - "else if no break"
2. **while/else** - "else if no break"
3. **try/else** - "else if no exception"
4. **Keep try blocks minimal** - only code that might raise the expected exception

---

## Quick Reference

```python
# Context manager class
class MyContext:
    def __enter__(self):
        # Setup
        return value_for_as_clause

    def __exit__(self, exc_type, exc_value, traceback):
        # Cleanup
        return True  # to suppress exception

# Context manager with decorator
from contextlib import contextmanager

@contextmanager
def my_context():
    # Setup
    try:
        yield value_for_as_clause
    finally:
        # Cleanup

# Pattern matching
match value:
    case Pattern(capture) if guard:
        action

# for/else
for item in items:
    if found(item):
        break
else:
    not_found()

# try/else
try:
    risky()
except Error:
    handle()
else:
    success()
```

---

## Summary

1. **Context managers** automate setup/teardown with `__enter__`/`__exit__`
2. **@contextmanager** creates context managers from generators with `yield`
3. **match/case** provides powerful pattern matching for sequence, mapping, and class patterns
4. **for/else and while/else** run `else` only if loop completes without `break`
5. **try/else** runs `else` only if no exception was raised
6. **EAFP** style uses `try/except` for control flow - idiomatic Python
