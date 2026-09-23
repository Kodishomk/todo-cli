"""
Expense Tracker (OOP)
---------------------
A command-line expense tracker built with Object-Oriented Programming (OOP).
Uses an Expense class to encapsulate single expense items and a Tracker class
to manage collections, aggregate metrics, and handle JSON file persistence.
"""

from datetime import datetime
import json
import os

FILENAME = "expenses.json"


class Expense:
    """Represents a single real-life financial expense record."""

    def __init__(self, amount: float, category: str, description: str, date: str | None = None) -> None:
        self.amount = float(amount)
        self.category = category.strip().capitalize()
        self.description = description.strip()
        # Default to current date (YYYY-MM-DD) if none supplied
        self.date = date if date else datetime.now().strftime("%Y-%m-%d")

    def to_dict(self) -> dict:
        """Serializes the Expense object into a dictionary for JSON output."""
        return {
            "amount": self.amount,
            "category": self.category,
            "description": self.description,
            "date": self.date,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Expense":
        """Factory method to instantiate a real Expense object from a dictionary."""
        return cls(
            amount=data["amount"],
            category=data["category"],
            description=data["description"],
            date=data.get("date"),
        )


class Tracker:
    """Manages a collection of Expense objects and handles disk persistence."""

    def __init__(self, filepath: str = FILENAME) -> None:
        self.filepath = filepath
        self.expenses: list[Expense] = []
        self.load_from_file()

    def add_expense(self, expense: Expense) -> None:
        """Appends an Expense object to the tracker and saves to file."""
        self.expenses.append(expense)
        self.save_to_file()

    def get_all_expenses(self) -> list[Expense]:
        """Returns the list of all tracked Expense objects."""
        return self.expenses

    def total_by_category(self) -> dict[str, float]:
        """Calculates total spending grouped by category."""
        breakdown: dict[str, float] = {}
        for exp in self.expenses:
            breakdown[exp.category] = breakdown.get(exp.category, 0.0) + exp.amount
        return breakdown

    def delete_expense(self, index: int) -> Expense | None:
        """Deletes an expense by 1-based index and saves changes."""
        if 1 <= index <= len(self.expenses):
            removed = self.expenses.pop(index - 1)
            self.save_to_file()
            return removed
        return None

    def save_to_file(self) -> None:
        """Serializes all Expense objects to JSON format."""
        data = [exp.to_dict() for exp in self.expenses]
        with open(self.filepath, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    def load_from_file(self) -> None:
        """Hydrates raw JSON dictionaries into real Expense objects on startup."""
        if not os.path.exists(self.filepath):
            self.expenses = []
            return

        try:
            with open(self.filepath, "r", encoding="utf-8") as file:
                raw_data = json.load(file)
                self.expenses = [Expense.from_dict(item) for item in raw_data]
        except (json.JSONDecodeError, OSError):
            self.expenses = []


# --- CLI INTERFACE & VALIDATION HELPERS ---


def get_float_input(prompt: str) -> float:
    """Ensures input is a valid positive number."""
    while True:
        try:
            val = float(input(prompt).strip())
            if val <= 0:
                print("Error: Amount must be greater than zero.")
                continue
            return val
        except ValueError:
            print("Error: Please enter a valid number (e.g. 12.50).")


def get_non_empty_string(prompt: str) -> str:
    """Ensures input is non-empty."""
    while True:
        val = input(prompt).strip()
        if val:
            return val
        print("Error: Field cannot be left blank.")


def get_optional_date(prompt: str) -> str:
    """Validates YYYY-MM-DD date or defaults to today if left blank."""
    while True:
        val = input(prompt).strip()
        if not val:
            return datetime.now().strftime("%Y-%m-%d")
        try:
            parsed_date = datetime.strptime(val, "%Y-%m-%d")
            return parsed_date.strftime("%Y-%m-%d")
        except ValueError:
            print("Error: Invalid date format. Please use YYYY-MM-DD or leave blank for today.")


def main() -> None:
    """Main program flow."""
    tracker = Tracker()

    while True:
        print("\n=== EXPENSE TRACKER (OOP) ===")
        print("1. Add expense")
        print("2. View all expenses")
        print("3. View total by category")
        print("4. Delete expense")
        print("5. Quit")

        choice = input("\nChoose an option (1-5): ").strip()

        if choice == "1":
            print("\n--- Add Expense ---")
            amount = get_float_input("Enter amount ($): ")
            category = get_non_empty_string("Enter category (e.g. Food, Transport): ")
            description = get_non_empty_string("Enter description: ")
            date_str = get_optional_date("Enter date (YYYY-MM-DD) or press Enter for today: ")

            # Construct real Expense object & pass to tracker
            expense = Expense(amount, category, description, date_str)
            tracker.add_expense(expense)
            print(f"Added: ${expense.amount:.2f} - {expense.category} ({expense.description}) on {expense.date}")

        elif choice == "2":
            print("\n--- All Expenses ---")
            expenses = tracker.get_all_expenses()
            if not expenses:
                print("No expenses recorded yet.")
            else:
                for idx, exp in enumerate(expenses, 1):
                    print(f"[{idx}] ${exp.amount:.2f} - {exp.category} - {exp.description} - {exp.date}")

        elif choice == "3":
            print("\n--- Total by Category ---")
            totals = tracker.total_by_category()
            if not totals:
                print("No expenses recorded yet.")
            else:
                grand_total = 0.0
                for cat, total in totals.items():
                    print(f"• {cat}: ${total:.2f}")
                    grand_total += total
                print(f"\nGrand Total: ${grand_total:.2f}")

        elif choice == "4":
            print("\n--- Delete Expense ---")
            expenses = tracker.get_all_expenses()
            if not expenses:
                print("No expenses available to delete.")
                continue

            for idx, exp in enumerate(expenses, 1):
                print(f"[{idx}] ${exp.amount:.2f} - {exp.category} - {exp.description}")

            try:
                num = int(input("\nEnter expense number to delete: ").strip())
                deleted = tracker.delete_expense(num)
                if deleted:
                    print(f"Successfully deleted: ${deleted.amount:.2f} - {deleted.description}")
                else:
                    print(f"Error: Expense #{num} does not exist.")
            except ValueError:
                print("Error: Please enter a valid number.")

        elif choice == "5":
            print("Goodbye!")
            break

        else:
            print("Error: Invalid option. Please enter a number between 1 and 5.")


if __name__ == "__main__":
    main()