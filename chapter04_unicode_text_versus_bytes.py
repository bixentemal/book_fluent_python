"""
Chapter 4: Unicode Text Versus Bytes - Exercises
=================================================

Complete each exercise by replacing the `None` or `...` placeholders.
Run this file to check your answers with the assertions.
"""

from unicodedata import normalize, name, combining, category

# =============================================================================
# Exercise 1: str vs bytes Basics
# =============================================================================
# Understand the fundamental difference between str and bytes

text = 'café'
encoded = text.encode('utf-8')

# TODO: What is the length of the string (number of characters)?
str_length = None

# TODO: What is the length of the bytes (number of bytes)?
bytes_length = None

# TODO: What is the first byte of 'encoded' (as an integer)?
first_byte = None  # Hint: encoded[0] returns an int

# TODO: What do you get when you slice bytes[:1]?
first_byte_slice = None  # Is it an int or bytes?

assert str_length == 4, "String has 4 characters"
assert bytes_length == 5, "UTF-8 encoding uses 5 bytes for 'café'"
assert first_byte == 99, "First byte is 99 (ASCII for 'c')"
assert first_byte_slice == b'c', "Slicing bytes gives bytes"
print("✓ Exercise 1 passed: str vs bytes Basics")


# =============================================================================
# Exercise 2: Encoding and Decoding
# =============================================================================
# Practice encoding strings to bytes and decoding bytes to strings

text = 'naïve'

# TODO: Encode to UTF-8
utf8_bytes = None

# TODO: Encode to Latin-1 (ISO-8859-1)
latin1_bytes = None

# TODO: Decode UTF-8 bytes back to string
decoded_text = None

# TODO: What happens with different encodings?
mystery_bytes = b'caf\xe9'  # This is 'café' in Latin-1

# Decode with the correct encoding
correct_decode = None  # Decode mystery_bytes with latin-1

assert utf8_bytes == b'na\xc3\xafve'
assert latin1_bytes == b'na\xefve'
assert decoded_text == 'naïve'
assert correct_decode == 'café'
print("✓ Exercise 2 passed: Encoding and Decoding")


# =============================================================================
# Exercise 3: Encoding Error Handling
# =============================================================================
# Handle encoding errors gracefully

text = 'São Paulo'

# TODO: Try to encode to ASCII with 'ignore' error handler
# (Characters that can't be encoded are dropped)
ignored = None

# TODO: Encode to ASCII with 'replace' error handler
# (Unencodable characters are replaced with ?)
replaced = None

# TODO: Encode to ASCII with 'xmlcharrefreplace' error handler
# (Unencodable characters become XML entities like &#227;)
xml_escaped = None

assert ignored == b'So Paulo'
assert replaced == b'S?o Paulo'
assert xml_escaped == b'S&#227;o Paulo'
print("✓ Exercise 3 passed: Encoding Error Handling")


# =============================================================================
# Exercise 4: Decoding Error Handling
# =============================================================================
# Handle decoding errors gracefully

# This is 'Montréal' encoded in Latin-1
data = b'Montr\xe9al'

# TODO: Decode with UTF-8, using 'replace' error handler
# (Invalid bytes become the replacement character U+FFFD)
with_replacement = None

# TODO: Decode with UTF-8, using 'ignore' error handler
ignored = None

# TODO: Decode correctly using Latin-1
correct = None

assert with_replacement == 'Montr�al'
assert ignored == 'Montral'
assert correct == 'Montréal'
print("✓ Exercise 4 passed: Decoding Error Handling")


# =============================================================================
# Exercise 5: Safe Decode Function
# =============================================================================
# Implement a function that tries UTF-8 first, falls back to Latin-1

def safe_decode(data: bytes) -> str:
    """
    Decode bytes to string.
    Try UTF-8 first, fall back to Latin-1 if it fails.
    Latin-1 never fails because it maps all 256 byte values.

    TODO: Implement this function
    """
    ...
    pass


# Test with UTF-8 encoded data
utf8_data = 'héllo wörld'.encode('utf-8')
assert safe_decode(utf8_data) == 'héllo wörld'

# Test with Latin-1 encoded data (not valid UTF-8)
latin1_data = b'caf\xe9'
assert safe_decode(latin1_data) == 'café'

# Test with pure ASCII (works with any encoding)
ascii_data = b'hello'
assert safe_decode(ascii_data) == 'hello'

print("✓ Exercise 5 passed: Safe Decode Function")


# =============================================================================
# Exercise 6: Unicode Normalization
# =============================================================================
# Understand and apply Unicode normalization

