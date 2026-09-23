"""
Quiz App Entry Point
--------------------
Runs the command-line interface, handles user input validation, and displays results.
"""

import sys
from quiz import Quiz


def get_valid_choice() -> str:
    """Prompts the user until a valid letter (A, B, C, or D) is entered."""
    valid_options = {"A", "B", "C", "D"}
    while True:
        choice = input("\nYour answer (A-D): ").strip().upper()
        if choice in valid_options:
            return choice
        print("Invalid choice. Please enter A, B, C, or D.")


def main() -> None:
    """Main execution loop."""
    print("==========================================")
    print("       WELCOME TO THE PYTHON QUIZ APP     ")
    print("==========================================")

    try:
        quiz = Quiz("questions.json")
    except (FileNotFoundError, ValueError) as err:
        print(err)
        sys.exit(1)

    if not quiz.questions:
        print("No questions found in questions.json. Exiting.")
        sys.exit(1)

    # Question Loop
    for index, q in enumerate(quiz.questions, 1):
        print(f"\nQuestion {index}/{len(quiz.questions)}:")
        print(q.text)
        for option in q.options:
            print(f"  {option}")

        user_choice = get_valid_choice()
        is_right = quiz.evaluate_answer(q, user_choice)

        if is_right:
            print("Correct!")
        else:
            print("Incorrect.")

    # Final Score & Summary
    print("\n==========================================")
    print("              QUIZ COMPLETE               ")
    print("==========================================")
    total = len(quiz.questions)
    percentage = (quiz.score / total) * 100
    print(f"Final Score: {quiz.score}/{total} ({percentage:.1f}%)")

    if quiz.missed_questions:
        print("\n--- Review Missed Questions ---")
        for q, wrong_ans in quiz.missed_questions:
            print(f"\n• {q.text}")
            print(f"  Your answer:    {wrong_ans}")
            print(f"  Correct answer: {q.answer}")
    else:
        print("\nPerfect score! Excellent work!")


if __name__ == "__main__":
    main()