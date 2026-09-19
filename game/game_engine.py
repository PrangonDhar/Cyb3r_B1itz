import time

from game.question_manager import QuestionManager
from game.scoring import ScoreManager
from game.timer import GameTimer, QuestionTimer


class GameEngine:

    def __init__(
        self,
        question_file,
        questions_per_game=10,
        question_time_seconds=4.0,
        points_per_correct=10
        
    ):

        # =====================================================
        # CONFIGURATION
        # =====================================================

        self.questions_per_game = questions_per_game
        self.question_time = question_time_seconds
        self.points_per_correct = points_per_correct

        # =====================================================
        # GAME COMPONENTS
        # =====================================================

        self.question_manager = QuestionManager(
            question_file,
            self.questions_per_game
        )

        self.score_manager = ScoreManager(
            self.points_per_correct
        )

        self.game_timer = GameTimer()

        self.question_timer = QuestionTimer(
            self.question_time
        )

        # =====================================================
        # GAME STATE
        # =====================================================

        self.running = False
        self.game_finished = False
        self.player_name = None
        self.player_id = None

        self.last_result = None

    def set_player(self, player_name, player_id):

        self.player_name = player_name
        self.player_id = player_id
    # =========================================================
    # START GAME
    # =========================================================

    def start_game(self):

        self.question_manager.start_game()

        self.score_manager.reset()

        self.game_timer.start()

        self.question_timer.start()

        self.running = True
        self.game_finished = False

        self.last_result = None


    # =========================================================
    # GET CURRENT GAME STATE
    # =========================================================

    def get_state(self):

        question = (
            self.question_manager.get_current_question()
        )

        # -----------------------------------------------------
        # No active question
        # -----------------------------------------------------

        if question is None:

            return {
                "running": False,
                "finished": True,
                "score": self.score_manager.get_score()
            }

        # -----------------------------------------------------
        # Active question
        # -----------------------------------------------------

        return {

            "running": self.running,

            "finished": self.game_finished,

            "question_number":
                self.question_manager.get_question_number(),

            "total_questions":
                self.questions_per_game,

            "id":
                question["id"],

            "category":
                question["category"],

            "top":
                question["top"],

            "bottom":
                question["bottom"],

            "score":
                self.score_manager.get_score(),

            "remaining":
                round(
                    self.question_timer.remaining(),
                    3
                ),

            "duration":
                self.question_time
        }


    # =========================================================
    # SUBMIT PLAYER DIRECTION
    # =========================================================

    def submit_direction(self, direction):

        if not self.running:
            return None

        # -----------------------------------------------------
        # Check timeout first
        # -----------------------------------------------------

        if self.question_timer.expired():

            self.handle_timeout()

            return {
                "result": "TIMEOUT",
                "score": self.score_manager.get_score()
            }

        # -----------------------------------------------------
        # Get current question
        # -----------------------------------------------------

        question = (
            self.question_manager.get_current_question()
        )

        if question is None:

            return None

        # -----------------------------------------------------
        # Check answer
        # -----------------------------------------------------

        correct_direction = (
            question["correct_direction"]
        )

        correct = (
            direction == correct_direction
        )

        # -----------------------------------------------------
        # Result
        # -----------------------------------------------------

        if correct:

            result = "CORRECT"

        else:

            result = "WRONG"


        # -----------------------------------------------------
        # Record answer history
        # -----------------------------------------------------

        self.score_manager.record_answer(
            correct=correct,
            question=question,
            selected_direction=direction,
            result=result
        )



        # -----------------------------------------------------
        # Move to next question
        # -----------------------------------------------------

        self._next_question()

        return {

            "result": result,

            "score":
                self.score_manager.get_score()
        }


    # =========================================================
    # HANDLE TIMEOUT
    # =========================================================

    def handle_timeout(self):

        if not self.running:
            return

        question = self.question_manager.get_current_question()

        self.score_manager.record_answer(
            correct=False,
            question=question,
            selected_direction=None,
            result="TIMEOUT"
        )
        self._next_question()


    # =========================================================
    # NEXT QUESTION
    # =========================================================

    def _next_question(self):

        self.question_manager.next_question()

        # -----------------------------------------------------
        # Game finished
        # -----------------------------------------------------

        if self.question_manager.is_finished():

            self._finish_game()

            return

        # -----------------------------------------------------
        # Start timer for next question
        # -----------------------------------------------------

        self.question_timer.start()


    # =========================================================
    # FINISH GAME
    # =========================================================

    def _finish_game(self):

        if not self.running:
            return

        self.game_timer.stop()

        self.running = False
        self.game_finished = True

        self.last_result = {

            "player_name":
                self.player_name,

            "player_id":
                self.player_id,

            "score":
                self.score_manager.get_score(),

            "correct_answers":
                self.score_manager.correct_answers,

            "total_questions":
                self.score_manager.total_questions,

            "time_seconds":
                round(
                    self.game_timer.elapsed_seconds(),
                    3
                ),

            "time_ms":
                round(
                    self.game_timer.elapsed_seconds()
                    * 1000
                ),

            "answer_history":
                self.score_manager.answer_history
        }
# =========================================================
# # GET RESULT
# =========================================================

    def get_result(self):

        return self.last_result