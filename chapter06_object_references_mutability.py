"""
Chapter 6: Object References, Mutability, and Recycling - Exercises
====================================================================

Complete each exercise by replacing the `None` or `...` placeholders.
Run this file to check your answers with the assertions.
"""

# =============================================================================
# Exercise 1: Identity vs Equality
# =============================================================================
# Given two lists with the same content, determine if they are equal (==)
# and if they are identical (is)

list_a = [1, 2, 3]
list_b = [1, 2, 3]
list_c = list_a

# TODO: Fill in True or False
are_a_b_equal = None          # Are list_a and list_b equal in value?
are_a_b_identical = None      # Are list_a and list_b the same object?
are_a_c_equal = None          # Are list_a and list_c equal in value?
are_a_c_identical = None      # Are list_a and list_c the same object?

assert are_a_b_equal == True, "list_a and list_b have the same values"
assert are_a_b_identical == False, "list_a and list_b are different objects"
assert are_a_c_equal == True, "list_a and list_c have the same values"
assert are_a_c_identical == True, "list_c is an alias to list_a"
print("✓ Exercise 1 passed: Identity vs Equality")


# =============================================================================
# Exercise 2: Shallow Copy Behavior
# =============================================================================
# Predict the behavior of shallow copies with nested mutable objects

original = [[1, 2], [3, 4]]
shallow_copy = list(original)  # This creates a shallow copy

# Modify the shallow copy
shallow_copy.append([5, 6])
shallow_copy[0][0] = 'X'

# TODO: What are the values now? Fill in the expected lists
expected_original = None       # What does `original` contain now?
expected_shallow = None        # What does `shallow_copy` contain now?

assert original == expected_original, f"Original should be {expected_original}, got {original}"
assert shallow_copy == expected_shallow, f"Shallow copy should be {expected_shallow}, got {shallow_copy}"
print("✓ Exercise 2 passed: Shallow Copy Behavior")


# =============================================================================
# Exercise 3: Deep Copy Independence
# =============================================================================
# Use deepcopy to create a fully independent copy

from copy import deepcopy

data = {'users': [{'name': 'Alice'}, {'name': 'Bob'}]}

# TODO: Create a deep copy of data
data_copy = None

# Modify the copy
data_copy['users'][0]['name'] = 'Charlie'
data_copy['users'].append({'name': 'Dave'})

# Assertions - original should be unchanged
assert data == {'users': [{'name': 'Alice'}, {'name': 'Bob'}]}, "Original should be unchanged"
assert data_copy == {'users': [{'name': 'Charlie'}, {'name': 'Bob'}, {'name': 'Dave'}]}, "Copy should be modified"
print("✓ Exercise 3 passed: Deep Copy Independence")


# =============================================================================
# Exercise 4: Fix the Mutable Default Bug
# =============================================================================
# This function has a bug - it uses a mutable default argument.
# Fix it using the None sentinel pattern.

# BUGGY VERSION (don't use this pattern!)
def buggy_add_item(item, items=[]):
    items.append(item)
    return items

# TODO: Write the fixed version below
def add_item(item, items=None):
    # Fix this function to avoid the mutable default bug
    ...
    pass


# Test the fixed function
result1 = add_item('a')
result2 = add_item('b')
result3 = add_item('c', ['x', 'y'])

assert result1 == ['a'], f"First call should return ['a'], got {result1}"
assert result2 == ['b'], f"Second call should return ['b'], got {result2}"
assert result3 == ['x', 'y', 'c'], f"Third call should return ['x', 'y', 'c'], got {result3}"
print("✓ Exercise 4 passed: Fixed Mutable Default Bug")


# =============================================================================
# Exercise 5: Defensive Copy in Class
# =============================================================================
# Complete the ShoppingCart class to protect internal state from external modification

class ShoppingCart:
    """A shopping cart that protects its internal items list."""

    def __init__(self, items=None):
        # TODO: Store items defensively (don't allow external list to affect internal state)
        # Hint: Make a copy of the incoming list
        self._items = None

    @property
    def items(self):
        # TODO: Return items defensively (don't expose internal list)
        # Hint: Return a copy so external code can't modify internal state
        return None

    def add(self, item):
        self._items.append(item)


# Test defensive copying
external_list = ['apple', 'banana']
cart = ShoppingCart(external_list)

# Modifying external list should NOT affect cart
external_list.append('cherry')
assert 'cherry' not in cart.items, "External modification should not affect cart"

# Modifying returned items should NOT affect cart
returned_items = cart.items
returned_items.append('durian')
assert 'durian' not in cart.items, "Modifying returned list should not affect cart"

