"""
Chapter 7: Functions as First-Class Objects - Exercises
========================================================

Complete each exercise by replacing the `None` or `...` placeholders.
Run this file to check your answers with the assertions.
"""

from functools import reduce, partial
from operator import itemgetter, attrgetter, methodcaller, mul, add

# =============================================================================
# Exercise 1: Functions as Objects
# =============================================================================
# Demonstrate that functions are first-class objects

def square(x):
    """Return x squared."""
    return x ** 2

def cube(x):
    """Return x cubed."""
    return x ** 3

# TODO: Create a dictionary mapping operation names to functions
math_ops = None  # {'square': square, 'cube': cube}

# TODO: Use the dictionary to compute 4 squared and 3 cubed
result_square = None  # Should be 16
result_cube = None    # Should be 27

assert math_ops == {'square': square, 'cube': cube}
assert result_square == 16, f"Expected 16, got {result_square}"
assert result_cube == 27, f"Expected 27, got {result_cube}"
print("✓ Exercise 1 passed: Functions as Objects")


# =============================================================================
# Exercise 2: Higher-Order Function
# =============================================================================
# Create a higher-order function that applies a function n times

def apply_n_times(func, value, n):
    """
    Apply func to value, n times.
    Example: apply_n_times(square, 2, 3) = square(square(square(2))) = 256

    TODO: Implement this function
    """
    ...
    pass


assert apply_n_times(square, 2, 1) == 4, "square(2) = 4"
assert apply_n_times(square, 2, 2) == 16, "square(square(2)) = 16"
assert apply_n_times(square, 2, 3) == 256, "square(square(square(2))) = 256"
assert apply_n_times(lambda x: x + 1, 0, 5) == 5, "Add 1 five times to 0 = 5"
print("✓ Exercise 2 passed: Higher-Order Function")


# =============================================================================
# Exercise 3: Replace map/filter with Comprehensions
# =============================================================================
# Rewrite these map/filter expressions using list comprehensions

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# OLD: list(map(lambda x: x ** 2, numbers))
# TODO: Rewrite using list comprehension
squared_numbers = None

# OLD: list(filter(lambda x: x % 2 == 0, numbers))
# TODO: Rewrite using list comprehension
even_numbers = None

# OLD: list(map(lambda x: x ** 2, filter(lambda x: x % 2 == 0, numbers)))
# TODO: Rewrite using list comprehension (combine map and filter)
squared_evens = None

