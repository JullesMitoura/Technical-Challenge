# Challenge 02: Orders Report

> ⚠️ **AI tools are not recommended.** The goal is not to get everything right, but to demonstrate general knowledge of Python and data processing.

## Objective

Complete the `report.py` file by implementing two functions that read a CSV file of orders and build a sales summary. All other files are already provided. Only the Python standard library is needed for the solution.

## Project Structure

| File | Description |
| --- | --- |
| `report.py` | ⚡ **Your focus**: loading and summarizing orders (file to be completed) |
| `parsing.py` | Row parsing and validation function |
| `models.py` | Dataclasses: `Order` and `Summary` |
| `orders.csv` | Sample data, including some invalid rows |
| `test_report.py` | Automated tests to check your solution |
| `requirements.txt` | Project dependencies |

## Functions

### `load_orders(path: str | Path) -> list[Order]`

Reads the CSV file at `path` and returns one `Order` per valid row, in file order.

- Each row must be converted with `parse_order` from `parsing.py`
- `parse_order` raises `ValueError` for invalid rows: those rows must be skipped, not crash the program
- If the file does not exist, let `FileNotFoundError` propagate

With the provided `orders.csv` (12 rows, 4 of them invalid):

```python
orders = load_orders("orders.csv")
len(orders)  # 8
orders[0]    # Order(order_id=1, customer='Ana', category='books', amount=35.5, created_at=datetime.date(2026, 1, 5))
```

### `summarize(orders: list[Order]) -> Summary`

Builds a `Summary` from a list of orders:

| Field | Rule |
| --- | --- |
| `total_orders` | Number of orders |
| `total_revenue` | Sum of all amounts, rounded to 2 decimal places |
| `revenue_by_category` | Sum of amounts per category, each rounded to 2 decimal places |
| `top_customer` | Customer with the highest total amount. On a tie, the first name in alphabetical order. `None` if there are no orders |

With the provided `orders.csv`:

```python
summarize(load_orders("orders.csv"))
# Summary(
#     total_orders=8,
#     total_revenue=634.04,
#     revenue_by_category={'books': 89.75, 'electronics': 288.9, 'games': 255.39},
#     top_customer='Ana',
# )
```

## Requirements

- Python 3.10 or newer
- Import and use the dataclasses already defined in `models.py`
- Import and use the parsing function from `parsing.py`
- Do not modify `parsing.py`, `models.py`, `orders.csv` or `test_report.py`
- Do not add third-party libraries (no pandas): the standard library is enough

## How to run

```bash
cd challenge-02-orders-report
pip install -r requirements.txt
pytest
```

The tests stop with an import error until both functions exist in `report.py`. The goal is to make all of them pass.

## What will be evaluated

- Correctness of both functions (the tests are a starting point, not the whole evaluation)
- Proper use of the provided dataclasses and parsing function
- File handling and error handling
- Code clarity and organization
- Basic Python best practices (type hints, naming)
