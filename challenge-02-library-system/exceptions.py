class LibraryError(Exception):
    """Base class for every error raised by the library."""


class DuplicateItemError(LibraryError):
    """An item with the same id is already in the catalog."""


class ItemNotFoundError(LibraryError):
    """No item with the given id exists in the catalog."""


class ItemUnavailableError(LibraryError):
    """The item cannot be borrowed by this member right now."""


class LoanLimitError(LibraryError):
    """The member already has the maximum number of active loans."""


class NotOnLoanError(LibraryError):
    """The item is not currently on loan, so it cannot be returned."""
