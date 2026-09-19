import json
import random
from pathlib import Path


class QuestionManager:
    def __init__(self, question_file, questions_per_game=10):
        self.question_file = Path(question_file)
        self.questions_per_game = questions_per_game

        self.questions = []
        self.current_index = 0

        self._load_questions()

    def _load_questions(self):
        with self.question_file.open("r", encoding="utf-8") as file:
            self.questions = json.load(file)

        if len(self.questions) < self.questions_per_game:
            raise ValueError(
                f"Question bank contains only {len(self.questions)} questions. "
                f"At least {self.questions_per_game} are required."
            )

    def start_game(self):
        selected_questions = random.sample(
            self.questions,
            self.questions_per_game
        )

        self.current_index = 0

        self.active_questions = []

        for question in selected_questions:
            question = question.copy()

            # Randomize which option appears at the top/bottom.
            if random.choice([True, False]):
                question["top"] = question["option_a"]
                question["bottom"] = question["option_b"]
                question["correct_direction"] = (
                    "UP" if question["correct"] == "A" else "DOWN"
                )
            else:
                question["top"] = question["option_b"]
                question["bottom"] = question["option_a"]
                question["correct_direction"] = (
                    "UP" if question["correct"] == "B" else "DOWN"
                )

            self.active_questions.append(question)

    def get_current_question(self):
        if self.current_index >= len(self.active_questions):
            return None

        return self.active_questions[self.current_index]

    def next_question(self):
        self.current_index += 1

        return self.get_current_question()

    def is_finished(self):
        return self.current_index >= len(self.active_questions)

    def get_question_number(self):
        return self.current_index + 1