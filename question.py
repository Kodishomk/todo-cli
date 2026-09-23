"""
Question Model
--------------
Defines the Question class encapsulating a single quiz item.
"""


class Question:
    """Represents an individual multiple-choice question."""

    def __init__(self, text: str, options: list[str], answer: str) -> None:
        self.text = text
        self.options = options
        self.answer = answer.strip().upper()

    def is_correct(self, user_answer: str) -> bool:
        """Compares user input against the stored correct answer."""
        return user_answer.strip().upper() == self.answer

    @classmethod
    def from_dict(cls, data: dict) -> "Question":
        """Factory method to hydrate a Question instance from a dictionary."""
        return cls(
            text=data["text"],
            options=data["options"],
            answer=data["answer"],
        )