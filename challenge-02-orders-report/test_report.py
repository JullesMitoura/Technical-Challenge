from datetime import date
from pathlib import Path

import pytest

from models import Order, Summary
from report import load_orders, summarize

DATA_FILE = Path(__file__).parent / "orders.csv"
HEADER = "order_id,customer,category,amount,created_at\n"


def make_order(order_id: int, customer: str, category: str, amount: float) -> Order:
    return Order(
        order_id=order_id,
        customer=customer,
        category=category,
        amount=amount,
        created_at=date(2026, 1, 1),
    )


def test_load_orders_skips_invalid_rows() -> None:
    orders = load_orders(DATA_FILE)

    assert [order.order_id for order in orders] == [1, 2, 3, 4, 6, 9, 11, 12]


def test_load_orders_returns_parsed_orders() -> None:
    orders = load_orders(DATA_FILE)

    assert orders[0] == Order(
        order_id=1,
        customer="Ana",
        category="books",
        amount=35.5,
        created_at=date(2026, 1, 5),
    )
    assert orders[3].category == "books"


def test_load_orders_accepts_string_path() -> None:
    assert len(load_orders(str(DATA_FILE))) == 8


def test_load_orders_with_only_header_returns_empty_list(tmp_path: Path) -> None:
    csv_file = tmp_path / "empty.csv"
    csv_file.write_text(HEADER, encoding="utf-8")

    assert load_orders(csv_file) == []


def test_load_orders_missing_file_raises(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        load_orders(tmp_path / "does_not_exist.csv")


def test_summarize_sample_file() -> None:
    summary = summarize(load_orders(DATA_FILE))

    assert summary == Summary(
        total_orders=8,
        total_revenue=634.04,
        revenue_by_category={
            "books": 89.75,
            "electronics": 288.9,
            "games": 255.39,
        },
        top_customer="Ana",
    )


def test_summarize_empty_list() -> None:
    assert summarize([]) == Summary(
        total_orders=0,
        total_revenue=0.0,
        revenue_by_category={},
        top_customer=None,
    )


def test_summarize_rounds_to_two_decimals() -> None:
    orders = [
        make_order(1, "Ana", "books", 0.1),
        make_order(2, "Ana", "books", 0.2),
    ]

    summary = summarize(orders)

    assert summary.total_revenue == 0.3
    assert summary.revenue_by_category == {"books": 0.3}


def test_summarize_top_customer_uses_total_revenue() -> None:
    orders = [
        make_order(1, "Bruno", "games", 100.0),
        make_order(2, "Ana", "books", 60.0),
        make_order(3, "Ana", "games", 60.0),
    ]

    assert summarize(orders).top_customer == "Ana"


def test_summarize_top_customer_tie_is_alphabetical() -> None:
    orders = [
        make_order(1, "Carla", "games", 50.0),
        make_order(2, "Bruno", "books", 50.0),
    ]

    assert summarize(orders).top_customer == "Bruno"
