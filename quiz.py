"""
Quiz Controller
---------------
Defines the Quiz class which manages loading questions, scoring, and tracking missed items.
"""

import json
import os
from question import Question


class Quiz:
    """Manages the quiz execution, score tracking, and question collection."""

    def __init__(self, filepath: str = "questions.json") -> None:
        self.filepath = filepath
        self.questions: list[Question] = []
        self.score: int = 0
        self.missed_questions: list[tuple[Question, str]] = []  # Stores (Question, UserChoice)
        self.load_questions()

    def load_questions(self) -> None:
        """Loads questions from JSON and hydrates them into Question objects."""
        if not os.path.exists(self.filepath):
            raise FileNotFoundError(f"Error: Question data file '{self.filepath}' not found.")

        try:
            with open(self.filepath, "r", encoding="utf-8") as file:
                data = json.load(file)
                self.questions = [Question.from_dict(item) for item in data]
        except (json.JSONDecodeError, KeyError) as err:
            raise ValueError(f"Error: Invalid JSON format in '{self.filepath}': {err}")

    def evaluate_answer(self, question: Question, user_choice: str) -> bool:
        """Evaluates an answer and updates score or missed list."""
        if question.is_correct(user_choice):
            self.score += 1
            return True
        else:
            self.missed_questions.append((question, user_choice.upper()))
            return False