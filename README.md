# Fluent Python - Study Notes & Exercises

A hands-on learning repository for **Fluent Python (2nd Edition)** by Luciano Ramalho.

## Overview

This repository contains:
- **Markdown memos** (`chapterNN_topic.md`) - Concise summaries of key concepts
- **Exercise files** (`chapterNN_topic.py`) - Practice problems with TODO placeholders

## Chapter Index

### Part I: Data Structures
| Ch | Topic | Memo | Exercises |
|----|-------|------|-----------|
| 01 | The Python Data Model | [memo](chapter01_python_data_model.md) | [exercises](chapter01_python_data_model.py) |
| 02 | An Array of Sequences | [memo](chapter02_array_of_sequences.md) | [exercises](chapter02_array_of_sequences.py) |
| 03 | Dictionaries and Sets | [memo](chapter03_dictionaries_and_sets.md) | [exercises](chapter03_dictionaries_and_sets.py) |
| 04 | Unicode Text Versus Bytes | [memo](chapter04_unicode_text_versus_bytes.md) | [exercises](chapter04_unicode_text_versus_bytes.py) |
| 05 | Data Class Builders | [memo](chapter05_data_class_builders.md) | [exercises](chapter05_data_class_builders.py) |

### Part II: Functions as Objects
| Ch | Topic | Memo | Exercises |
|----|-------|------|-----------|
| 06 | Object References, Mutability, and Recycling | [memo](chapter06_object_references_mutability.md) | [exercises](chapter06_object_references_mutability.py) |
| 07 | Functions as First-Class Objects | [memo](chapter07_functions_first_class_objects.md) | [exercises](chapter07_functions_first_class_objects.py) |
| 08 | Type Hints in Functions | [memo](chapter08_type_hints_in_functions.md) | [exercises](chapter08_type_hints_in_functions.py) |
| 09 | Decorators and Closures | [memo](chapter09_decorators_and_closures.md) | [exercises](chapter09_decorators_and_closures.py) |
| 10 | Design Patterns with First-Class Functions | [memo](chapter10_design_patterns_with_first_class_functions.md) | [exercises](chapter10_design_patterns_with_first_class_functions.py) |

### Part III: Classes and Protocols
| Ch | Topic | Memo | Exercises |
|----|-------|------|-----------|
| 11 | A Pythonic Object | [memo](chapter11_a_pythonic_object.md) | [exercises](chapter11_a_pythonic_object.py) |
| 12 | Special Methods for Sequences | [memo](chapter12_special_methods_for_sequences.md) | [exercises](chapter12_special_methods_for_sequences.py) |
| 13 | Interfaces, Protocols, and ABCs | [memo](chapter13_interfaces_protocols_and_abcs.md) | [exercises](chapter13_interfaces_protocols_and_abcs.py) |
| 14 | Inheritance: For Better or for Worse | [memo](chapter14_inheritance.md) | [exercises](chapter14_inheritance.py) |
| 15 | More About Type Hints | [memo](chapter15_more_about_type_hints.md) | [exercises](chapter15_more_about_type_hints.py) |

### Part IV: Control Flow
| Ch | Topic | Memo | Exercises |
|----|-------|------|-----------|
| 16 | Operator Overloading | [memo](chapter16_operator_overloading.md) | [exercises](chapter16_operator_overloading.py) |
| 17 | Iterators, Generators, and Classic Coroutines | [memo](chapter17_iterators_generators_classic_coroutines.md) | [exercises](chapter17_iterators_generators_classic_coroutines.py) |
| 18 | with, match, and else Blocks | [memo](chapter18_with_match_and_else_blocks.md) | [exercises](chapter18_with_match_and_else_blocks.py) |
| 19 | Concurrency Models in Python | [memo](chapter19_concurrency_models_in_python.md) | [exercises](chapter19_concurrency_models_in_python.py) |
| 20 | Concurrent Executors | [memo](chapter20_concurrent_executors.md) | [exercises](chapter20_concurrent_executors.py) |
| 21 | Asynchronous Programming | [memo](chapter21_asynchronous_programming.md) | [exercises](chapter21_asynchronous_programming.py) |

### Part V: Metaprogramming
| Ch | Topic | Memo | Exercises |
|----|-------|------|-----------|
| 22 | Dynamic Attributes and Properties | [memo](chapter22_dynamic_attributes_and_properties.md) | [exercises](chapter22_dynamic_attributes_and_properties.py) |
| 23 | Attribute Descriptors | [memo](chapter23_attribute_descriptors.md) | [exercises](chapter23_attribute_descriptors.py) |
| 24 | Class Metaprogramming | [memo](chapter24_class_metaprogramming.md) | [exercises](chapter24_class_metaprogramming.py) |

## Usage

### Running Exercises

Each exercise file contains TODO placeholders. Fill in the implementations and run:

```bash
# Run a specific chapter
python chapter01_python_data_model.py

# Run all exercises
python run_all.py
```

Passing exercises print checkmarks; all tests pass shows "Congratulations!" at the end.

### Exercise Pattern

```python
# =============================================================================
# Exercise N: Topic
# =============================================================================
# Description of what to implement

def some_function():
    # TODO: Implement this
    pass

# Test
assert some_function() == expected
print("    Exercise N passed")
```

## Requirements

- Python 3.12+ (some exercises use modern syntax)
- No external dependencies for most chapters
- `httpx` recommended for Chapter 21 (async HTTP)

## Structure

```
.
├── README.md                    # This file
├── CLAUDE.md                    # AI assistant instructions
├── pyproject.toml               # Project configuration
├── run_all.py                   # Test runner for all exercises
├── chapter01_*.md / .py         # Chapter 1 materials
├── chapter02_*.md / .py         # Chapter 2 materials
└── ...                          # Chapters 3-24
```

## License

This is a personal study repository. The book "Fluent Python" is copyrighted by Luciano Ramalho / O'Reilly Media.
