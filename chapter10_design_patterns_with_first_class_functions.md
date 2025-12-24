# Design Patterns with First-Class Functions - Practical Memo

## Core Insight

Many classic design patterns exist to work around limitations in languages without first-class functions. In Python, patterns like **Strategy** and **Command** can often be simplified by using functions instead of classes.

> "16 of 23 patterns have qualitatively simpler implementation in Lisp or Dylan than in C++ for at least some uses of each pattern"
> — Peter Norvig, "Design Patterns in Dynamic Languages"

---

## The Strategy Pattern

### The Problem

Define a family of algorithms, encapsulate each one, and make them interchangeable.

**Classic Example:** Discount strategies for an e-commerce order:
- Fidelity discount: 5% for customers with 1000+ points
- Bulk discount: 10% for line items with 20+ units
- Large order discount: 7% for orders with 10+ distinct items

### Classic OOP Approach (Verbose)

```python
from abc import ABC, abstractmethod
from decimal import Decimal

class Promotion(ABC):  # Strategy interface
    @abstractmethod
    def discount(self, order: 'Order') -> Decimal:
        """Return discount as a positive dollar amount"""

class FidelityPromo(Promotion):  # Concrete Strategy
    """5% discount for customers with 1000+ fidelity points"""
    def discount(self, order: 'Order') -> Decimal:
        if order.customer.fidelity >= 1000:
            return order.total() * Decimal('0.05')
        return Decimal(0)

class BulkItemPromo(Promotion):  # Another Concrete Strategy
    """10% discount for line items with 20+ units"""
    def discount(self, order: 'Order') -> Decimal:
        discount = Decimal(0)
        for item in order.cart:
            if item.quantity >= 20:
                discount += item.total() * Decimal('0.1')
        return discount

# Usage
order = Order(customer, cart, FidelityPromo())  # Must instantiate!
```

**Problems with this approach:**
- Each strategy is a class with a single method
- Strategy instances have no state
- Boilerplate code (ABC, class definitions)
- Must instantiate strategy objects

### Function-Oriented Approach (Pythonic)

```python
from decimal import Decimal
from typing import Callable, Optional

# Type alias for promotion functions
Promotion = Callable[['Order'], Decimal]

class Order:
    def __init__(self, customer, cart, promotion: Optional[Promotion] = None):
        self.customer = customer
        self.cart = cart
        self.promotion = promotion

    def due(self) -> Decimal:
        if self.promotion is None:
            discount = Decimal(0)
        else:
            discount = self.promotion(self)  # Just call the function!
        return self.total() - discount

# Strategies are just functions
def fidelity_promo(order: Order) -> Decimal:
    """5% discount for customers with 1000+ fidelity points"""
    if order.customer.fidelity >= 1000:
        return order.total() * Decimal('0.05')
    return Decimal(0)

def bulk_item_promo(order: Order) -> Decimal:
    """10% discount for line items with 20+ units"""
    discount = Decimal(0)
    for item in order.cart:
        if item.quantity >= 20:
            discount += item.total() * Decimal('0.1')
    return discount

def large_order_promo(order: Order) -> Decimal:
    """7% discount for orders with 10+ distinct items"""
    distinct_items = {item.product for item in order.cart}
    if len(distinct_items) >= 10:
        return order.total() * Decimal('0.07')
    return Decimal(0)

# Usage - just pass the function!
order = Order(customer, cart, fidelity_promo)
```

**Advantages:**
- Less code, more readable
- No need to instantiate strategy objects
- Functions are naturally "flyweight" (shared, stateless)
- Easy to test in isolation

---

## Choosing the Best Strategy

### Simple Approach: List of Functions

```python
promos = [fidelity_promo, bulk_item_promo, large_order_promo]

def best_promo(order: Order) -> Decimal:
    """Compute the best discount available"""
    return max(promo(order) for promo in promos)

# Usage
order = Order(customer, cart, best_promo)
```

**Problem:** Must remember to add new promos to the list manually.

### Module Introspection Approach

```python
# All promo functions in a separate module: promotions.py
import inspect
import promotions

promos = [func for _, func in
          inspect.getmembers(promotions, inspect.isfunction)]

def best_promo(order: Order) -> Decimal:
    return max(promo(order) for promo in promos)
```

**Problem:** All functions in the module must be valid promos.

### Decorator-Enhanced Approach (Best)

