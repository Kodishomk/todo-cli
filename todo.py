"""
To-Do List CLI (File-Saved)
---------------------------
A persistent command-line task manager that reads from and writes to a local file,
allowing tasks to remain saved across program restarts.
"""

import os

FILENAME = "tasks.txt"


def load_tasks(filepath: str) -> list[dict[str, str | bool]]:
    """Loads tasks from a text file into memory.

    Each line in the file is stored as: Status|Task Description
    Status: 'DONE' or 'PENDING'
    """
    tasks = []
    if not os.path.exists(filepath):
        return tasks

    with open(filepath, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            parts = line.split("|", 1)
            if len(parts) == 2:
                status, title = parts
                tasks.append({"title": title, "done": status == "DONE"})
    return tasks


def save_tasks(filepath: str, tasks: list[dict[str, str | bool]]) -> None:
    """Saves current in-memory tasks to the text file immediately."""
    with open(filepath, "w", encoding="utf-8") as file:
        for task in tasks:
            status = "DONE" if task["done"] else "PENDING"
            file.write(f"{status}|{task['title']}\n")


def display_tasks(tasks: list[dict[str, str | bool]]) -> None:
    """Displays all current tasks with line numbers and status indicators."""
    print("\n--- YOUR TASKS ---")
    if not tasks:
        print("No tasks found. Your list is empty!")
        return

    for index, task in enumerate(tasks, 1):
        status = "[X]" if task["done"] else "[ ]"
        print(f"{index}. {status} {task['title']}")


def get_task_index(prompt: str, max_index: int) -> int | None:
    """Prompts for a task number and validates it against current list range."""
    user_input = input(prompt).strip()
    try:
        idx = int(user_input)
        if 1 <= idx <= max_index:
            return idx - 1  # Convert 1-based display to 0-based index
        print(f"Error: Task number {idx} does not exist. Please enter a number between 1 and {max_index}.")
    except ValueError:
        print("Error: Invalid input. Please enter a valid task number.")
    return None


def main() -> None:
    """Main application loop managing task operations."""
    tasks = load_tasks(FILENAME)

    while True:
        print("\n=== TO-DO LIST CLI ===")
        print("1. Add task")
        print("2. View tasks")
        print("3. Complete task")
        print("4. Delete task")
        print("5. Quit")

        choice = input("\nChoose an option (1-5): ").strip()

        if choice == "1":
            new_task = input("Enter task: ").strip()
            if new_task:
                tasks.append({"title": new_task, "done": False})
                save_tasks(FILENAME, tasks)
                print("Task added.")
            else:
                print("Error: Task description cannot be empty.")

        elif choice == "2":
            display_tasks(tasks)

        elif choice == "3":
            if not tasks:
                print("\nNo tasks available to complete.")
            else:
                display_tasks(tasks)
                idx = get_task_index("Enter task number to complete: ", len(tasks))
                if idx is not None:
                    tasks[idx]["done"] = True
                    save_tasks(FILENAME, tasks)
                    print(f"Task {idx + 1} marked as complete.")

        elif choice == "4":
            if not tasks:
                print("\nNo tasks available to delete.")
            else:
                display_tasks(tasks)
                idx = get_task_index("Enter task number to delete: ", len(tasks))
                if idx is not None:
                    removed = tasks.pop(idx)
                    save_tasks(FILENAME, tasks)
                    print(f"Task deleted: '{removed['title']}'")

        elif choice == "5":
            print("Goodbye!")
            break

        else:
            print("Error: Invalid option. Please enter a number between 1 and 5.")


if __name__ == "__main__":
    main()