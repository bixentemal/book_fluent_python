# Unicode Text Versus Bytes - Practical Memo

## The Fundamental Distinction

| Type | Contains | Immutable | Use For |
|------|----------|-----------|---------|
| `str` | Unicode characters (code points) | Yes | Human-readable text |
| `bytes` | Integers 0-255 | Yes | Binary data, encoded text |
| `bytearray` | Integers 0-255 | No | Mutable binary data |

```python
# str: sequence of Unicode characters
s = 'café'
len(s)        # 4 characters

# bytes: sequence of integers 0-255
b = b'caf\xc3\xa9'  # UTF-8 encoded
len(b)        # 5 bytes
b[0]          # 99 (integer, not 'c')
b[:1]         # b'c' (slice is still bytes)

# Conversion
s.encode('utf-8')  # str → bytes
b.decode('utf-8')  # bytes → str
```

---

## Encoding & Decoding

```
┌─────────┐   encode()   ┌─────────┐
│   str   │ ──────────►  │  bytes  │
│ (text)  │              │ (binary)│
└─────────┘  ◄────────── └─────────┘
               decode()
```

```python
text = 'café'

# Encoding (str → bytes)
text.encode('utf-8')      # b'caf\xc3\xa9'
text.encode('latin-1')    # b'caf\xe9'
text.encode('utf-16')     # b'\xff\xfec\x00a\x00f\x00\xe9\x00'

# Decoding (bytes → str)
b'caf\xc3\xa9'.decode('utf-8')    # 'café'
b'caf\xe9'.decode('latin-1')      # 'café'
```

---

## Common Encodings

| Encoding | Description | Use Case |
|----------|-------------|----------|
| `utf-8` | Variable 1-4 bytes, ASCII-compatible | **Default choice**, web, Linux/macOS |
| `utf-16` | Variable 2-4 bytes, has BOM | Windows APIs, Java, JavaScript |
| `latin-1` / `iso-8859-1` | 1 byte per char, 256 chars | Western European legacy |
| `cp1252` | Windows Latin-1 superset | Windows legacy |
| `ascii` | 7-bit, 128 chars | Subset of everything |

**Rule:** When in doubt, use UTF-8.

```python
# Check if string is pure ASCII
'hello'.isascii()   # True
'café'.isascii()    # False
```

---

## Error Handling

### Encoding Errors (str → bytes)

```python
city = 'São Paulo'

# Default: raises UnicodeEncodeError
city.encode('ascii')  # Error! 'ã' not in ASCII

# Error handlers
city.encode('ascii', errors='ignore')         # b'So Paulo' (data loss!)
city.encode('ascii', errors='replace')        # b'S?o Paulo'
city.encode('ascii', errors='xmlcharrefreplace')  # b'S&#227;o Paulo'
city.encode('ascii', errors='backslashreplace')   # b'S\\xe3o Paulo'
```

### Decoding Errors (bytes → str)

```python
data = b'Montr\xe9al'  # 'é' in latin-1

# Wrong encoding: garbage (mojibake)
data.decode('utf-8')           # UnicodeDecodeError
data.decode('koi8-r')          # 'MontrИal' (wrong!)

# Error handlers
data.decode('utf-8', errors='ignore')   # 'Montral'
data.decode('utf-8', errors='replace')  # 'Montr�al' (U+FFFD)

# Correct
data.decode('latin-1')  # 'Montréal'
```

### Practical Pattern: Try UTF-8 First

```python
def decode_safely(data: bytes) -> str:
    """Try UTF-8 first, fall back to latin-1."""
    try:
        return data.decode('utf-8')
    except UnicodeDecodeError:
        return data.decode('latin-1')  # Never fails
```

---

## The Unicode Sandwich

**Best Practice:** Decode bytes to str at input, work with str internally, encode to bytes at output.

```
Input (bytes) → Decode → [Process str] → Encode → Output (bytes)
```

### File I/O