assert squared_numbers == [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
assert even_numbers == [2, 4, 6, 8, 10]
assert squared_evens == [4, 16, 36, 64, 100]
print("✓ Exercise 3 passed: Replace map/filter with Comprehensions")


# =============================================================================
# Exercise 4: Replace reduce with Built-ins
# =============================================================================
# Replace reduce with more Pythonic alternatives

numbers = [1, 2, 3, 4, 5]

# OLD: reduce(add, numbers)
# TODO: Use built-in function
total = None

# OLD: reduce(mul, numbers)
# TODO: Use built-in function (hint: import from math)
import math
product = None

# OLD: reduce(lambda acc, x: acc if acc > x else x, numbers)
# TODO: Use built-in function
maximum = None

# OLD: reduce(lambda acc, x: acc and x > 0, numbers, True)
# TODO: Use built-in function with generator expression
all_positive = None

assert total == 15
assert product == 120
assert maximum == 5
assert all_positive == True
print("✓ Exercise 4 passed: Replace reduce with Built-ins")


# =============================================================================
# Exercise 5: Using operator.itemgetter
# =============================================================================
# Use itemgetter to sort and extract data

students = [
    {'name': 'Alice', 'grade': 'B', 'age': 22},
    {'name': 'Bob', 'grade': 'A', 'age': 20},
    {'name': 'Charlie', 'grade': 'C', 'age': 21},
    {'name': 'Diana', 'grade': 'A', 'age': 19},
]

# TODO: Sort students by age using itemgetter (not lambda)
sorted_by_age = None

# TODO: Sort students by grade, then by name using itemgetter
sorted_by_grade_name = None

# TODO: Extract just the names using itemgetter and map
names_only = None  # Should be ['Alice', 'Bob', 'Charlie', 'Diana']

assert [s['name'] for s in sorted_by_age] == ['Diana', 'Bob', 'Charlie', 'Alice']
assert [s['name'] for s in sorted_by_grade_name] == ['Bob', 'Diana', 'Alice', 'Charlie']
assert names_only == ['Alice', 'Bob', 'Charlie', 'Diana']
print("✓ Exercise 5 passed: Using operator.itemgetter")


# =============================================================================
# Exercise 6: Using operator.attrgetter
# =============================================================================
# Use attrgetter to work with objects

from collections import namedtuple

City = namedtuple('City', ['name', 'country', 'population'])

cities = [
    City('Tokyo', 'Japan', 37400000),
    City('Delhi', 'India', 28514000),
    City('Shanghai', 'China', 25582000),
    City('São Paulo', 'Brazil', 21650000),
    City('Mexico City', 'Mexico', 21581000),
]

# TODO: Sort cities by population (descending) using attrgetter
sorted_by_pop_desc = None

# TODO: Get the country of the most populous city using attrgetter
get_country = None  # Create the attrgetter
most_populous_country = None  # Apply it to get the country

# TODO: Extract all city names using attrgetter and map
city_names = None

assert [c.name for c in sorted_by_pop_desc] == ['Tokyo', 'Delhi', 'Shanghai', 'São Paulo', 'Mexico City']
assert most_populous_country == 'Japan'
assert city_names == ['Tokyo', 'Delhi', 'Shanghai', 'São Paulo', 'Mexico City']
print("✓ Exercise 6 passed: Using operator.attrgetter")


# =============================================================================
# Exercise 7: Using operator.methodcaller
# =============================================================================
# Use methodcaller to call methods on objects

words = ['  hello  ', '  WORLD  ', '  Python  ']

# TODO: Use methodcaller to strip whitespace from all words
# Hint: methodcaller('strip') creates a callable that calls .strip() on its argument
stripped = None

# TODO: Use methodcaller to replace spaces with underscores in this string
text = "hello world python"
replace_spaces = None  # Create methodcaller for replace(' ', '_')
result = None          # Apply it to text

# TODO: Chain operations: upper + strip using map and methodcaller
upper_stripped = None  # Result should be ['HELLO', 'WORLD', 'PYTHON']

assert stripped == ['hello', 'WORLD', 'Python']
assert result == 'hello_world_python'
assert upper_stripped == ['HELLO', 'WORLD', 'PYTHON']
print("✓ Exercise 7 passed: Using operator.methodcaller")


# =============================================================================
# Exercise 8: Using functools.partial
# =============================================================================
# Use partial to create specialized functions

def power(base, exponent):
    return base ** exponent

# TODO: Create a 'square' function using partial (exponent=2)
square_partial = None

# TODO: Create a 'cube' function using partial (exponent=3)
cube_partial = None

# TODO: Create a function to parse binary strings using partial
# Hint: int('1010', base=2) returns 10
parse_binary = None

# TODO: Create a function to parse hex strings using partial
parse_hex = None

assert square_partial(5) == 25
assert cube_partial(3) == 27
assert parse_binary('1010') == 10
assert parse_binary('1111') == 15
assert parse_hex('ff') == 255
assert parse_hex('10') == 16
print("✓ Exercise 8 passed: Using functools.partial")


# =============================================================================
# Exercise 9: Callable Class (with __call__)
# =============================================================================
# Create a callable class that counts how many times it's been called

class CallCounter:
    """
    A callable that wraps a function and counts how many times it's been called.

    Usage:
        counter = CallCounter(some_func)
        counter(args)  # Calls some_func(args) and increments count
        counter.count  # Returns number of times called
    """

    def __init__(self, func):
        # TODO: Store the function and initialize count
        ...
        pass

    def __call__(self, *args, **kwargs):
        # TODO: Increment count and call the wrapped function
        ...
        pass


def greet(name):
    return f"Hello, {name}!"

counted_greet = CallCounter(greet)

assert counted_greet.count == 0
result1 = counted_greet("Alice")
assert result1 == "Hello, Alice!"
assert counted_greet.count == 1

result2 = counted_greet("Bob")
assert result2 == "Hello, Bob!"
assert counted_greet.count == 2

# Verify it's callable
assert callable(counted_greet)

print("✓ Exercise 9 passed: Callable Class")


# =============================================================================
# Exercise 10: Function Factory (Higher-Order Function)
# =============================================================================
# Create a function that returns other functions

def make_validator(min_val, max_val):
    """
    Return a function that checks if a value is within [min_val, max_val].

    Example:
        is_valid_percentage = make_validator(0, 100)
        is_valid_percentage(50)  # True
        is_valid_percentage(150) # False

    TODO: Implement this function factory
    """
    ...
    pass


is_valid_percentage = make_validator(0, 100)
is_valid_age = make_validator(0, 150)
is_valid_temperature_celsius = make_validator(-273.15, 1000)

assert is_valid_percentage(50) == True
assert is_valid_percentage(0) == True
assert is_valid_percentage(100) == True
assert is_valid_percentage(-1) == False
assert is_valid_percentage(101) == False

assert is_valid_age(25) == True
assert is_valid_age(200) == False

assert is_valid_temperature_celsius(-273.15) == True
assert is_valid_temperature_celsius(-300) == False

print("✓ Exercise 10 passed: Function Factory")


# =============================================================================
# Exercise 11: Practical - Sort with Multiple Criteria
# =============================================================================
# Sort a list of products using various techniques

Product = namedtuple('Product', ['name', 'category', 'price', 'rating'])

products = [
    Product('Laptop', 'Electronics', 999.99, 4.5),
    Product('Headphones', 'Electronics', 149.99, 4.8),
    Product('Coffee Maker', 'Kitchen', 79.99, 4.2),
    Product('Blender', 'Kitchen', 49.99, 4.0),
    Product('Smartphone', 'Electronics', 699.99, 4.7),
    Product('Toaster', 'Kitchen', 29.99, 3.8),
]

# TODO: Sort by price (ascending) using attrgetter
by_price = None

# TODO: Sort by rating (descending) using attrgetter and reverse=True
by_rating_desc = None

# TODO: Sort by category, then by price (ascending) using attrgetter with multiple fields
by_category_price = None

# TODO: Get the cheapest product in each category
# Hint: Sort by category and price, then use a dict comprehension
cheapest_by_category = None  # {'Electronics': 'Headphones', 'Kitchen': 'Toaster'}

assert [p.name for p in by_price] == ['Toaster', 'Blender', 'Coffee Maker', 'Headphones', 'Smartphone', 'Laptop']
assert [p.name for p in by_rating_desc] == ['Headphones', 'Smartphone', 'Laptop', 'Coffee Maker', 'Blender', 'Toaster']
assert [p.name for p in by_category_price] == ['Headphones', 'Smartphone', 'Laptop', 'Toaster', 'Blender', 'Coffee Maker']
assert cheapest_by_category == {'Electronics': 'Headphones', 'Kitchen': 'Toaster'}
print("✓ Exercise 11 passed: Sort with Multiple Criteria")


# =============================================================================
# Exercise 12: Compose Functions
# =============================================================================
# Create a compose function that combines multiple functions

def compose(*functions):
    """
    Return a function that applies all functions right-to-left.

    Example:
        f = compose(str, lambda x: x + 1, lambda x: x * 2)
        f(5) == str((5 * 2) + 1) == '11'

    TODO: Implement using reduce
    Hint: reduce(lambda acc, f: f(acc), reversed(functions), initial_value)
    """
    def composed(x):
        ...
        pass
    return composed


# Test composition
add_one = lambda x: x + 1
double = lambda x: x * 2
to_string = str

# compose applies right-to-left: to_string(double(add_one(5))) = '12'
pipeline = compose(to_string, double, add_one)
assert pipeline(5) == '12', f"Expected '12', got {pipeline(5)}"

# Another test
negate = lambda x: -x
composed = compose(str, negate, double, add_one)
assert composed(3) == '-8'  # str(negate(double(add_one(3)))) = str(-(3+1)*2) = '-8'

print("✓ Exercise 12 passed: Compose Functions")


# =============================================================================
# All exercises completed!
# =============================================================================
print("\n" + "=" * 60)
print("🎉 Congratulations! All Chapter 7 exercises passed!")
print("=" * 60)
