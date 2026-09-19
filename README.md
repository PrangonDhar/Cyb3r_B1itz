# Cyber Rapid Fire

**Cyber Rapid Fire** is a fast-paced cybersecurity awareness arcade game designed for technology exhibitions and corporate cybersecurity awareness events.

Players get approximately one minute to answer 10 cybersecurity-awareness questions using an arcade joystick, gamepad, or keyboard.

Each question presents two possible actions:

* One cybersecurity-safe action
* One unsafe/risky action

The player selects the appropriate action using UP/DOWN controls.

---

## Features

* Cybersecurity awareness focused gameplay
* 10 randomly selected questions per game
* Randomized position of correct answers
* 4-second response window per question
* Keyboard controls
* Gamepad controls
* Arcade joystick support through the browser Gamepad API
* A button mapped to ENTER
* Selected option highlighting
* Unselected option dimming
* Correct / Wrong / Timeout visual feedback
* Final scorecard
* Gameplay time recorded to milliseconds
* Complete answer review
* Replay support
* Central MongoDB Atlas leaderboard
* First-attempt leaderboard registration per Player ID and Game ID

---

## Game Flow

```text
START
  |
  v
3 - 2 - 1 - GO
  |
  v
QUESTION
  |
  v
PLAYER ANSWERS
  |
  v
CORRECT / WRONG / TIMEOUT
  |
  v
NEXT QUESTION
  |
  v
QUESTION 10
  |
  v
PLAYER NAME + STAFF ID
  |
  v
SCORECARD
  |
  v
SEE ANSWERS
  |
  v
ANSWER REVIEW
  |
  v
PLAY AGAIN
```

---

## Gameplay

Each game contains **10 questions**.

Each question has a response window of **4 seconds**.

If the player selects the correct action:

```text
+10 points
```

If the player selects the wrong action:

```text
0 points
```

If the response window expires:

```text
0 points
```

Maximum raw score:

```text
100
```

---

## Controls

### Keyboard

| Key        | Action                        |
| ---------- | ----------------------------- |
| Arrow Up   | Select upper option           |
| Arrow Down | Select lower option           |
| Enter      | Confirm / Continue / Navigate |

### Gamepad / Arcade Controller

| Control          | Action              |
| ---------------- | ------------------- |
| Right Stick Up   | Select upper option |
| Right Stick Down | Select lower option |
| A Button         | Enter               |

The X, Y and B buttons are currently unused.

---

## Technology Stack

### Backend

* Python
* Flask
* Flask-SocketIO
* PyMongo
* MongoDB Atlas

### Frontend

* HTML
* CSS
* JavaScript
* Socket.IO
* Browser Gamepad API

### Local Input

* Pygame
* Keyboard fallback

---

## Project Structure

```text
cyber_rapid_fire/
|
├── main.py
├── requirements.txt
├── README.md
├── .env.example
├── .gitignore
|
├── game/
│   ├── __init__.py
│   ├── game_engine.py
│   ├── question_manager.py
│   ├── input_manager.py
│   ├── scoring.py
│   └── timer.py
|
├── questions/
│   ├── __init__.py
│   └── question_bank.json
|
├── player/
│   ├── __init__.py
│   └── player_manager.py
|
├── network/
│   ├── __init__.py
│   └── leaderboard_client.py
|
├── local/
│   └── offline_queue.json
|
├── config/
│   └── config.json
|
└── web/
    ├── templates/
    │   └── index.html
    |
    ├── static/
    │   ├── css/
    │   │   ├── theme.css
    │   │   ├── main.css
    │   │   └── animations.css
    │   |
    │   ├── js/
    │   │   ├── game.js
    │   │   ├── effects.js
    │   │   └── input.js
    │   |
    │   └── assets/
    │       ├── images/
    │       ├── sounds/
    │       ├── fonts/
    │       └── logo/
    |
    └── app.py
```

---

## Architecture

