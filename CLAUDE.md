# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a learning repository for **Fluent Python (2nd Edition)** by Luciano Ramalho. It contains chapter notes and hands-on exercises for practicing Python concepts from the book.

## Structure

- `chapterN_Topic_Name.md` - Markdown memos summarizing key concepts from each chapter
- `chapterN_topic_name.py` - Exercise files with TODO placeholders for the reader to complete
- `chapterN.py` - Simple code examples/notes from reading the book

The book is available via `muextract` (MinerU PDF extraction tool) configured globally. Use `muextract extract` to pull content from specific chapters.

## Running Exercises

```bash
# Run a specific chapter's exercises
python chapter1_python_data_model.py

# Exercises use assertions - passing means all checks succeeded
# Look for "✓ Exercise N passed" output and final "Congratulations!" message
```

## Exercise File Pattern

Exercise files follow a consistent structure:
1. Each exercise is a numbered section with a class or function to implement
2. Replace `None`, `...`, or `pass` placeholders with working code
3. Assertions after each exercise validate the implementation
4. The file is meant to be run directly to check all solutions

## Python Version

Requires Python 3.14+ (see pyproject.toml).

## External Tool

`muextract` - CLI tool for extracting content from the Fluent Python PDF:
- `muextract info` - Show chapters, page counts, content types
- `muextract extract --chapter "Chapter Name"` - Extract specific chapter content
- `muextract status` - Show current configuration
