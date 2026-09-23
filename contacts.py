"""
Contact Book (JSON)
-------------------
A persistent command-line contact management tool that serializes structured
dictionaries into a JSON file, supporting full CRUD operations and case-insensitive partial searches.
"""

import json
import os

FILENAME = "contacts.json"


def load_contacts(filepath: str) -> list[dict[str, str]]:
    """Loads contacts from a JSON file. Returns an empty list if file doesn't exist or is invalid."""
    if not os.path.exists(filepath):
        return []

    try:
        with open(filepath, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        return []


def save_contacts(filepath: str, contacts: list[dict[str, str]]) -> None:
    """Saves the current contacts list to a formatted JSON file."""
    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(contacts, file, indent=4)


def get_non_empty_input(prompt: str) -> str:
    """Prompts user repeatedly until a non-blank string is provided."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Error: Field cannot be left blank. Please try again.")


def add_contact(contacts: list[dict[str, str]]) -> None:
    """Prompts for contact details, constructs a dictionary, and appends to the list."""
    print("\n--- Add New Contact ---")
    name = get_non_empty_input("Enter Name: ")
    phone = get_non_empty_input("Enter Phone: ")
    email = get_non_empty_input("Enter Email: ")

    contact = {"name": name, "phone": phone, "email": email}
    contacts.append(contact)
    save_contacts(FILENAME, contacts)
    print(f"Contact '{name}' successfully added and saved!")


def view_contacts(contacts: list[dict[str, str]]) -> None:
    """Prints all stored contacts in a formatted layout."""
    print("\n--- All Contacts ---")
    if not contacts:
        print("No contacts found.")
        return

    for index, c in enumerate(contacts, 1):
        print(f"{index}. Name: {c['name']} | Phone: {c['phone']} | Email: {c['email']}")


def search_contacts(contacts: list[dict[str, str]]) -> None:
    """Searches contacts by partial, case-insensitive match on the name field."""
    print("\n--- Search Contacts ---")
    if not contacts:
        print("No contacts to search.")
        return

    query = input("Enter name or partial name to search: ").strip().lower()
    if not query:
        print("Error: Search query cannot be blank.")
        return

    matches = [c for c in contacts if query in c["name"].lower()]

    if matches:
        print(f"\nFound {len(matches)} matching contact(s):")
        for index, c in enumerate(matches, 1):
            print(f"{index}. Name: {c['name']} | Phone: {c['phone']} | Email: {c['email']}")
    else:
        print("No contacts found.")


def delete_contact(contacts: list[dict[str, str]]) -> None:
    """Deletes a contact by exact name match (case-insensitive)."""
    print("\n--- Delete Contact ---")
    if not contacts:
        print("No contacts to delete.")
        return

    target_name = input("Enter exact name of contact to delete: ").strip().lower()
    if not target_name:
        print("Error: Name cannot be blank.")
        return

    for index, c in enumerate(contacts):
        if c["name"].lower() == target_name:
            removed = contacts.pop(index)
            save_contacts(FILENAME, contacts)
            print(f"Contact '{removed['name']}' has been permanently deleted.")
            return

    print("Contact not found.")


def main() -> None:
    """Main execution menu loop."""
    contacts = load_contacts(FILENAME)

    while True:
        print("\n=== CONTACT BOOK (JSON) ===")
        print("1. Add contact")
        print("2. View all contacts")
        print("3. Search contacts")
        print("4. Delete contact")
        print("5. Quit")

        choice = input("\nChoose an option (1-5): ").strip()

        if choice == "1":
            add_contact(contacts)

        elif choice == "2":
            view_contacts(contacts)

        elif choice == "3":
            search_contacts(contacts)

        elif choice == "4":
            delete_contact(contacts)

        elif choice == "5":
            print("Goodbye!")
            break

        else:
            print("Error: Invalid option. Please enter a number between 1 and 5.")


if __name__ == "__main__":
    main()