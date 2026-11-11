import math
from datetime import date

from models import Order


def parse_order(row: dict[str, str]) -> Order:
    """Convert a raw CSV row into an Order.

    Raises ValueError when the row is invalid: missing fields, wrong types,
    empty customer or category, or an amount that is not a positive number.
    """
    try:
        order = Order(
            order_id=int(row["order_id"]),
            customer=row["customer"].strip(),
            category=row["category"].strip().lower(),
            amount=float(row["amount"]),
            created_at=date.fromisoformat(row["created_at"].strip()),
        )
    except (KeyError, TypeError, AttributeError) as error:
        raise ValueError(f"Invalid row: {row}") from error

    if not order.customer or not order.category:
        raise ValueError(f"Missing customer or category: {row}")
    if not math.isfinite(order.amount) or order.amount <= 0:
        raise ValueError(f"Invalid amount: {row}")

    return order
