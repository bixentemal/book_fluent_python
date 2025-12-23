"""
Chapter 10: Design Patterns with First-Class Functions - Exercises
===================================================================

Complete each exercise by replacing the `None` or `...` placeholders.
Run this file to check your answers with the assertions.
"""

from __future__ import annotations
from decimal import Decimal
from typing import Callable, NamedTuple, Optional
from collections.abc import Sequence
import functools


# =============================================================================
# Exercise 1: Function as Strategy
# =============================================================================
# Replace a class-based strategy with a function

class Product(NamedTuple):
    name: str
    price: Decimal
    quantity: int


def calculate_total(products: list[Product]) -> Decimal:
    """Calculate total price of all products."""
    return sum(p.price * p.quantity for p in products)


# TODO: Implement these discount strategy functions
# Each takes a list of products and returns the discount amount (Decimal)

def no_discount(products: list[Product]) -> Decimal:
    """No discount applied."""
    ...
    pass


def ten_percent_discount(products: list[Product]) -> Decimal:
    """10% discount on total."""
    ...
    pass


def bulk_discount(products: list[Product]) -> Decimal:
    """
    $5 off for each product with quantity >= 10.
    Example: 2 products with qty >= 10 means $10 off.
    """
    ...
    pass


# Test the strategy functions
products = [
    Product("Apple", Decimal("1.00"), 5),
    Product("Banana", Decimal("0.50"), 15),
    Product("Orange", Decimal("0.75"), 10),
]

total = calculate_total(products)  # 1*5 + 0.5*15 + 0.75*10 = 5 + 7.5 + 7.5 = 20

assert no_discount(products) == Decimal("0"), f"Expected 0, got {no_discount(products)}"
assert ten_percent_discount(products) == Decimal("2.00"), f"Expected 2.00, got {ten_percent_discount(products)}"
assert bulk_discount(products) == Decimal("10.00"), f"Expected 10.00 (2 items with qty>=10), got {bulk_discount(products)}"

print("✓ Exercise 1 passed: Function as Strategy")


# =============================================================================
# Exercise 2: Selecting the Best Strategy
# =============================================================================
# Create a function that selects the strategy giving the maximum discount

# List of available discount strategies
discount_strategies = [no_discount, ten_percent_discount, bulk_discount]


def best_discount(products: list[Product]) -> Decimal:
    """
    Return the maximum discount available from all strategies.

    TODO: Implement using max() with a generator expression
    """
    ...
    pass


def apply_best_discount(products: list[Product]) -> Decimal:
    """
    Return the final price after applying the best discount.

    TODO: Implement
    """
    ...
    pass


assert best_discount(products) == Decimal("10.00"), f"Expected 10.00, got {best_discount(products)}"
assert apply_best_discount(products) == Decimal("10.00"), f"Expected 10.00, got {apply_best_discount(products)}"

# Test with different products where 10% is better
expensive_products = [
    Product("Laptop", Decimal("1000.00"), 1),
    Product("Mouse", Decimal("50.00"), 1),
]
assert best_discount(expensive_products) == Decimal("105.00")  # 10% of 1050

print("✓ Exercise 2 passed: Selecting the Best Strategy")


# =============================================================================
# Exercise 3: Registration Decorator for Strategies
# =============================================================================
# Use a decorator to automatically register strategies

# This list will hold all registered tax strategies
tax_strategies: list[Callable[[Decimal], Decimal]] = []


def tax_strategy(func: Callable[[Decimal], Decimal]) -> Callable[[Decimal], Decimal]:
    """
    Decorator that registers a tax calculation strategy.

    TODO: Append func to tax_strategies and return func unchanged
    """
    ...
    pass


# Apply the decorator to register these strategies
# TODO: Add @tax_strategy decorator to each function below

def no_tax(amount: Decimal) -> Decimal:
    """No tax."""
    return Decimal("0")


def standard_tax(amount: Decimal) -> Decimal:
    """Standard 10% tax."""
    return amount * Decimal("0.10")


def luxury_tax(amount: Decimal) -> Decimal:
    """Luxury 20% tax."""
    return amount * Decimal("0.20")


