from collections.abc import Callable
from dataclasses import dataclass

DEFAULT_TAX_RATE = 0.10


@dataclass
class Item:
    sku: str
    name: str
    price: float
    quantity: int = 1


def build_discounts(rates: dict[str, float]) -> dict[str, Callable[[float], float]]:
    """Map each discount code to a function that applies its own rate to a price.

    Example: build_discounts({"WELCOME10": 0.10})["WELCOME10"](200.0) returns 180.0
    """
    discounts: dict[str, Callable[[float], float]] = {}
    for code, rate in rates.items():
        discounts[code] = lambda price: price * (1 - rate)
    return discounts


class Cart:
    def __init__(self, owner: str, items: list[Item] = []) -> None:
        """Create a cart for `owner`. A cart created without items starts empty."""
        self.owner = owner
        self.items = items

    def add(self, item: Item) -> None:
        """Add an item. If its SKU is already in the cart, increase the quantity."""
        for existing in self.items:
            if existing.sku == item.sku:
                existing.quantity += item.quantity
                return
        self.items.append(item)

    def remove_empty(self) -> None:
        """Remove every item whose quantity is zero."""
        for item in self.items:
            if item.quantity == 0:
                self.items.remove(item)

    def subtotal(self) -> float:
        """Sum of price times quantity for every item."""
        return sum((item.price * item.quantity for item in self.items), start=0.0)

    def total(self, tax_rate: float | None = None) -> float:
        """Subtotal plus tax. Uses DEFAULT_TAX_RATE only when no tax rate is given."""
        rate = tax_rate or DEFAULT_TAX_RATE
        return self.subtotal() * (1 + rate)

    def clone(self, owner: str) -> "Cart":
        """Return a copy of this cart for another owner.

        The copy is independent: changing one cart never affects the other.
        """
        return Cart(owner, self.items.copy())

    def summary(self) -> dict[str, int]:
        """Describe the items in stock (quantity greater than zero).

        Returns "units" (sum of their quantities) and "lines" (how many
        distinct items they are).
        """
        in_stock = (item for item in self.items if item.quantity > 0)
        units = sum(item.quantity for item in in_stock)
        lines = len(list(in_stock))
        return {"units": units, "lines": lines}
