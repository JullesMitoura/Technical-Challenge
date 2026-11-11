import pytest

from cart import DEFAULT_TAX_RATE, Cart, Item, build_discounts


def make_cart(*items: Item) -> Cart:
    return Cart("ana", list(items))


# Cart creation and add


def test_new_carts_start_empty() -> None:
    first = Cart("ana")
    first.add(Item("A-1", "Notebook", 10.0))

    second = Cart("bruno")

    assert second.items == []


def test_add_appends_new_item() -> None:
    cart = make_cart(Item("A-1", "Notebook", 10.0))

    cart.add(Item("B-2", "Pen", 2.5))

    assert [item.sku for item in cart.items] == ["A-1", "B-2"]


def test_add_merges_quantity_for_same_sku() -> None:
    cart = make_cart(Item("A-1", "Notebook", 10.0, quantity=2))

    cart.add(Item("A-1", "Notebook", 10.0, quantity=3))

    assert len(cart.items) == 1
    assert cart.items[0].quantity == 5


# remove_empty


def test_remove_empty_keeps_items_in_stock() -> None:
    cart = make_cart(
        Item("A-1", "Notebook", 10.0, quantity=0),
        Item("B-2", "Pen", 2.5, quantity=4),
        Item("C-3", "Eraser", 1.0, quantity=0),
    )

    cart.remove_empty()

    assert [item.sku for item in cart.items] == ["B-2"]


def test_remove_empty_removes_every_zero_quantity_item() -> None:
    cart = make_cart(
        Item("A-1", "Notebook", 10.0, quantity=0),
        Item("B-2", "Pen", 2.5, quantity=0),
        Item("C-3", "Eraser", 1.0, quantity=4),
    )

    cart.remove_empty()

    assert [item.sku for item in cart.items] == ["C-3"]


# subtotal and total


def test_subtotal() -> None:
    cart = make_cart(
        Item("A-1", "Notebook", 10.0, quantity=2),
        Item("B-2", "Pen", 2.5, quantity=4),
    )

    assert cart.subtotal() == pytest.approx(30.0)


def test_total_uses_default_tax_rate() -> None:
    cart = make_cart(Item("A-1", "Notebook", 10.0, quantity=2))

    assert cart.total() == pytest.approx(20.0 * (1 + DEFAULT_TAX_RATE))


def test_total_with_custom_tax_rate() -> None:
    cart = make_cart(Item("A-1", "Notebook", 10.0, quantity=2))

    assert cart.total(tax_rate=0.25) == pytest.approx(25.0)


def test_total_with_zero_tax_rate() -> None:
    cart = make_cart(Item("A-1", "Notebook", 10.0, quantity=2))

    assert cart.total(tax_rate=0.0) == pytest.approx(20.0)


# build_discounts


def test_single_discount() -> None:
    discounts = build_discounts({"WELCOME10": 0.10})

    assert discounts["WELCOME10"](200.0) == pytest.approx(180.0)


def test_each_discount_uses_its_own_rate() -> None:
    discounts = build_discounts({"WELCOME10": 0.10, "VIP30": 0.30})

    assert discounts["WELCOME10"](200.0) == pytest.approx(180.0)
    assert discounts["VIP30"](200.0) == pytest.approx(140.0)


# clone


def test_clone_new_items_do_not_reach_original() -> None:
    original = make_cart(Item("A-1", "Notebook", 10.0))

    copy = original.clone("bruno")
    copy.add(Item("B-2", "Pen", 2.5))

    assert copy.owner == "bruno"
    assert [item.sku for item in copy.items] == ["A-1", "B-2"]
    assert [item.sku for item in original.items] == ["A-1"]


def test_clone_quantity_changes_do_not_reach_original() -> None:
    original = make_cart(Item("A-1", "Notebook", 10.0, quantity=1))

    copy = original.clone("bruno")
    copy.add(Item("A-1", "Notebook", 10.0, quantity=4))

    assert copy.items[0].quantity == 5
    assert original.items[0].quantity == 1


# summary


def test_summary_counts_units_in_stock() -> None:
    cart = make_cart(
        Item("A-1", "Notebook", 10.0, quantity=2),
        Item("B-2", "Pen", 2.5, quantity=0),
        Item("C-3", "Eraser", 1.0, quantity=3),
    )

    assert cart.summary()["units"] == 5


def test_summary_counts_lines_in_stock() -> None:
    cart = make_cart(
        Item("A-1", "Notebook", 10.0, quantity=2),
        Item("B-2", "Pen", 2.5, quantity=0),
        Item("C-3", "Eraser", 1.0, quantity=3),
    )

    assert cart.summary()["lines"] == 2