# Verify registration worked
assert len(tax_strategies) == 3, f"Expected 3 registered strategies, got {len(tax_strategies)}"
assert no_tax in tax_strategies
assert standard_tax in tax_strategies
assert luxury_tax in tax_strategies

# Verify functions still work
assert standard_tax(Decimal("100")) == Decimal("10.00")

print("✓ Exercise 3 passed: Registration Decorator for Strategies")


# =============================================================================
# Exercise 4: Command Pattern with Functions
# =============================================================================
# Implement a simple command pattern using functions

class TextEditor:
    """A simple text editor that tracks content."""

    def __init__(self):
        self.content = ""

    def insert(self, text: str) -> None:
        self.content += text

    def delete(self, count: int) -> str:
        """Delete last `count` characters and return them."""
        deleted = self.content[-count:]
        self.content = self.content[:-count]
        return deleted

    def clear(self) -> str:
        """Clear all content and return it."""
        old_content = self.content
        self.content = ""
        return old_content


def make_insert_command(editor: TextEditor, text: str) -> Callable[[], None]:
    """
    Create a command that inserts text into the editor.

    TODO: Return a function that calls editor.insert(text)
    """
    ...
    pass


def make_delete_command(editor: TextEditor, count: int) -> Callable[[], None]:
    """
    Create a command that deletes `count` characters from the editor.

    TODO: Return a function that calls editor.delete(count)
    """
    ...
    pass


editor = TextEditor()
insert_hello = make_insert_command(editor, "Hello")
insert_world = make_insert_command(editor, " World")
delete_5 = make_delete_command(editor, 5)

insert_hello()
assert editor.content == "Hello"
insert_world()
assert editor.content == "Hello World"
delete_5()
assert editor.content == "Hello "

print("✓ Exercise 4 passed: Command Pattern with Functions")


# =============================================================================
# Exercise 5: MacroCommand - Composite Commands
# =============================================================================
# Create a class that executes multiple commands in sequence

class MacroCommand:
    """
    A command that executes a sequence of commands.

    Usage:
        macro = MacroCommand([cmd1, cmd2, cmd3])
        macro()  # Executes cmd1, cmd2, cmd3 in order
    """

    def __init__(self, commands: Sequence[Callable[[], None]]):
        """
        TODO: Store the commands as a list
        """
        ...
        pass

    def __call__(self) -> None:
        """
        TODO: Execute each command in sequence
        """
        ...
        pass


editor2 = TextEditor()
cmd1 = make_insert_command(editor2, "First ")
cmd2 = make_insert_command(editor2, "Second ")
cmd3 = make_insert_command(editor2, "Third")

macro = MacroCommand([cmd1, cmd2, cmd3])
macro()

assert editor2.content == "First Second Third", f"Got: {editor2.content}"

# Verify it's callable
assert callable(macro)

print("✓ Exercise 5 passed: MacroCommand - Composite Commands")


# =============================================================================
# Exercise 6: Strategy with Callable Class (Stateful Strategy)
# =============================================================================
# When strategy needs state, use a callable class

class ProgressiveDiscount:
    """
    A discount strategy that gives bigger discounts for repeat customers.
    First purchase: 0% discount
    Second purchase: 5% discount
    Third+ purchase: 10% discount

    TODO: Implement __init__ and __call__
    """

    def __init__(self):
        """Initialize the purchase counter."""
        ...
        pass

    def __call__(self, amount: Decimal) -> Decimal:
        """
        Calculate discount based on purchase history.
        Increment counter after each call.

        TODO: Implement
        """
        ...
        pass


progressive = ProgressiveDiscount()

assert progressive(Decimal("100")) == Decimal("0")  # First: 0%
assert progressive(Decimal("100")) == Decimal("5")  # Second: 5%
assert progressive(Decimal("100")) == Decimal("10")  # Third: 10%
assert progressive(Decimal("100")) == Decimal("10")  # Fourth: still 10%

# Different customer, fresh state
progressive2 = ProgressiveDiscount()
assert progressive2(Decimal("200")) == Decimal("0")  # First: 0%

print("✓ Exercise 6 passed: Strategy with Callable Class")


# =============================================================================
# Exercise 7: Finding Strategies Dynamically
# =============================================================================
# Use introspection to find all strategies matching a pattern

