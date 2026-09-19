class ScoreManager:

    def __init__(self, points_per_correct=10):

        self.points_per_correct = points_per_correct

        self.score = 0
        self.correct_answers = 0
        self.total_questions = 0

        self.answer_history = []


    def reset(self):

        self.score = 0
        self.correct_answers = 0
        self.total_questions = 0

        self.answer_history = []


    def record_answer(
        self,
        correct,
        question=None,
        selected_direction=None,
        result=None
    ):

        self.total_questions += 1

        if correct:

            self.score += self.points_per_correct

            self.correct_answers += 1


        # ---------------------------------------------
        # ANSWER HISTORY
        # ---------------------------------------------

        if question:

            self.answer_history.append({

                "question_number":
                    self.total_questions,

                "question_id":
                    question.get("id"),

                "category":
                    question.get("category"),

                "top":
                    question.get("top"),

                "bottom":
                    question.get("bottom"),

                "correct_direction":
                    question.get(
                        "correct_direction"
                    ),

                "selected_direction":
                    selected_direction,

                "result":
                    result,

                "correct_answer":
                    (
                        question.get("top")
                        if question.get(
                            "correct_direction"
                        ) == "UP"
                        else question.get("bottom")
                    )

            })


    def get_score(self):

        return self.score