from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class Order:
    order_id: int
    customer: str
    category: str
    amount: float
    created_at: date


@dataclass(frozen=True)
class Summary:
    total_orders: int
    total_revenue: float
    revenue_by_category: dict[str, float]
    top_customer: str | None
