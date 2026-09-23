"""
Automated File Organizer
------------------------
Scans a designated target folder, sorts loose files into categorical subfolders
based on file extensions, safely handles duplicate filenames, and uses a custom
decorator to log all operations with timestamps.
"""

import functools
import os
from datetime import datetime
from pathlib import Path
import shutil

# Configuration: Mapping file extensions to categorical folder names
EXTENSION_MAP = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"],
    "Documents": [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".csv", ".pptx"],
    "Audio": [".mp3", ".wav", ".aac", ".flac", ".m4a"],
    "Video": [".mp4", ".mkv", ".mov", ".avi"],
    "Archives": [".zip", ".tar", ".gz", ".7z", ".rar"],
    "Code": [".py", ".js", ".html", ".css", ".json", ".sql"],
}

LOG_FILE = "log.txt"


def log_action(func):
    """
    Decorator: Intercepts the move_file function to record timestamped
    log entries into log.txt without polluting core file-movement logic.
    """

    @functools.wraps(func)
    def wrapper(src_path: Path, dest_folder: Path) -> Path:
        dest_path = func(src_path, dest_folder)

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] Moved '{src_path.name}' -> {dest_folder.name}/{dest_path.name}\n"

        with open(LOG_FILE, "a", encoding="utf-8") as file:
            file.write(log_entry)

        return dest_path

    return wrapper


def get_category(extension: str) -> str:
    """Matches a file extension against EXTENSION_MAP to determine target folder."""
    ext = extension.lower()
    for category, extensions in EXTENSION_MAP.items():
        if ext in extensions:
            return category
    return "Other"


def resolve_duplicate_name(dest_folder: Path, filename: str) -> Path:
    """
    Prevents overwriting existing files by appending a numeric counter
    (e.g. photo(1).jpg) if a file with the same name exists at destination.
    """
    target = dest_folder / filename
    if not target.exists():
        return target

    stem = Path(filename).stem
    suffix = Path(filename).suffix
    counter = 1

    while True:
        new_filename = f"{stem}({counter}){suffix}"
        target = dest_folder / new_filename
        if not target.exists():
            return target
        counter += 1


@log_action
def move_file(src_path: Path, dest_folder: Path) -> Path:
    """
    Core function to move a file to its destination directory.
    Decorated with @log_action to automatically write to log.txt.
    """
    dest_folder.mkdir(parents=True, exist_ok=True)
    final_dest_path = resolve_duplicate_name(dest_folder, src_path.name)
    shutil.move(str(src_path), str(final_dest_path))
    return final_dest_path


def organize_folder(target_dir: str | Path) -> dict[str, int]:
    """Scans target directory for loose files and sorts them into subfolders."""
    target_path = Path(target_dir).resolve()

    if not target_path.exists() or not target_path.is_dir():
        raise FileNotFoundError(f"Directory '{target_path}' does not exist.")

    summary: dict[str, int] = {}
    total_moved = 0

    # Retrieve loose files sitting directly inside target folder (ignore subfolders)
    items = [item for item in target_path.iterdir() if item.is_file() and item.name != LOG_FILE]

    for file_path in items:
        category = get_category(file_path.suffix)
        dest_folder = target_path / category

        move_file(file_path, dest_folder)

        summary[category] = summary.get(category, 0) + 1
        total_moved += 1

    summary["_total"] = total_moved
    return summary


def create_test_environment(test_dir: Path) -> None:
    """Creates a dummy test directory filled with mock files for safe testing."""
    test_dir.mkdir(exist_ok=True)
    dummy_files = [
        "sample_photo.jpg",
        "notes.txt",
        "document.pdf",
        "song.mp3",
        "script.py",
        "unknown_file.xyz",
        "sample_photo.jpg",  # Intentionally duplicated to test collision renaming
    ]
    for name in dummy_files:
        (test_dir / name).write_text(f"Dummy content for {name}", encoding="utf-8")
    print(f"Created temporary test folder '{test_dir.name}' with {len(dummy_files)} dummy files.")


def main() -> None:
    """Main execution loop."""
    print("==========================================")
    print("        AUTOMATED FILE ORGANIZER          ")
    print("==========================================")

    test_folder = Path("messy_folder")

    # Prompt user to prepare or organize messy_folder
    if not test_folder.exists():
        print(f"\nNo '{test_folder}' directory detected.")
        choice = input("Would you like to automatically create 'messy_folder' with dummy files to test? (y/n): ").strip().lower()
        if choice == "y":
            create_test_environment(test_folder)
        else:
            print("Please create a target folder and try again. Exiting.")
            return

    input(f"\nPress Enter to organize files inside '{test_folder.name}'...")

    summary = organize_folder(test_folder)
    total_files = summary.pop("_total", 0)

    print("\n==========================================")
    print("           ORGANIZATION COMPLETE          ")
    print("==========================================")
    print(f"Total files organized: {total_files}")
    if summary:
        print("\nBreakdown by category:")
        for category, count in summary.items():
            print(f"  • {category}: {count} file(s)")

    print(f"\nAll operations logged to '{LOG_FILE}'.")


if __name__ == "__main__":
    main()