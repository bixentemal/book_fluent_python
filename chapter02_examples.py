# Container sequences : list, tuple, and collections.deque.

## Mutable sequences
## For example, list, bytearray, array.array, and collections.deque.

## Immutable sequences
## For example, tuple, str, and bytes.

# flat sequences : str, bytes, bytearray, memoryview, and array.array.

# List Comprehensions and Readability
symbols = '$¢£¥€¤'
codes = [ord(symbol) for symbol in symbols]
print(codes)


# Local Scope Within Comprehensions and Generator Expressions
x = 'ABC'
codes = [ord(x) for x in x]
print(x)

print(codes)

codes = [last := ord(c) for c in x]
print(last)

# Generator Expressions
# saves memory because it yields items
# one by one using the iterator protoco
# Genexps use the same syntax as listcomps, but are enclosed in parentheses rather
# than brackets.

symbols = '$¢£¥€¤'
print(tuple(ord(symbol) for symbol in symbols))
import array
print(array.array('I', (ord(symbol) for symbol in symbols)))

# Unpacking Sequences and Iterables
a, b, *rest = range(5)
print(a, b, rest)
print(a, b, *rest)

# Pattern Matching with Sequences
metro_areas = [
('Tokyo', 'JP', 36.933, (35.689722, 139.691667)),
('Delhi NCR', 'IN', 21.935, (28.613889, 77.208889)),
('Mexico City', 'MX', 20.142, (19.433333,-99.133333)),
('New York-Newark', 'US', 20.104, (40.808611,-74.020386)),
('São Paulo', 'BR', 19.649, (-23.547778,-46.635833)),]
def main():
    print(f'{"":15} | {"latitude":>9} | {"longitude":>9}')
for record in metro_areas:
    match record:
        case [name, _, _, (lat, lon)] if lon <= 0:
            print(f'{name:15} | {lat:9.4f} | {lon:9.4f}')

# Slicing
l = [10, 20, 30, 40, 50, 60]
print(l[:2]) # split at 2
print(l[2:])
print(l[:3]) # split at 3
print(l[3:])

# Slice Objects seq[start:stop:step]
# Python calls seq.__getitem__(slice(start, stop, step)).
s = 'bicycle'
print(s[::3])
print(s[::-1])
print(s[::-2])

# The list.sort method sorts a list in place

# When a List Is Not the Answer
# If a list only contains numbers, an array.array is a more efficient replacement.
'''
>>> from array import array
>>> from random import random
>>> floats = array('d', (random() for i in range(10**7)))
>>> floats[-1]
0.07802343889111107
>>> fp = open('floats.bin', 'wb')
>>> floats.tofile(fp)
>>> fp.close()
>>> floats2 = array('d')
>>> fp = open('floats.bin', 'rb')
>>> floats2.fromfile(fp, 10**7)
>>> fp.close()
>>> floats2[-1]
0.07802343889111107
>>> floats2 == floats
True
'''

# Memory Views

# A memoryview is essentially a generalized NumPy array structure in Python itself
# (without the math). It allows you to share memory between data-structures (things like
# PIL images, SQLite databases, NumPy arrays, etc.) without first copying. This is very
# important for large data sets.

# Using notation similar to the array module, the memoryview.cast method lets you
# change the way multiple bytes are read or written as units without moving bits
# around. memoryview.cast returns yet another memoryview object, always sharing the
# same memory.
# Build array of 6 bytes (typecode 'B').
'''
>>> from array import array
>>> octets = array('B', range(6))
62 | Chapter 2: An Array of Sequences
>>> m1 = memoryview(octets)
>>> m1.tolist()
[0, 1, 2, 3, 4, 5]
>>> m2 = m1.cast('B', [2, 3])
>>> m2.tolist()
[[0, 1, 2], [3, 4, 5]]
>>> m3 = m1.cast('B', [3, 2])
>>> m3.tolist()
[[0, 1], [2, 3], [4, 5]]
>>> m2[1,1] = 22
>>> m3[1,1] = 33
>>> octets
array('B', [0, 1, 2, 33, 22, 5])
'''

# Example 2-21. Changing the value of a 16-bit integer array item by poking one of its
# bytes
# Build memoryview from array of 5 16-bit signed integers (typecode 'h').
# memv sees the same 5 items in the array.
# Create memv_oct by casting the elements of memv to bytes (typecode 'B').
# Export elements of memv_oct as a list of 10 bytes, for inspection.
# Assign value 4 to byte offset 5.
# Note the change to numbers: a 4 in the most significant byte of a 2-byte unsigned
# integer is 1024.
'''
>>> numbers = array.array('h', [-2,
>>> memv = memoryview(numbers)
>>> len(memv)
5
>>> memv[0]
-2
>>> memv_oct = memv.cast('B')
>>> memv_oct.tolist()
[254, 255, 255, 255, 0, 0, 1, 0, 2, 0]
>>> memv_oct[5] = 4
>>> numbers
array('h', [-2, -1, 1024, 1, 2])
'''

# Deques and Other Queues
'''
Example 2-23. Working with a deque
>>> from collections import deque
>>> dq = deque(range(10), maxlen=10)
>>> dq
deque([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], maxlen=10)
>>> dq.rotate(3)
>>> dq
deque([7, 8, 9, 0, 1, 2, 3, 4, 5, 6], maxlen=10)
>>> dq.rotate(-4)
>>> dq
deque([1, 2, 3, 4, 5, 6, 7, 8, 9, 0], maxlen=10)
>>> dq.appendleft(-1)
>>> dq
deque([-1, 1, 2, 3, 4, 5, 6, 7, 8, 9], maxlen=10)
>>> dq.extend([11, 22, 33])
>>> dq
deque([3, 4, 5, 6, 7, 8, 9, 11, 22, 33], maxlen=10)
>>> dq.extendleft([10, 20, 30, 40])
>>> dq
deque([40, 30, 20, 10, 3, 4, 5, 6, 7, 8], maxlen=10)
'''

# Besides deque, other Python standard library packages implement queues:
# queue
# This provides the synchronized (i.e., thread-safe) classes SimpleQueue, Queue,
# LifoQueue, and PriorityQueue. These can be used for safe communication
# between threads. All except SimpleQueue can be bounded by providing a max
# size argument greater than 0 to the constructor. However, they don’t discard
# items to make room as deque does. Instead, when the queue is full, the insertion
# of a new item blocks—i.e., it waits until some other thread makes room by taking
# an item from the queue, which is useful to throttle the number of live threads.
# multiprocessing
# Implements its own unbounded SimpleQueue and bounded Queue, very similar
# to those in the queue package, but designed for interprocess communication. A
# specialized multiprocessing.JoinableQueue is provided for task management.
# asyncio
# Provides Queue, LifoQueue, PriorityQueue, and JoinableQueue with APIs
# inspired by the classes in the queue and multiprocessing modules, but adapted
# for managing tasks in asynchronous programming.
# heapq
# In contrast to the previous three modules, heapq does not implement a queue
# class, but provides functions like heappush and heappop that let you use a muta‐
# ble sequence as a heap queue or priority queue.