# Adding via method should work
cart.add('elderberry')
assert 'elderberry' in cart.items, "Adding via method should work"

print("✓ Exercise 5 passed: Defensive Copy in Class")


# =============================================================================
# Exercise 6: Understanding References
# =============================================================================
# Predict what happens when we delete references

class TrackedObject:
    instances = []

    def __init__(self, name):
        self.name = name
        TrackedObject.instances.append(self)

    def __repr__(self):
        return f"TrackedObject({self.name!r})"


# Clear any previous instances
TrackedObject.instances.clear()

obj1 = TrackedObject('first')
obj2 = obj1  # Alias
obj3 = TrackedObject('second')

# TODO: How many instances exist?
count_before_del = None

del obj1

# TODO: How many instances still exist? (objects are only deleted when no refs remain)
count_after_del_obj1 = None

# TODO: Can we still access the 'first' object through obj2?
can_access_first_via_obj2 = None  # True or False

del obj2

# TODO: Now how many TrackedObject instances are still referenced in instances list?
# Note: instances list still holds references!
count_in_instances_list = None

assert count_before_del == 2, "Two TrackedObject instances were created"
assert count_after_del_obj1 == 2, "Deleting obj1 doesn't delete the object (obj2 still refs it)"
assert can_access_first_via_obj2 == True, "obj2 is still a valid reference"
assert count_in_instances_list == 2, "instances list still holds both objects"
print("✓ Exercise 6 passed: Understanding References")


# =============================================================================
# Exercise 7: Tuple Immutability Gotcha
# =============================================================================
# Tuples are immutable, but their contents might not be!

t = (1, 2, [3, 4])

# TODO: What happens when we try these operations?
# Set to True if it succeeds, False if it raises an error

# Trying to reassign an element of the tuple
try:
    t[0] = 99
    reassign_succeeded = True
except TypeError:
    reassign_succeeded = False

can_reassign_tuple_element = None  # What should this be?

# Trying to modify the list inside the tuple
try:
    t[2].append(5)
    modify_inner_list_succeeded = True
except TypeError:
    modify_inner_list_succeeded = False

can_modify_inner_list = None  # What should this be?

# What is t now?
expected_t = None  # Fill in the expected tuple value

assert can_reassign_tuple_element == reassign_succeeded
assert can_modify_inner_list == modify_inner_list_succeeded
assert t == expected_t, f"Expected {expected_t}, got {t}"
print("✓ Exercise 7 passed: Tuple Immutability Gotcha")


# =============================================================================
# Exercise 8: Practical - Safe Config Handler
# =============================================================================
# Create a configuration handler that safely manages default settings

class ConfigHandler:
    """
    A configuration handler that:
    1. Has sensible defaults
    2. Allows overriding with custom config
    3. Protects defaults from modification
    """

    DEFAULT_CONFIG = {
        'debug': False,
        'timeout': 30,
        'retries': 3,
        'endpoints': ['api.example.com']
    }

    def __init__(self, custom_config=None):
        # TODO: Initialize self.config by merging DEFAULT_CONFIG with custom_config
        # Requirements:
        # 1. Start with a COPY of DEFAULT_CONFIG (don't modify the class attribute)
        # 2. If custom_config is provided, update with those values
        # 3. Make sure nested mutables (like 'endpoints') are also copied
        self.config = None

    def get(self, key):
        return self.config.get(key)

    def set(self, key, value):
        self.config[key] = value


# Test 1: Defaults should work
handler1 = ConfigHandler()
assert handler1.get('debug') == False
assert handler1.get('timeout') == 30

# Test 2: Custom config should override
handler2 = ConfigHandler({'debug': True, 'timeout': 60})
assert handler2.get('debug') == True
assert handler2.get('timeout') == 60
assert handler2.get('retries') == 3  # Default preserved

# Test 3: Modifications should not affect DEFAULT_CONFIG
handler1.set('debug', True)
handler1.config['endpoints'].append('backup.example.com')

assert ConfigHandler.DEFAULT_CONFIG['debug'] == False, "DEFAULT_CONFIG should be unchanged"
assert ConfigHandler.DEFAULT_CONFIG['endpoints'] == ['api.example.com'], "DEFAULT_CONFIG endpoints should be unchanged"

# Test 4: Different instances should be independent
handler3 = ConfigHandler()
assert handler3.get('debug') == False, "New instance should have fresh defaults"
assert handler3.get('endpoints') == ['api.example.com'], "New instance should have original endpoints"

print("✓ Exercise 8 passed: Safe Config Handler")


# =============================================================================
# All exercises completed!
# =============================================================================
print("\n" + "=" * 60)
print("🎉 Congratulations! All Chapter 6 exercises passed!")
print("=" * 60)
