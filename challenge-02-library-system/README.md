# Challenge 02: Library System

> ⚠️ **AI tools are not recommended.** The goal is not to get everything right, but to demonstrate general knowledge of Python, object-oriented programming and data structures.

## Objective

Complete the `library.py` file by implementing three classes: two kinds of library items and the library that lends them. All other files are already provided.

How you store the data inside the library is up to you: choosing the right structures is part of the challenge.

## Project Structure

| File | Description |
| --- | --- |
| `library.py` | ⚡ **Your focus**: item types and the library (file to be completed) |
| `models.py` | `LibraryItem` abstract base class, `Member` and `Loan` |
| `exceptions.py` | Errors the library must raise |
| `test_library.py` | Automated tests to check your solution |
| `requirements.txt` | Project dependencies |

## Classes

### `Book` and `Magazine`

Both must inherit from `LibraryItem` and implement what the base class leaves abstract.

| Class | Constructor | `loan_days` | `describe()` |
| --- | --- | --- | --- |
| `Book` | `Book(item_id, title, author)` | `14` | `"Refactoring, by Martin Fowler"` |
| `Magazine` | `Magazine(item_id, title, issue)` | `7` | `"Wired #42"` |

`author` is a `str`, `issue` is an `int`, and both must be available as attributes.

### `Library`

| Member | Behavior |
| --- | --- |
| `Library()` | Creates an empty library |
| `add_item(item)` | Adds an item to the catalog |
| `borrow(item_id, member, today)` | Lends the item to the member and returns a `Loan` |
| `return_item(item_id, today)` | Takes the item back and returns how many days late it is |
| `reserve(item_id, member)` | Puts the member in the waiting line of the item |
| `available_items()` | Returns the items that are not on loan, sorted by title |
| `loans_of(member)` | Returns the active loans of the member, in the order they were made |
| `len(library)` | Number of items in the catalog |
| `item_id in library` | Whether the catalog has an item with that id |

### Rules

**Catalog**

- Item ids are unique: adding an id that already exists raises `DuplicateItemError`
- Any method that receives an `item_id` that is not in the catalog raises `ItemNotFoundError`

**Borrowing.** `borrow` checks these rules, in this order:

1. An item that is already on loan raises `ItemUnavailableError`
2. An item with a waiting line can only be borrowed by the first member in line: anyone else gets `ItemUnavailableError`
3. A member can have at most 3 active loans: a fourth one raises `LoanLimitError`

When the loan succeeds, its `due_date` is `today` plus the `loan_days` of the item. If the member was first in line, they leave the line.

**Returning**

- Returning an item that is not on loan raises `NotOnLoanError`
- The result is the number of days after the `due_date`, or `0` when the item is returned on time
- After the return, the item is available again and no longer counts toward the member's limit

**Reserving**

- Each item has its own waiting line, served in order of arrival
- A member who is already in the line of an item keeps their position when reserving it again

### Example

```python
from datetime import date

from library import Book, Library, Magazine
from models import Member

library = Library()
library.add_item(Book("B1", "Refactoring", "Martin Fowler"))
library.add_item(Magazine("M1", "Wired", 42))

ana, bruno = Member(1, "Ana"), Member(2, "Bruno")

loan = library.borrow("B1", ana, date(2026, 3, 2))
loan.due_date                                # date(2026, 3, 16)

library.reserve("B1", bruno)
library.return_item("B1", date(2026, 3, 21))  # 5
library.borrow("B1", ana, date(2026, 3, 21))  # raises ItemUnavailableError: Bruno is first in line

len(library)                                 # 2
"M1" in library                              # True
```

## Requirements

- Python 3.10 or newer
- Import and use the base class and the models already defined in `models.py`
- Import and use the errors already defined in `exceptions.py`
- Use only the Python standard library
- Do not modify `models.py`, `exceptions.py` or `test_library.py`

## How to run

```bash
cd challenge-02-library-system
pip install -r requirements.txt
pytest
```

The tests stop with an import error until the three classes exist in `library.py`. The goal is to make all of them pass.

## What will be evaluated

- Correctness of the three classes (the tests are a starting point, not the whole evaluation)
- Object-oriented design: inheritance, encapsulation and proper use of the provided base class
- Choice of data structures for the catalog, the loans and the waiting lines
- Error handling with the provided exceptions
- Code clarity and basic Python best practices (type hints, naming)