# Two ways to represent 'é'
e_acute = 'é'               # Single character: U+00E9
e_with_combining = 'e\u0301'  # e + combining acute accent

# TODO: Are they equal without normalization?
equal_without_norm = None  # True or False

# TODO: What are their lengths?
len_single = None
len_combining = None

# TODO: Normalize both to NFC and check equality
from unicodedata import normalize
normalized_single = None
normalized_combining = None
equal_after_nfc = None

# TODO: What is the length of e_with_combining after NFC normalization?
len_after_nfc = None

assert equal_without_norm == False
assert len_single == 1
assert len_combining == 2
assert equal_after_nfc == True
assert len_after_nfc == 1
print("✓ Exercise 6 passed: Unicode Normalization")


# =============================================================================
# Exercise 7: Remove Accents
# =============================================================================
# Implement a function to remove diacritics/accents

def remove_accents(text: str) -> str:
    """
    Remove diacritics (accents) from text.

    Steps:
    1. Normalize to NFD (decompose characters)
    2. Filter out combining characters (category starts with 'M')

    TODO: Implement this function
    Hint: Use unicodedata.combining(c) to check if c is a combining char
    """
    ...
    pass


assert remove_accents('café') == 'cafe'
assert remove_accents('naïve') == 'naive'
assert remove_accents('résumé') == 'resume'
assert remove_accents('Ångström') == 'Angstrom'
assert remove_accents('hello') == 'hello'  # No change for ASCII
print("✓ Exercise 7 passed: Remove Accents")


# =============================================================================
# Exercise 8: Case Folding
# =============================================================================
# Understand the difference between lower() and casefold()

# German sharp s
sharp_s = 'ß'

# TODO: What does lower() return?
lower_result = None

# TODO: What does casefold() return?
casefold_result = None

# TODO: Are 'STRASSE' and 'straße' equal using casefold?
word1 = 'STRASSE'
word2 = 'straße'
equal_casefold = None  # Compare using casefold()

assert lower_result == 'ß', "lower() doesn't change ß"
assert casefold_result == 'ss', "casefold() converts ß to ss"
assert equal_casefold == True
print("✓ Exercise 8 passed: Case Folding")


# =============================================================================
# Exercise 9: Case-Insensitive Comparison
# =============================================================================
# Implement a robust case-insensitive comparison function

def equals_ignore_case(s1: str, s2: str) -> bool:
    """
    Compare two strings case-insensitively.

    Steps:
    1. Normalize both strings (NFC)
    2. Apply casefold() to both
    3. Compare

    TODO: Implement this function
    """
    ...
    pass


assert equals_ignore_case('Hello', 'hello') == True
assert equals_ignore_case('CAFÉ', 'café') == True
assert equals_ignore_case('straße', 'STRASSE') == True
assert equals_ignore_case('hello', 'world') == False
print("✓ Exercise 9 passed: Case-Insensitive Comparison")


# =============================================================================
# Exercise 10: Unicode Character Information
# =============================================================================
# Use the unicodedata module to get character info

import unicodedata

# TODO: Get the Unicode name of 'é'
e_name = None  # Should be 'LATIN SMALL LETTER E WITH ACUTE'

# TODO: Get the Unicode category of 'é'
e_category = None  # Should be 'Ll' (Letter, lowercase)

# TODO: Look up a character by name
omega = None  # Look up 'GREEK SMALL LETTER OMEGA'

# TODO: Get the numeric value of '½'
half_value = None  # Should be 0.5

assert e_name == 'LATIN SMALL LETTER E WITH ACUTE'
assert e_category == 'Ll'
assert omega == 'ω'
assert half_value == 0.5
print("✓ Exercise 10 passed: Unicode Character Information")


# =============================================================================
# Exercise 11: Working with bytes
# =============================================================================
# Practice bytes operations

# TODO: Create bytes from a list of integers
# [72, 101, 108, 108, 111] should give b'Hello'
from_ints = None

# TODO: Create bytes from hex string '48656c6c6f'
from_hex = None

# TODO: Convert bytes to hex string with spaces
hello_bytes = b'Hello'
hex_string = None  # Should be '48 65 6c 6c 6f'

# TODO: Create a bytearray from b'hello' and change first byte to uppercase
mutable = None  # Create bytearray
# Modify first byte to be uppercase 'H' (ASCII 72)
...

assert from_ints == b'Hello'
assert from_hex == b'Hello'
assert hex_string == '48 65 6c 6c 6f'
assert mutable == bytearray(b'Hello')
print("✓ Exercise 11 passed: Working with bytes")


# =============================================================================
# Exercise 12: Practical - Sanitize Filename
# =============================================================================
# Create a function to convert Unicode strings to safe ASCII filenames