```python
from typing import Callable
from decimal import Decimal

Promotion = Callable[['Order'], Decimal]
promos: list[Promotion] = []

def promotion(promo: Promotion) -> Promotion:
    """Registration decorator for promotions"""
    promos.append(promo)
    return promo

def best_promo(order: Order) -> Decimal:
    """Compute the best discount available"""
    return max(promo(order) for promo in promos)

@promotion
def fidelity(order: Order) -> Decimal:
    """5% discount for customers with 1000+ fidelity points"""
    if order.customer.fidelity >= 1000:
        return order.total() * Decimal('0.05')
    return Decimal(0)

@promotion
def bulk_item(order: Order) -> Decimal:
    """10% discount for line items with 20+ units"""
    # ... implementation
    pass

@promotion
def large_order(order: Order) -> Decimal:
    """7% discount for orders with 10+ distinct items"""
    # ... implementation
    pass
```

**Advantages:**
- No need for special naming conventions
- Decorator clearly marks the purpose
- Easy to disable (comment out decorator)
- Can define promos in any module

---

## The Command Pattern

### The Problem

Decouple an object that invokes an operation (invoker) from the object that implements it (receiver).

**Classic approach:** Command objects with an `execute()` method.

### Pythonic Approach: Use Callables

```python
# Instead of Command classes, use functions or callable objects

class MacroCommand:
    """A command that executes a list of commands"""

    def __init__(self, commands):
        self.commands = list(commands)

    def __call__(self):
        for command in self.commands:
            command()

# Usage
def save_document():
    print("Saving document...")

def close_document():
    print("Closing document...")

# Create a macro from functions
save_and_close = MacroCommand([save_document, close_document])
save_and_close()  # Executes both commands
```

### Commands with State (Using Closures)

```python
def make_undo_command(receiver, state_before):
    """Create an undoable command using a closure"""
    def undo():
        receiver.restore(state_before)
    return undo

# Or use a callable class for more complex state
class UndoableCommand:
    def __init__(self, receiver, action, undo_action):
        self.receiver = receiver
        self.action = action
        self.undo_action = undo_action
        self.executed = False

    def __call__(self):
        self.action(self.receiver)
        self.executed = True

    def undo(self):
        if self.executed:
            self.undo_action(self.receiver)
            self.executed = False
```

---

## General Pattern: Replace Single-Method Classes

**When you see this pattern:**
```python
class SomeHandler:
    def execute(self, *args):
        # do something
        pass

handler = SomeHandler()
handler.execute(data)
```

**Consider replacing with:**
```python
def some_handler(*args):
    # do something
    pass

some_handler(data)
```

**Or with a callable class if you need state:**
```python
class SomeHandler:
    def __init__(self, config):
        self.config = config

    def __call__(self, *args):
        # do something using self.config
        pass

handler = SomeHandler(config)
handler(data)  # Call directly
```

---

## Patterns That Simplify with First-Class Functions

| Pattern | Classic Approach | Pythonic Approach |
|---------|------------------|-------------------|
| **Strategy** | Abstract class + concrete subclasses | Functions |
| **Command** | Command objects with execute() | Callables (functions or `__call__`) |
| **Template Method** | Abstract class with hook methods | Functions with callbacks |
| **Visitor** | Visitor classes | Functions + `@singledispatch` |
| **Factory** | Factory classes | Factory functions |
| **Callback** | Listener/Observer objects | Functions |

---

## When to Still Use Classes

Functions aren't always the answer. Use classes when:

1. **State is needed between calls**
   ```python
   class Counter:
       def __init__(self):
           self.count = 0
       def __call__(self):
           self.count += 1
           return self.count
   ```

2. **Multiple related methods are needed**
   ```python
   class Command:
       def execute(self): ...
       def undo(self): ...
       def can_execute(self) -> bool: ...
   ```

3. **Inheritance/polymorphism is genuinely useful**

4. **You need to inspect/modify behavior at runtime**

5. **The interface is complex** (more than just "call this")

---

## Key Takeaways

1. **Functions are objects** - they can be stored in data structures, passed as arguments, returned from functions

2. **Single-method classes are often unnecessary** - a function does the same job with less code

3. **Callables unify the interface** - whether it's a function, a lambda, or a class with `__call__`, you invoke it the same way: `thing(args)`

4. **Registration decorators** are great for collecting related functions

5. **Module introspection** (`globals()`, `inspect`) can find functions dynamically

6. **Design patterns are starting points**, not destinations - adapt them to Python's strengths

---

## Quick Reference

```python
# Strategy with functions
strategies = [strategy_a, strategy_b, strategy_c]
best = max(s(data) for s in strategies)

# Command with callables
commands = [cmd1, cmd2, cmd3]
for cmd in commands:
    cmd()

# Registration decorator pattern
registry = []
def register(func):
    registry.append(func)
    return func

@register
def my_func(): ...

# Callable class (when you need state)
class Multiplier:
    def __init__(self, factor):
        self.factor = factor
    def __call__(self, x):
        return x * self.factor

double = Multiplier(2)
double(5)  # 10
```
