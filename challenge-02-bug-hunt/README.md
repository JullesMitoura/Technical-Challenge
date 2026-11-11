# Challenge 02: Bug Hunt

> ⚠️ **AI tools are not recommended.** The goal is not to get everything right, but to demonstrate that you can read Python code and understand how the language behaves.

## Objective

The `cart.py` file implements a small shopping cart. It runs without errors, but it contains **6 bugs**. Find them, fix them and explain each one in `NOTES.md`.

No new code needs to be written from scratch, and no library solves this for you: every bug comes from how Python itself works.

## Project Structure

| File | Description |
| --- | --- |
| `cart.py` | ⚡ **Your focus**: shopping cart module (file to be fixed) |
| `NOTES.md` | ⚡ **Your focus**: your explanation of each bug (file to be filled in) |
| `test_cart.py` | Automated tests that describe the expected behavior |
| `requirements.txt` | Project dependencies |

## What the code should do

The docstrings in `cart.py` are correct: they describe the intended behavior. The code is what is wrong.

| Function or method | Intended behavior |
| --- | --- |
| `build_discounts(rates)` | Maps each discount code to a function that applies its own rate to a price |
| `Cart(owner, items)` | Creates a cart. Without `items`, the cart starts empty |
| `Cart.add(item)` | Adds an item, or increases the quantity if the SKU is already in the cart |
| `Cart.remove_empty()` | Removes every item whose quantity is zero |
| `Cart.subtotal()` | Sum of price times quantity |
| `Cart.total(tax_rate)` | Subtotal plus tax. Uses the default rate only when no rate is given |
| `Cart.clone(owner)` | Returns an independent copy of the cart for another owner |
| `Cart.summary()` | Units and number of distinct items in stock |

## The tests

`test_cart.py` has 15 tests. At the start, **9 pass and 6 fail**: each failing test exposes one of the bugs.

```bash
cd challenge-02-bug-hunt
pip install -r requirements.txt
pytest
```

A failing test shows you a symptom. Your job is to find the cause.

## Requirements

- Python 3.10 or newer
- Fix the bugs in `cart.py` so that all 15 tests pass
- Fill in `NOTES.md` with the root cause and the fix for each bug
- Do not modify `test_cart.py`
- Keep the public interface of `cart.py`: same names, same parameters
- Do not add third-party libraries

## What will be evaluated

- Your explanations in `NOTES.md`: understanding why each bug happens matters more than making the test pass
- Quality of each fix: it should solve the cause, not work around the test
- All tests passing, including the ones that already passed
- Code clarity and basic Python best practices (type hints, naming)