```text
              ┌─────────────────────┐
              │  Arcade Controller  │
              │  Gamepad / Keyboard │
              └──────────┬──────────┘
                         |
                         v
              ┌─────────────────────┐
              │  Browser Frontend   │
              │     HTML/CSS/JS     │
              └──────────┬──────────┘
                         |
                      Socket.IO
                         |
                         v
              ┌─────────────────────┐
              │     Flask App       │
              └──────────┬──────────┘
                         |
                         v
              ┌─────────────────────┐
              │     Game Engine     │
              └──────┬────┬────┬────┘
                     |    |    |
                     v    v    v
               Questions Timer Scoring
                              |
                              v
                    ┌─────────────────┐
                    │   MongoDB Atlas │
                    │    Leaderboard  │
                    └─────────────────┘
```

The Python backend manages:

* Game state
* Question selection
* Answer validation
* Scoring
* Question timing
* Gameplay timing
* Leaderboard submission

The browser manages:

* User interface
* Animations
* Visual feedback
* Keyboard input
* Gamepad input
* Answer review
* Player interaction

---

## Question Format

Questions are stored in:

```text
questions/question_bank.json
```

Example:

```json
{
    "id": "SOCIAL_001",
    "category": "Social Engineering",
    "option_a": "Verify unexpected requests for sensitive information",
    "option_b": "Trust anyone claiming to be from IT",
    "correct": "A"
}
```

The game randomly selects questions from the question bank.

The two options are also randomized between the UP and DOWN positions.

Therefore, the correct answer is not always the UP option.

---

## Player Identity

After the game is completed, the player enters:

* Player Name
* Staff ID / Company ID

The Staff ID field accepts free-form text.

The player identity is collected **after gameplay** so that players can immediately start the game without entering information first.

---

## Leaderboard

The game uses MongoDB Atlas for centralized leaderboard storage.

Database:

```text
Cyber_Blitz
```

Collection:

```text
leaderboard
```

Game ID:

```text
cyber_rapid_fire
```

Example leaderboard document:

```json
{
    "playerId": "A531332",
    "playerName": "Rahul Sharma",
    "score": 850,
    "gameId": "cyber_rapid_fire"
}
```

A unique database index is maintained on:

```text
playerId + gameId
```

This ensures that only the first registered attempt for a player is eligible for leaderboard registration.

Players can still replay the game.

---

## Environment Variables

MongoDB credentials are **not stored in the Git repository**.

Create a `.env` file in the project root:

```text
MONGO_URI=your_mongodb_connection_string
```

The application loads the variable using `python-dotenv`.

Example:

```text
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/
```

### Important

Never commit the real `.env` file.

Never place the MongoDB username or password inside:

* Python source code
* `config.json`
* `README.md`
* `question_bank.json`
* GitHub

---

## Installation

Clone or copy the project:

```bash
cd cyber_rapid_fire
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create the `.env` file:

```text
MONGO_URI=your_mongodb_connection_string
```

Start the application:

```bash
python web/app.py
```

Open:

```text
http://127.0.0.1:5000
```

---

## Configuration

Game configuration is stored in:

```text
config/config.json
```

Current configuration:

```json
{
    "window": {
        "width": 1280,
        "height": 720,
        "fullscreen": false,
        "fps": 60
    },
    "game": {
        "questions_per_game": 10,
        "question_time_seconds": 4,
        "points_per_correct": 10
    },
    "leaderboard": {
        "display_limit": 10
    }
}
```

---

## MongoDB Credential Setup

The repository should contain:

```text
.env.example
```

with:

```text
MONGO_URI=your_mongodb_connection_string
```

The actual deployment machine should contain:

```text
.env
```

with the real MongoDB connection string.

The `.env` file must not be committed.

---

## Security

Cyber Rapid Fire is a cybersecurity awareness game and is not intended to perform offensive security testing against players, networks, or external systems.

The question bank focuses on cybersecurity awareness topics such as:

* Social engineering
* Phishing
* Password security
* Information handling
* Device security
* Safe browsing
* Suspicious requests
* Cyber hygiene

The application should be deployed in a controlled exhibition environment.

---

## Silver Release

**Project:** Cyber Rapid Fire
**Release:** Silver
**Purpose:** Cybersecurity Awareness Exhibition Arcade
**Gameplay:** 10 questions / approximately 1 minute
**Backend:** Python + Flask + Socket.IO
**Frontend:** HTML + CSS + JavaScript
**Database:** MongoDB Atlas
