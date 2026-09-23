"""
Book Model
----------
Defines the Book class encapsulating title, author, availability status,
and current borrower details.
"""


class Book:
    """Represents an individual book in the library collection."""

    def __init__(
        self,
        title: str,
        author: str,
        is_available: bool = True,
        borrower: str | None = None,
    ) -> None:
        self.title = title.strip()
        self.author = author.strip()
        self.is_available = is_available
        self.borrower = borrower.strip() if borrower else None

    def check_out(self, borrower_name: str) -> bool:
        """Marks the book as checked out to a specific borrower."""
        if not self.is_available:
            return False
        self.is_available = False
        self.borrower = borrower_name.strip()
        return True

    def return_book(self) -> bool:
        """Clears the borrower and marks the book as available."""
        if self.is_available:
            return False
        self.is_available = True
        self.borrower = None
        return True

    def to_dict(self) -> dict:
        """Serializes the Book instance into a dictionary for JSON output."""
        return {
            "title": self.title,
            "author": self.author,
            "is_available": self.is_available,
            "borrower": self.borrower,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Book":
        """Factory method to instantiate a Book object from a dictionary."""
        return cls(
            title=data["title"],
            author=data["author"],
            is_available=data.get("is_available", True),
            borrower=data.get("borrower"),
        )