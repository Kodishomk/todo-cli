"""
Main Entry Point
----------------
Handles user menu rendering, option routing, and input prompting.
All operational logic delegates directly to the Library class.
"""

import sys
from library import Library


def get_non_empty_input(prompt: str) -> str:
    """Helper function to enforce non-blank user input."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Error: Field cannot be left blank.")


def main() -> None:
    """Main CLI program loop."""
    library = Library()

    while True:
        print("\n=== LIBRARY MANAGEMENT SYSTEM ===")
        print("1. Add book")
        print("2. View all books")
        print("3. Check out a book")
        print("4. Return a book")
        print("5. View who has a book")
        print("6. Quit")

        choice = input("\nChoose an option (1-6): ").strip()

        if choice == "1":
            print("\n--- Add Book ---")
            title = get_non_empty_input("Enter book title: ")
            author = get_non_empty_input("Enter author name: ")
            new_book = library.add_book(title, author)
            print(f"Added: '{new_book.title}' by {new_book.author}")

        elif choice == "2":
            print("\n--- Catalog ---")
            books = library.get_all_books()
            if not books:
                print("No books in the library catalog yet.")
            else:
                for idx, book in enumerate(books, 1):
                    status = "Available" if book.is_available else f"Checked out by {book.borrower}"
                    print(f"[{idx}] '{book.title}' by {book.author} — Status: {status}")

        elif choice == "3":
            print("\n--- Check Out Book ---")
            title = get_non_empty_input("Enter book title to check out: ")
            borrower = get_non_empty_input("Enter borrower's name: ")
            success, message = library.check_out_book(title, borrower)
            print(message)

        elif choice == "4":
            print("\n--- Return Book ---")
            title = get_non_empty_input("Enter book title to return: ")
            success, message = library.return_book(title)
            print(message)

        elif choice == "5":
            print("\n--- Borrower Lookup ---")
            title = get_non_empty_input("Enter book title to check: ")
            success, message = library.get_borrower_info(title)
            print(message)

        elif choice == "6":
            print("Goodbye!")
            sys.exit(0)

        else:
            print("Error: Invalid option. Please enter a number between 1 and 6.")


if __name__ == "__main__":
    main()