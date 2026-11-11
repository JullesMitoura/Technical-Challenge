from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import date


class LibraryItem(ABC):
    """Base class for anything the library can lend."""

    def __init__(self, item_id: str, title: str) -> None:
        self.item_id = item_id
        self.title = title

    @property
    @abstractmethod
    def loan_days(self) -> int:
        """How many days this kind of item can be borrowed for."""

    @abstractmethod
    def describe(self) -> str:
        """Short text that presents the item to a reader."""

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.item_id!r}, {self.title!r})"


@dataclass(frozen=True)
class Member:
    member_id: int
    name: str


@dataclass(frozen=True)
class Loan:
    item: LibraryItem
    member: Member
    due_date: date
