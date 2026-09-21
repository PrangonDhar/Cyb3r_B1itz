from pathlib import Path
import sys
DEFAULT_QUESTION_TIME = 4.0

BASE_DIR = Path(__file__).resolve().parent.parent

sys.path.insert(
    0,
    str(BASE_DIR)
)


from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from game.game_engine import GameEngine
from game.input_manager import InputManager
from player.player_manager import PlayerManager
from network.leaderboard_client import submit_score

# =========================================================
# PATHS
# =========================================================

QUESTION_FILE = (
    BASE_DIR
    / "questions"
    / "question_bank.json"
)


# =========================================================
# FLASK
# =========================================================

app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static"
)


socketio = SocketIO(
    app,
    cors_allowed_origins="*"
)


# =========================================================
# GAME ENGINE
# =========================================================

game_engine = GameEngine(

    question_file=QUESTION_FILE,

    questions_per_game=10,

    question_time_seconds=DEFAULT_QUESTION_TIME,

    points_per_correct=10
)

input_manager = InputManager()
player_manager = PlayerManager()
DEFAULT_QUESTION_TIME = 4.0

def game_loop():

    print("Game loop started.")
    print(
        "RUNNING AT LOOP START:",
        game_engine.running
    )

    while game_engine.running:

        # =============================================
        # TIMEOUT ONLY
        # =============================================

        if (
            game_engine.question_active
            and
            game_engine.question_timer.expired()
        ):

            print("Question timeout.")

            game_engine.handle_timeout()

            socketio.emit(
                "answer_result",
                {
                    "result": "TIMEOUT",
                    "score":
                        game_engine.score_manager.get_score()
                }
            )

            # -----------------------------------------
            # Game finished after final timeout
            # -----------------------------------------

            if game_engine.game_finished:

                result = game_engine.get_result()

                socketio.emit(
                    "game_finished",
                    result
                )

            # -----------------------------------------
            # More questions remaining
            # -----------------------------------------

            else:

                socketio.start_background_task(
                    send_next_question_after_feedback
                )

        socketio.sleep(0.02)

    print("Game loop stopped.")


def send_next_question_after_feedback():

    socketio.sleep(0.7)

    if not game_engine.running:
        return

    game_engine.start_question_timer()

    socketio.emit(
        "next_question",
        game_engine.get_state()
    )
# =========================================================
# WEB PAGE
# =========================================================

@app.route("/")
def index():

    return render_template(
        "index.html"
    )


# =========================================================
# SOCKET CONNECT
# =========================================================

@socketio.on("connect")
def handle_connect():

    print("Browser connected.")

    emit(
        "system_status",
        {
            "status": "ONLINE"
        }
    )


# =========================================================
# SOCKET DISCONNECT
# =========================================================

@socketio.on("disconnect")
def handle_disconnect():

    print("Browser disconnected.")


# =========================================================
# START GAME
# =========================================================

@socketio.on("start_game")
def handle_start_game(data):
    print("START GAME received from browser.")

    if game_engine.running:
        print("Game already running. Rejecting duplicate start.")
        emit("start_rejected", {
            "reason": "GAME_ALREADY_RUNNING"
        })
        return

    question_time = DEFAULT_QUESTION_TIME

    if data:
        try:
            question_time = float(
                data.get(
                    "question_time",
                    DEFAULT_QUESTION_TIME
                )
            )
        except (TypeError, ValueError):
            question_time = DEFAULT_QUESTION_TIME

    question_time = max(
        1.0,
        min(question_time, 60.0)
    )

    game_engine.question_time = question_time
    game_engine.question_timer.duration = question_time

    print(
        f"QUESTION TIME: {question_time:.1f}s"
    )

    game_engine.set_player(None, None)
    game_engine.start_game()

    state = game_engine.get_state()

    socketio.start_background_task(game_loop)

    emit("game_started", state)

    print("Game started.")
    print(
        f"Question: "
        f"{state['question_number']}/"
        f"{state['total_questions']}"
    )
    print(f"Question ID: {state['id']}")
    print(f"TOP: {state['top']}")
    print(f"BOTTOM: {state['bottom']}")

@socketio.on("submit_identity")
def handle_submit_identity(data):
    print("IDENTITY RECEIVED:", data)

    player_name = data.get("player_name")
    player_id = data.get("player_id")

    if not player_name or not player_id:
        emit("identity_rejected", {
            "reason": "IDENTITY_REQUIRED"
        })
        return

    result = game_engine.get_result()

    if not result:
        emit("identity_rejected", {
            "reason": "NO_GAME_RESULT"
        })
        return

    # Attach identity to the completed game.
    game_engine.set_player(
        player_name,
        player_id
    )

    result = game_engine.get_result()

    result["player_name"] = player_name
    result["player_id"] = player_id

    leaderboard_result = submit_score(
        player_id=result["player_id"],
        player_name=result["player_name"],
        raw_score=result["score"],
        gameplay_time=result["time_seconds"]
    )

    result["leaderboard"] = leaderboard_result

    print(
        "LEADERBOARD RESULT:",
        leaderboard_result
    )

    emit(
        "identity_submitted",
        result
    )

# =========================================================
# PLAYER DIRECTION
# =========================================================

@socketio.on("player_direction")
def handle_player_direction(data):

    print(
        "DIRECTION RECEIVED:",
        data,
        "RUNNING:",
        game_engine.running
    )

    direction = data.get("direction")

    if direction not in ("UP", "DOWN"):
        return

    result = game_engine.submit_direction(direction)

    if result is None:
        return

    emit("answer_result", result)

    if game_engine.game_finished:

        final_result = game_engine.get_result()

        emit(
            "game_finished",
            final_result
        )

    else:

        socketio.start_background_task(
            send_next_question_after_feedback
        )

# =========================================================
# RUN
# =========================================================

if __name__ == "__main__":

    socketio.run(

        app,

        host="127.0.0.1",

        port=5000,

        debug=True,

        allow_unsafe_werkzeug=True
    )