import re

def sanitize_filename(name: str) -> str:
    """
    Convert a Unicode string to a safe ASCII filename.

    Steps:
    1. Normalize to NFD
    2. Remove combining characters (accents)
    3. Replace spaces with underscores
    4. Remove any characters that aren't alphanumeric, underscore, hyphen, or dot
    5. Convert to lowercase

    TODO: Implement this function
    """
    ...
    pass


assert sanitize_filename('Café Münchën.txt') == 'cafe_munchen.txt'
assert sanitize_filename('résumé (final).pdf') == 'resume_final.pdf'
assert sanitize_filename('Hello World!') == 'hello_world'
assert sanitize_filename('file-name_123.txt') == 'file-name_123.txt'
print("✓ Exercise 12 passed: Sanitize Filename")


# =============================================================================
# Exercise 13: Practical - Detect and Handle BOM
# =============================================================================
# Handle files that may have a Byte Order Mark

UTF8_BOM = b'\xef\xbb\xbf'

def read_with_bom_handling(data: bytes) -> str:
    """
    Decode bytes to string, handling UTF-8 BOM if present.

    If data starts with UTF-8 BOM, decode as UTF-8 and strip BOM.
    Otherwise, decode as UTF-8 normally.

    TODO: Implement this function
    """
    ...
    pass


# Test with BOM
data_with_bom = b'\xef\xbb\xbfHello, World!'
assert read_with_bom_handling(data_with_bom) == 'Hello, World!'

# Test without BOM
data_without_bom = b'Hello, World!'
assert read_with_bom_handling(data_without_bom) == 'Hello, World!'

# Test with UTF-8 content
utf8_with_bom = b'\xef\xbb\xbfcaf\xc3\xa9'
assert read_with_bom_handling(utf8_with_bom) == 'café'

print("✓ Exercise 13 passed: Handle BOM")


# =============================================================================
# Exercise 14: Practical - Text Normalizer Class
# =============================================================================
# Create a class for normalizing text with various options

class TextNormalizer:
    """
    A configurable text normalizer.

    Options:
    - normalize_unicode: Apply NFC normalization (default True)
    - lowercase: Convert to lowercase using casefold (default False)
    - strip_accents: Remove diacritics (default False)
    - strip_whitespace: Strip leading/trailing whitespace (default True)
    """

    def __init__(self, normalize_unicode=True, lowercase=False,
                 strip_accents=False, strip_whitespace=True):
        # TODO: Store configuration
        ...
        pass

    def normalize(self, text: str) -> str:
        """
        Apply all configured normalizations to the text.

        TODO: Implement this method
        Order: strip_whitespace -> normalize_unicode -> strip_accents -> lowercase
        """
        ...
        pass


# Test basic normalizer
basic = TextNormalizer()
assert basic.normalize('  café  ') == 'café'

# Test with lowercase
lower = TextNormalizer(lowercase=True)
assert lower.normalize('HELLO') == 'hello'
assert lower.normalize('Straße') == 'strasse'

# Test with accent stripping
no_accents = TextNormalizer(strip_accents=True)
assert no_accents.normalize('café') == 'cafe'

# Test with all options
full = TextNormalizer(lowercase=True, strip_accents=True)
assert full.normalize('  CAFÉ  ') == 'cafe'

print("✓ Exercise 14 passed: Text Normalizer Class")


# =============================================================================
# Exercise 15: Practical - Character Counter by Category
# =============================================================================
# Count characters by their Unicode category

from collections import Counter

def count_by_category(text: str) -> dict:
    """
    Count characters in text by their Unicode general category.

    Return a dict mapping category codes to counts.
    Use unicodedata.category() to get the category of each character.

    Categories:
    - 'Lu': Letter, uppercase
    - 'Ll': Letter, lowercase
    - 'Nd': Number, decimal digit
    - 'Zs': Separator, space
    - 'Po': Punctuation, other
    - etc.

    TODO: Implement this function
    """
    ...
    pass


text = "Hello, World! 123"
counts = count_by_category(text)

assert counts['Lu'] == 2, "2 uppercase letters: H, W"
assert counts['Ll'] == 8, "8 lowercase letters"
assert counts['Nd'] == 3, "3 digits: 1, 2, 3"
assert counts['Zs'] == 2, "2 spaces"
assert counts['Po'] == 2, "2 punctuation: comma and exclamation"

print("✓ Exercise 15 passed: Character Counter by Category")


# =============================================================================
# All exercises completed!
# =============================================================================
print("\n" + "=" * 60)
print("🎉 Congratulations! All Chapter 4 exercises passed!")
print("=" * 60)
