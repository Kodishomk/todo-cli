"""
Library Controller
------------------
Manages the collection of Book objects, handles checkouts/returns,
and controls JSON file persistence.
"""

import json
import os
from book import Book

FILENAME = "library.json"


class Library:
    """Manages library inventory, checkouts, returns, and persistence."""

    def __init__(self, filepath: str = FILENAME) -> None:
        self.filepath = filepath
        self.books: list[Book] = []
        self.load_from_file()

    def add_book(self, title: str, author: str) -> Book:
        """Creates a new Book object, adds it to inventory, and saves to file."""
        book = Book(title, author)
        self.books.append(book)
        self.save_to_file()
        return book

    def get_all_books(self) -> list[Book]:
        """Returns the full list of tracked books."""
        return self.books

    def find_book(self, title: str) -> Book | None:
        """Case-insensitive lookup for a book by title."""
        target_title = title.strip().lower()
        for book in self.books:
            if book.title.lower() == target_title:
                return book
        return None

    def check_out_book(self, title: str, borrower_name: str) -> tuple[bool, str]:
        """
        Attempts to check out a book by title to a borrower.
        Returns (success_status, descriptive_message).
        """
        book = self.find_book(title)
        if not book:
            return False, f"Error: '{title}' was not found in the library catalog."

        if not book.is_available:
            return False, f"Error: '{book.title}' is already checked out by {book.borrower}."

        book.check_out(borrower_name)
        self.save_to_file()
        return True, f"Success: '{book.title}' has been checked out to {borrower_name}."

    def return_book(self, title: str) -> tuple[bool, str]:
        """
        Attempts to return a checked-out book by title.
        Returns (success_status, descriptive_message).
        """
        book = self.find_book(title)
        if not book:
            return False, f"Error: '{title}' was not found in the library catalog."

        if book.is_available:
            return False, f"Notice: '{book.title}' is already in the library (not checked out)."

        book.return_book()
        self.save_to_file()
        return True, f"Success: '{book.title}' has been returned and is now available."

    def get_borrower_info(self, title: str) -> tuple[bool, str]:
        """Returns current borrower information or availability status for a book."""
        book = self.find_book(title)
        if not book:
            return False, f"Error: '{title}' was not found in the library catalog."

        if book.is_available:
            return True, f"'{book.title}' is currently AVAILABLE."
        return True, f"'{book.title}' is currently CHECKED OUT by {book.borrower}."

    def save_to_file(self) -> None:
        """Serializes all Book objects to JSON format and writes to disk."""
        data = [book.to_dict() for book in self.books]
        with open(self.filepath, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    def load_from_file(self) -> None:
        """Hydrates raw JSON objects back into real Book instances on startup."""
        if not os.path.exists(self.filepath):
            self.books = []
            return

        try:
            with open(self.filepath, "r", encoding="utf-8") as file:
                raw_data = json.load(file)
                self.books = [Book.from_dict(item) for item in raw_data]
        except (json.JSONDecodeError, OSError):
            self.books = []