```python
# ALWAYS specify encoding explicitly!

# Writing
with open('file.txt', 'w', encoding='utf-8') as f:
    f.write('café')

# Reading
with open('file.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Binary mode (no encoding/decoding)
with open('file.bin', 'rb') as f:
    data = f.read()  # bytes

with open('file.bin', 'wb') as f:
    f.write(b'\x00\x01\x02')
```

### Detect Encoding with chardet

```python
import chardet

with open('unknown.txt', 'rb') as f:
    raw = f.read()

detected = chardet.detect(raw)
# {'encoding': 'utf-8', 'confidence': 0.99, 'language': ''}

text = raw.decode(detected['encoding'])
```

---

## BOM (Byte Order Mark)

```python
# UTF-16 has BOM to indicate byte order
'hello'.encode('utf-16')     # b'\xff\xfeh\x00e\x00l\x00l\x00o\x00'
                              #  ^^^^^^^^ BOM (little-endian)

# Explicit byte order (no BOM)
'hello'.encode('utf-16-le')  # b'h\x00e\x00l\x00l\x00o\x00'
'hello'.encode('utf-16-be')  # b'\x00h\x00e\x00l\x00l\x00o'

# UTF-8 with BOM (for Excel compatibility)
'hello'.encode('utf-8-sig')  # b'\xef\xbb\xbfhello'

# Reading: utf-8-sig handles both with and without BOM
with open('file.txt', encoding='utf-8-sig') as f:
    text = f.read()  # BOM stripped if present
```

---

## Unicode Normalization

Same visual character can have different code point representations:

```python
s1 = 'café'           # 'é' as single char U+00E9
s2 = 'cafe\u0301'     # 'e' + combining acute accent U+0301

s1 == s2              # False!
len(s1), len(s2)      # (4, 5)

# But they look identical when printed
```

### Normalization Forms

| Form | Description | Use Case |
|------|-------------|----------|
| `NFC` | Composed (single char when possible) | **Default choice**, storage |
| `NFD` | Decomposed (base + combining chars) | Searching, text processing |
| `NFKC` | Compatibility composed | Search, comparisons |
| `NFKD` | Compatibility decomposed | Search, comparisons |

```python
from unicodedata import normalize

s1 = 'café'
s2 = 'cafe\u0301'

normalize('NFC', s1) == normalize('NFC', s2)   # True
normalize('NFD', s1) == normalize('NFD', s2)   # True

# NFC is generally preferred
len(normalize('NFC', s2))   # 4
len(normalize('NFD', s1))   # 5
```

### Practical Normalization Function

```python
from unicodedata import normalize, combining

def normalize_text(s: str) -> str:
    """Normalize to NFC form."""
    return normalize('NFC', s)

def remove_accents(s: str) -> str:
    """Remove diacritics/accents from text."""
    # Decompose, then remove combining characters
    decomposed = normalize('NFD', s)
    return ''.join(c for c in decomposed if not combining(c))

remove_accents('café')   # 'cafe'
remove_accents('naïve')  # 'naive'
```

---

## Case Folding

For case-insensitive comparisons, use `casefold()` instead of `lower()`:

```python
# lower() is not enough for some languages
'ß'.lower()      # 'ß' (unchanged)
'ß'.casefold()   # 'ss'

# Turkish dotted/dotless i
'İ'.lower()      # 'i̇' (wrong for Turkish)
'İ'.casefold()   # 'i̇'

# Safe case-insensitive comparison
def equals_ignore_case(s1: str, s2: str) -> bool:
    return normalize('NFC', s1).casefold() == normalize('NFC', s2).casefold()
```

---

## Unicode Sorting

Default `sorted()` uses code point values, which gives wrong order for non-ASCII:

```python
fruits = ['açaí', 'apple', 'banana', 'Äpfel']
sorted(fruits)
# ['apple', 'banana', 'Äpfel', 'açaí']  # Wrong! Accented chars at end
```

### Using locale

```python
import locale

locale.setlocale(locale.LC_COLLATE, 'pt_BR.UTF-8')  # Brazilian Portuguese
sorted(fruits, key=locale.strxfrm)
# ['açaí', 'apple', 'Äpfel', 'banana']
```