# These are shipping strategies (all end with _shipping)
def standard_shipping(weight: float) -> Decimal:
    """$5 flat rate."""
    return Decimal("5.00")


def express_shipping(weight: float) -> Decimal:
    """$10 + $0.50 per pound."""
    return Decimal("10.00") + Decimal(str(weight)) * Decimal("0.50")


def overnight_shipping(weight: float) -> Decimal:
    """$25 + $1 per pound."""
    return Decimal("25.00") + Decimal(str(weight)) * Decimal("1.00")


def calculate_tax(amount: Decimal) -> Decimal:
    """This is NOT a shipping strategy."""
    return amount * Decimal("0.08")


def find_shipping_strategies() -> list[Callable[[float], Decimal]]:
    """
    Find all functions in the current module that end with '_shipping'.

    TODO: Use globals() to find all shipping strategy functions
    Hint: globals() returns a dict of name -> value
    Filter for names ending with '_shipping' and values that are callable
    """
    ...
    pass


shipping_strategies = find_shipping_strategies()
assert len(shipping_strategies) == 3, f"Expected 3 shipping strategies, got {len(shipping_strategies)}"
assert standard_shipping in shipping_strategies
assert express_shipping in shipping_strategies
assert overnight_shipping in shipping_strategies
assert calculate_tax not in shipping_strategies

print("✓ Exercise 7 passed: Finding Strategies Dynamically")


# =============================================================================
# Exercise 8: Best Shipping Strategy
# =============================================================================
# Find the cheapest shipping option

def cheapest_shipping(weight: float) -> tuple[str, Decimal]:
    """
    Find the cheapest shipping option for the given weight.
    Return a tuple of (strategy_name, cost).

    TODO: Implement using find_shipping_strategies()
    Hint: Use min() with a key function
    """
    ...
    pass


name, cost = cheapest_shipping(5.0)
assert name == "standard_shipping", f"Expected standard_shipping, got {name}"
assert cost == Decimal("5.00")

# For heavy packages, express might be cheaper than overnight
name2, cost2 = cheapest_shipping(100.0)
assert name2 == "standard_shipping"  # Still cheapest at flat rate
assert cost2 == Decimal("5.00")

print("✓ Exercise 8 passed: Best Shipping Strategy")


# =============================================================================
# Exercise 9: Command with Undo
# =============================================================================
# Implement commands that can be undone

class UndoableTextEditor:
    """Text editor with undo support."""

    def __init__(self):
        self.content = ""
        self.history: list[Callable[[], None]] = []  # Stack of undo functions

    def insert(self, text: str) -> None:
        self.content += text

    def delete_last(self, count: int) -> str:
        deleted = self.content[-count:] if count <= len(self.content) else self.content
        self.content = self.content[:-count] if count <= len(self.content) else ""
        return deleted

    def undo(self) -> None:
        """Execute the last undo function."""
        if self.history:
            undo_func = self.history.pop()
            undo_func()


def make_undoable_insert(editor: UndoableTextEditor, text: str) -> Callable[[], None]:
    """
    Create a command that:
    1. Inserts text into editor
    2. Pushes an undo function onto editor.history

    The undo function should delete len(text) characters.

    TODO: Implement
    """
    ...
    pass


def make_undoable_delete(editor: UndoableTextEditor, count: int) -> Callable[[], None]:
    """
    Create a command that:
    1. Deletes `count` characters from editor
    2. Pushes an undo function onto editor.history

    The undo function should re-insert the deleted text.

    TODO: Implement using a closure to capture the deleted text
    """
    ...
    pass


undo_editor = UndoableTextEditor()

insert_cmd = make_undoable_insert(undo_editor, "Hello")
insert_cmd()
assert undo_editor.content == "Hello"

insert_cmd2 = make_undoable_insert(undo_editor, " World")
insert_cmd2()
assert undo_editor.content == "Hello World"

undo_editor.undo()  # Undo " World"
assert undo_editor.content == "Hello", f"After undo, expected 'Hello', got '{undo_editor.content}'"

undo_editor.undo()  # Undo "Hello"
assert undo_editor.content == "", f"After second undo, expected '', got '{undo_editor.content}'"

