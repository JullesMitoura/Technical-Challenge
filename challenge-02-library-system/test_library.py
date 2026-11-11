from datetime import date

import pytest

from exceptions import (
    DuplicateItemError,
    ItemNotFoundError,
    ItemUnavailableError,
    LoanLimitError,
    NotOnLoanError,
)
from library import Book, Library, Magazine
from models import LibraryItem, Loan, Member

TODAY = date(2026, 3, 2)

ANA = Member(1, "Ana")
BRUNO = Member(2, "Bruno")
CARLA = Member(3, "Carla")


@pytest.fixture
def library() -> Library:
    library = Library()
    library.add_item(Book("B1", "Refactoring", "Martin Fowler"))
    library.add_item(Book("B2", "Clean Code", "Robert C. Martin"))
    library.add_item(Book("B3", "Fluent Python", "Luciano Ramalho"))
    library.add_item(Book("B4", "Domain-Driven Design", "Eric Evans"))
    library.add_item(Magazine("M1", "Wired", 42))
    return library


# Item types


def test_book() -> None:
    book = Book("B1", "Refactoring", "Martin Fowler")

    assert isinstance(book, LibraryItem)
    assert (book.item_id, book.title, book.author) == ("B1", "Refactoring", "Martin Fowler")
    assert book.loan_days == 14
    assert book.describe() == "Refactoring, by Martin Fowler"


def test_magazine() -> None:
    magazine = Magazine("M1", "Wired", 42)

    assert isinstance(magazine, LibraryItem)
    assert (magazine.item_id, magazine.title, magazine.issue) == ("M1", "Wired", 42)
    assert magazine.loan_days == 7
    assert magazine.describe() == "Wired #42"


# Catalog


def test_len_and_contains(library: Library) -> None:
    assert len(Library()) == 0
    assert len(library) == 5
    assert "B1" in library
    assert "X9" not in library


def test_add_duplicate_id_raises(library: Library) -> None:
    with pytest.raises(DuplicateItemError):
        library.add_item(Magazine("B1", "Another Title", 1))

    assert len(library) == 5


# borrow


def test_borrow_book_returns_loan(library: Library) -> None:
    loan = library.borrow("B1", ANA, TODAY)

    assert isinstance(loan, Loan)
    assert loan.item.item_id == "B1"
    assert loan.member == ANA
    assert loan.due_date == date(2026, 3, 16)


def test_borrow_magazine_has_shorter_due_date(library: Library) -> None:
    loan = library.borrow("M1", ANA, TODAY)

    assert loan.due_date == date(2026, 3, 9)


def test_borrow_unknown_item_raises(library: Library) -> None:
    with pytest.raises(ItemNotFoundError):
        library.borrow("X9", ANA, TODAY)


def test_borrow_item_on_loan_raises(library: Library) -> None:
    library.borrow("B1", ANA, TODAY)

    with pytest.raises(ItemUnavailableError):
        library.borrow("B1", BRUNO, TODAY)


def test_borrow_above_limit_raises(library: Library) -> None:
    library.borrow("B1", ANA, TODAY)
    library.borrow("B2", ANA, TODAY)
    library.borrow("B3", ANA, TODAY)

    with pytest.raises(LoanLimitError):
        library.borrow("B4", ANA, TODAY)


def test_loan_limit_is_per_member(library: Library) -> None:
    library.borrow("B1", ANA, TODAY)
    library.borrow("B2", ANA, TODAY)
    library.borrow("B3", ANA, TODAY)

    loan = library.borrow("B4", BRUNO, TODAY)

    assert loan.member == BRUNO


# return_item


def test_return_on_time_returns_zero(library: Library) -> None:
    library.borrow("B1", ANA, TODAY)

    assert library.return_item("B1", date(2026, 3, 16)) == 0


def test_return_late_returns_days_late(library: Library) -> None:
    library.borrow("B1", ANA, TODAY)

    assert library.return_item("B1", date(2026, 3, 21)) == 5


def test_returned_item_can_be_borrowed_again(library: Library) -> None:
    library.borrow("B1", ANA, TODAY)
    library.return_item("B1", date(2026, 3, 5))

    loan = library.borrow("B1", BRUNO, date(2026, 3, 5))

    assert loan.member == BRUNO
    assert loan.due_date == date(2026, 3, 19)


def test_return_frees_a_loan_slot(library: Library) -> None:
    library.borrow("B1", ANA, TODAY)
    library.borrow("B2", ANA, TODAY)
    library.borrow("B3", ANA, TODAY)
    library.return_item("B2", TODAY)

    loan = library.borrow("B4", ANA, TODAY)

    assert loan.item.item_id == "B4"


def test_return_item_not_on_loan_raises(library: Library) -> None:
    with pytest.raises(NotOnLoanError):
        library.return_item("B1", TODAY)


def test_return_unknown_item_raises(library: Library) -> None:
    with pytest.raises(ItemNotFoundError):
        library.return_item("X9", TODAY)


# reserve


def test_reserved_item_goes_to_members_in_line_order(library: Library) -> None:
    library.borrow("B1", ANA, TODAY)
    library.reserve("B1", BRUNO)
    library.reserve("B1", CARLA)
    library.return_item("B1", TODAY)

    with pytest.raises(ItemUnavailableError):
        library.borrow("B1", CARLA, TODAY)
    with pytest.raises(ItemUnavailableError):
        library.borrow("B1", ANA, TODAY)

    assert library.borrow("B1", BRUNO, TODAY).member == BRUNO
    library.return_item("B1", TODAY)
    assert library.borrow("B1", CARLA, TODAY).member == CARLA
    library.return_item("B1", TODAY)
    assert library.borrow("B1", ANA, TODAY).member == ANA


def test_reserving_twice_keeps_the_original_position(library: Library) -> None:
    library.borrow("B1", ANA, TODAY)
    library.reserve("B1", BRUNO)
    library.reserve("B1", CARLA)
    library.reserve("B1", BRUNO)
    library.return_item("B1", TODAY)

    assert library.borrow("B1", BRUNO, TODAY).member == BRUNO
    library.return_item("B1", TODAY)
    assert library.borrow("B1", CARLA, TODAY).member == CARLA
    library.return_item("B1", TODAY)
    assert library.borrow("B1", ANA, TODAY).member == ANA


def test_reservations_are_per_item(library: Library) -> None:
    library.reserve("B1", BRUNO)

    assert library.borrow("B2", ANA, TODAY).member == ANA


def test_reserve_unknown_item_raises(library: Library) -> None:
    with pytest.raises(ItemNotFoundError):
        library.reserve("X9", ANA)


# Queries


def test_available_items_are_sorted_by_title(library: Library) -> None:
    library.borrow("B2", ANA, TODAY)

    titles = [item.title for item in library.available_items()]

    assert titles == ["Domain-Driven Design", "Fluent Python", "Refactoring", "Wired"]


def test_loans_of_member_in_borrowing_order(library: Library) -> None:
    library.borrow("B3", ANA, TODAY)
    library.borrow("B1", BRUNO, TODAY)
    library.borrow("M1", ANA, TODAY)

    assert [loan.item.item_id for loan in library.loans_of(ANA)] == ["B3", "M1"]
    assert [loan.item.item_id for loan in library.loans_of(BRUNO)] == ["B1"]
    assert library.loans_of(CARLA) == []


def test_loans_of_member_ignores_returned_items(library: Library) -> None:
    library.borrow("B3", ANA, TODAY)
    library.borrow("M1", ANA, TODAY)
    library.return_item("B3", TODAY)

    assert [loan.item.item_id for loan in library.loans_of(ANA)] == ["M1"]