### Using pyuca (Pure Python, locale-independent)

```bash
pip install pyuca
```

```python
from pyuca import Collator

collator = Collator()
sorted(fruits, key=collator.sort_key)
# Correct Unicode collation order
```

---

## Unicode Database

```python
import unicodedata

# Character info
unicodedata.name('é')        # 'LATIN SMALL LETTER E WITH ACUTE'
unicodedata.category('é')    # 'Ll' (Letter, lowercase)
unicodedata.numeric('½')     # 0.5

# Lookup by name
unicodedata.lookup('GREEK SMALL LETTER ALPHA')  # 'α'
'\N{GREEK SMALL LETTER ALPHA}'                   # 'α' (in string literal)

# Category codes
# L=Letter, M=Mark, N=Number, P=Punctuation, S=Symbol, Z=Separator, C=Other
```

---

## Working with bytes

### Creating bytes

```python
# Literals
b'hello'
b'\x00\x01\x02'

# From string
'hello'.encode('utf-8')
bytes('hello', encoding='utf-8')

# From integers
bytes([72, 101, 108, 108, 111])  # b'Hello'

# From hex
bytes.fromhex('48 65 6c 6c 6f')  # b'Hello'

# Zeros
bytes(10)  # b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
```

### bytes/bytearray Methods

```python
data = b'Hello, World!'

# String-like methods work (with bytes args)
data.upper()              # b'HELLO, WORLD!'
data.replace(b'o', b'0')  # b'Hell0, W0rld!'
data.split(b', ')         # [b'Hello', b'World!']
data.startswith(b'Hello') # True

# To hex string
data.hex()                # '48656c6c6f2c20576f726c6421'
data.hex(' ')             # '48 65 6c 6c 6f 2c 20 57 6f 72 6c 64 21'

# bytearray is mutable
ba = bytearray(b'hello')
ba[0] = 72                # bytearray(b'Hello')
ba.append(33)             # bytearray(b'Hello!')
```

---

## Common Patterns

### Safe File Reading

```python
def read_text_file(path: str, encoding: str = 'utf-8') -> str:
    """Read text file with fallback encodings."""
    encodings = [encoding, 'utf-8-sig', 'latin-1']

    for enc in encodings:
        try:
            with open(path, encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue

    # Last resort: binary
    with open(path, 'rb') as f:
        return f.read().decode('latin-1')
```

### Normalize for Comparison/Storage

```python
from unicodedata import normalize

def normalize_string(s: str) -> str:
    """Normalize string for storage/comparison."""
    return normalize('NFC', s.strip())

def normalize_for_search(s: str) -> str:
    """Normalize for case-insensitive search."""
    return normalize('NFKC', s.casefold())
```

### Sanitize Filename

```python
import re
from unicodedata import normalize, combining

def sanitize_filename(name: str) -> str:
    """Convert string to safe ASCII filename."""
    # Normalize and remove accents
    name = normalize('NFD', name)
    name = ''.join(c for c in name if not combining(c))
    # Replace spaces and remove invalid chars
    name = name.replace(' ', '_')
    name = re.sub(r'[^\w\-.]', '', name)
    return name.lower()

sanitize_filename('Café Münchën.txt')  # 'cafe_munchen.txt'
```

---

## Quick Reference

| Task | Code |
|------|------|
| Encode to UTF-8 | `s.encode('utf-8')` |
| Decode from UTF-8 | `b.decode('utf-8')` |
| Check ASCII-only | `s.isascii()` |
| Normalize | `unicodedata.normalize('NFC', s)` |
| Case-insensitive | `s.casefold()` |
| Remove accents | `''.join(c for c in normalize('NFD', s) if not combining(c))` |
| Char name | `unicodedata.name(c)` |
| Char from name | `unicodedata.lookup('NAME')` or `'\N{NAME}'` |
| Open text file | `open(path, encoding='utf-8')` |
| Open binary file | `open(path, 'rb')` |