# Test undoable delete
undo_editor.content = "ABCDEF"
undo_editor.history.clear()

delete_cmd = make_undoable_delete(undo_editor, 3)
delete_cmd()
assert undo_editor.content == "ABC"

undo_editor.undo()  # Should restore "DEF"
assert undo_editor.content == "ABCDEF", f"Expected 'ABCDEF', got '{undo_editor.content}'"

print("✓ Exercise 9 passed: Command with Undo")


# =============================================================================
# Exercise 10: Validator Strategy Pattern
# =============================================================================
# Use functions as validation strategies

# Type alias for validator functions
Validator = Callable[[str], tuple[bool, str]]  # Returns (is_valid, error_message)


def validate_not_empty(value: str) -> tuple[bool, str]:
    """
    Validate that value is not empty.

    TODO: Return (True, "") if valid, (False, "Value cannot be empty") if not
    """
    ...
    pass


def validate_min_length(min_len: int) -> Validator:
    """
    Factory function that creates a minimum length validator.

    TODO: Return a validator function that checks len(value) >= min_len
    Error message should be f"Value must be at least {min_len} characters"
    """
    ...
    pass


def validate_alphanumeric(value: str) -> tuple[bool, str]:
    """
    Validate that value contains only alphanumeric characters.

    TODO: Return (True, "") if valid, (False, "Value must be alphanumeric") if not
    """
    ...
    pass


def validate_all(value: str, validators: list[Validator]) -> tuple[bool, list[str]]:
    """
    Run all validators and collect errors.

    TODO: Return (True, []) if all pass, (False, [list of error messages]) if any fail
    """
    ...
    pass


# Test individual validators
assert validate_not_empty("hello") == (True, "")
assert validate_not_empty("") == (False, "Value cannot be empty")

validate_min_5 = validate_min_length(5)
assert validate_min_5("hello") == (True, "")
assert validate_min_5("hi") == (False, "Value must be at least 5 characters")

assert validate_alphanumeric("hello123") == (True, "")
assert validate_alphanumeric("hello!") == (False, "Value must be alphanumeric")

# Test combined validation
validators = [validate_not_empty, validate_min_length(5), validate_alphanumeric]

is_valid, errors = validate_all("hello123", validators)
assert is_valid == True
assert errors == []

is_valid, errors = validate_all("hi!", validators)
assert is_valid == False
assert len(errors) == 2  # Too short AND not alphanumeric

print("✓ Exercise 10 passed: Validator Strategy Pattern")


# =============================================================================
# Exercise 11: Event Handler Registry
# =============================================================================
# Implement event handling using the registration pattern

# Event handler registry: event_name -> list of handler functions
event_handlers: dict[str, list[Callable[..., None]]] = {}


def on(event_name: str) -> Callable[[Callable], Callable]:
    """
    Decorator factory that registers a function as an event handler.

    Usage:
        @on('user_login')
        def handle_login(user):
            print(f"User {user} logged in")

    TODO: Implement this decorator factory
    """
    ...
    pass


def emit(event_name: str, *args, **kwargs) -> None:
    """
    Emit an event, calling all registered handlers.

    TODO: Implement
    """
    ...
    pass


# Register event handlers
@on('startup')
def log_startup():
    startup_log.append("System starting...")


@on('startup')
def init_database():
    startup_log.append("Database initialized")


@on('shutdown')
def cleanup():
    shutdown_log.append("Cleanup complete")


# Test event emission
startup_log = []
shutdown_log = []

emit('startup')
assert len(startup_log) == 2
assert "System starting..." in startup_log
assert "Database initialized" in startup_log

emit('shutdown')
assert len(shutdown_log) == 1
assert "Cleanup complete" in shutdown_log

# Emit unknown event (should do nothing, not error)
emit('unknown_event')

print("✓ Exercise 11 passed: Event Handler Registry")


# =============================================================================
# Exercise 12: Pipeline Pattern
# =============================================================================
# Create a data processing pipeline using functions

# Type for a processing step: takes a value, returns transformed value
Step = Callable[[str], str]


class Pipeline:
    """
    A processing pipeline that chains multiple transformation steps.

    Usage:
        pipeline = Pipeline()
        pipeline.add_step(str.lower)
        pipeline.add_step(str.strip)
        result = pipeline.process("  HELLO  ")  # Returns "hello"

    TODO: Implement add_step, process, and __call__
    """

    def __init__(self):
        """Initialize with empty steps list."""
        ...
        pass

    def add_step(self, step: Step) -> 'Pipeline':
        """
        Add a processing step. Return self for chaining.
        """
        ...
        pass

    def process(self, value: str) -> str:
        """
        Run value through all steps in order.
        """
        ...
        pass

    def __call__(self, value: str) -> str:
        """
        Make pipeline callable (same as process).
        """
        ...
        pass


# Build a text normalization pipeline
normalize = Pipeline()
normalize.add_step(str.strip)
normalize.add_step(str.lower)
normalize.add_step(lambda s: s.replace("  ", " "))  # Remove double spaces

assert normalize.process("  HELLO   WORLD  ") == "hello  world"  # Note: only outer spaces stripped
assert normalize("  TEST  ") == "test"  # Should be callable

# Test method chaining
pipeline2 = Pipeline().add_step(str.upper).add_step(lambda s: s + "!")
assert pipeline2("hello") == "HELLO!"

print("✓ Exercise 12 passed: Pipeline Pattern")


# =============================================================================
# Exercise 13: Lazy Command Execution
# =============================================================================
# Create commands that are only executed when explicitly invoked

class LazyComputation:
    """
    Wraps a function for lazy evaluation.
    The function is only called when .get() is invoked.
    Result is cached after first computation.

    TODO: Implement __init__, get, and computed property
    """

    def __init__(self, func: Callable[[], any]):
        """Store the function without executing it."""
        ...
        pass

    @property
    def computed(self) -> bool:
        """Return True if the value has been computed."""
        ...
        pass

    def get(self) -> any:
        """
        Return the computed value.
        Compute and cache on first call.
        """
        ...
        pass


computation_count = 0


def expensive_computation():
    global computation_count
    computation_count += 1
    return sum(range(1000))


lazy = LazyComputation(expensive_computation)

assert lazy.computed == False
assert computation_count == 0  # Not computed yet

result1 = lazy.get()
assert result1 == 499500
assert lazy.computed == True
assert computation_count == 1  # Computed once

result2 = lazy.get()
assert result2 == 499500
assert computation_count == 1  # Still 1 - cached!

print("✓ Exercise 13 passed: Lazy Command Execution")


# =============================================================================
# Exercise 14: Combining Strategies with Higher-Order Functions
# =============================================================================
# Create utility functions for combining strategies

def combine_discounts(*discount_funcs: Callable[[Decimal], Decimal]) -> Callable[[Decimal], Decimal]:
    """
    Combine multiple discount functions by summing their results.

    TODO: Return a function that applies all discounts and returns the total
    """
    ...
    pass


def cap_discount(max_discount: Decimal) -> Callable[[Callable[[Decimal], Decimal]], Callable[[Decimal], Decimal]]:
    """
    Decorator factory that caps the maximum discount.

    TODO: Return a decorator that limits the discount to max_discount
    """
    ...
    pass


def percentage_discount(percentage: int) -> Callable[[Decimal], Decimal]:
    """Helper: Create a percentage discount function."""
    rate = Decimal(percentage) / Decimal(100)
    return lambda amount: amount * rate


# Test combining discounts
member_discount = percentage_discount(5)   # 5% off
holiday_discount = percentage_discount(10)  # 10% off

combined = combine_discounts(member_discount, holiday_discount)
assert combined(Decimal("100")) == Decimal("15")  # 5 + 10

# Test capped discount
@cap_discount(Decimal("20"))
def big_discount(amount: Decimal) -> Decimal:
    return amount * Decimal("0.50")  # 50% off

assert big_discount(Decimal("100")) == Decimal("20")  # Capped at 20
assert big_discount(Decimal("30")) == Decimal("15")   # 15 < 20, not capped

print("✓ Exercise 14 passed: Combining Strategies with Higher-Order Functions")


# =============================================================================
# All exercises completed!
# =============================================================================
print("\n" + "=" * 65)
print("🎉 Congratulations! All Chapter 10 exercises passed!")
print("=" * 65)
