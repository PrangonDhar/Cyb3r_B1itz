const socket = io();


// =========================================================
// ELEMENTS
// =========================================================

const startScreen =
    document.getElementById("startScreen");

const gameScreen =
    document.getElementById("gameScreen");

const startButton =
    document.getElementById("startButton");

const categoryElement =
    document.getElementById("category");

const questionNumberElement =
    document.getElementById("questionNumber");

const totalQuestionsElement =
    document.getElementById("totalQuestions");

const scoreElement =
    document.getElementById("score");

const topTextElement =
    document.getElementById("topText");

const bottomTextElement =
    document.getElementById("bottomText");

const timerElement =
    document.getElementById("timer");

const timerFillElement =
    document.getElementById("timerFill");

const resultsScreen =
    document.getElementById("resultsScreen");

const finalScoreElement =
    document.getElementById("finalScore");

const correctAnswersElement =
    document.getElementById("correctAnswers");

const finalTimeElement =
    document.getElementById("finalTime");


const seeAnswersButton =
    document.getElementById("seeAnswersButton");

const playerScreen =
    document.getElementById("playerScreen");

const employeeButton =
    document.getElementById("employeeButton");

const externalButton =
    document.getElementById("externalButton");

const nameLabel =
    document.getElementById("nameLabel");

const idLabel =
    document.getElementById("idLabel");

const playerName =
    document.getElementById("playerName");

const playerId =
    document.getElementById("playerId");

const playerPreview =
    document.getElementById("playerPreview");

const continueButton =
    document.getElementById("continueButton");

const reviewScreen =
    document.getElementById("reviewScreen");

const reviewQuestionNumber =
    document.getElementById("reviewQuestionNumber");

const reviewTotalQuestions =
    document.getElementById("reviewTotalQuestions");

const reviewCategory =
    document.getElementById("reviewCategory");

const reviewStatus =
    document.getElementById("reviewStatus");

const reviewYourAnswer =
    document.getElementById("reviewYourAnswer");

const reviewCorrectAnswer =
    document.getElementById("reviewCorrectAnswer");

const reviewExplanation =
    document.getElementById("reviewExplanation");

const reviewNextButton =
    document.getElementById("reviewNextButton");


const reviewPlayAgainButton =
    document.getElementById("reviewPlayAgainButton");

const reviewScrollDown =
    document.getElementById(
        "reviewScrollDown"
    );

const topOption =
    document.getElementById("topOption");

const bottomOption =
    document.getElementById("bottomOption");

reviewScrollDown.addEventListener(
    "click",
    () => {

        reviewScreen.scrollBy({
            top: 420,
            behavior: "smooth"
        });

    }
);

// =========================================================
// PLAYER TYPE
// =========================================================

let playerType = "EMPLOYEE";


employeeButton.addEventListener(
    "click",
    () => {

        playerType = "EMPLOYEE";

        employeeButton.classList.add("active");

        externalButton.classList.remove("active");

        nameLabel.textContent =
            "EMPLOYEE NAME";

        idLabel.textContent =
            "STAFF ID";

        playerId.placeholder =
            "ENTER STAFF ID / COMPANY NAME";

        updatePlayerPreview();

    }
);


externalButton.addEventListener(
    "click",
    () => {

        playerType = "EXTERNAL";

        externalButton.classList.add("active");

        employeeButton.classList.remove("active");

        nameLabel.textContent =
            "NAME";

        idLabel.textContent =
            "COMPANY";

        playerId.placeholder =
            "ENTER COMPANY";

        updatePlayerPreview();

    }
);

// =========================================================
// PLAYER PREVIEW
// =========================================================

playerName.addEventListener(
    "input",
    updatePlayerPreview
);


playerId.addEventListener(
    "input",
    updatePlayerPreview
);


function updatePlayerPreview() {

    const name =
        playerName.value.trim();

    const id =
        playerId.value.trim();


    if (!name || !id) {

        playerPreview.textContent =
            "IDENTITY // --";

        return;

    }


    playerPreview.textContent =
        `IDENTITY // ${name}_${id}`;

}

// =========================================================
// GAME VARIABLES
// =========================================================

let currentDuration = 4.0;

let timerInterval = null;

let questionStartTime = null;

let gameStartSent = false;

let answerLocked = false;

let lastGameResult = null;

let reviewIndex = 0;

// =========================================================
// CONNECTION
// =========================================================

socket.on("connect", () => {

    console.log(
        "Connected to Cyber Rapid Fire server."
    );

});


socket.on(
    "start_rejected",
    (data) => {

        console.warn(
            "START REJECTED:",
            data.reason
        );

        gameStartSent = false;

        playerScreen.style.display =
            "block";

        gameScreen.style.display =
            "none";

        playerPreview.textContent =
            "SESSION // ALREADY ACTIVE";

    }
);

// =========================================================
// SYSTEM STATUS
// =========================================================

socket.on("system_status", (data) => {

    console.log(
        "System:",
        data.status
    );

});


// =========================================================
// START BUTTON
// =========================================================

startButton.addEventListener(
    "click",
    startCountdown
);


// =========================================================
// CONTINUE TO GAME
// =========================================================

continueButton.addEventListener(
    "click",
    startPlayerGame
);


function startPlayerGame() {

    const name =
        playerName.value.trim();

    const id =
        playerId.value.trim();

    if (!name || !id) {

        playerPreview.textContent =
            "IDENTITY // INPUT REQUIRED";

        return;
    }

    if (
        playerType === "EMPLOYEE" &&
        !/^\d{6}$/.test(id)
    ) {

        playerPreview.textContent =
            "IDENTITY // STAFF ID MUST BE 6 DIGITS";

        playerId.focus();

        return;
    }

    socket.emit(
        "submit_identity",
        {
            player_name: name,
            player_id: id
        }
    );

    continueButton.disabled = true;
}
// =========================================================
// GAME COUNTDOWN
// =========================================================

function startCountdown() {

    if (gameStartSent) {
        return;
    }

    startScreen.style.display = "none";
    playerScreen.style.display = "none";
    gameScreen.style.display = "none";

    showCountdown(3);

}


function showCountdown(number) {

    console.log(
        "COUNTDOWN:",
        number
    );

    const countdownOverlay =
        document.createElement("div");

    countdownOverlay.id =
        "countdownOverlay";

    countdownOverlay.className =
        "countdown-overlay";

    countdownOverlay.innerHTML = `
        <div class="countdown-grid"></div>

        <div class="countdown-corner top-left"></div>
        <div class="countdown-corner top-right"></div>
        <div class="countdown-corner bottom-left"></div>
        <div class="countdown-corner bottom-right"></div>

        <div class="countdown-content">

            <div class="countdown-system">
                SYSTEM INITIALIZING
            </div>

            <div class="countdown-number">
                ${number}
            </div>

            <div class="countdown-label">
                GET READY
            </div>

        </div>
    `;

    document.body.appendChild(
        countdownOverlay
    );


    // -----------------------------------------------------
    // NUMBER TRANSITION
    // -----------------------------------------------------

    requestAnimationFrame(() => {

        countdownOverlay
            .classList.add("countdown-active");

    });


    setTimeout(() => {

        countdownOverlay
            .classList.add("countdown-exit");

    }, 720);


    setTimeout(() => {

        countdownOverlay.remove();

        if (number > 1) {

            showCountdown(
                number - 1
            );

            return;
        }


        showGo();

    }, 950);

}

function showGo() {

    const countdownOverlay =
        document.createElement("div");

    countdownOverlay.id =
        "countdownOverlay";

    countdownOverlay.className =
        "countdown-overlay go-screen";

    countdownOverlay.innerHTML = `
        <div class="countdown-grid"></div>

        <div class="countdown-content">

            <div class="countdown-system">
                CONNECTION ESTABLISHED
            </div>

            <div class="countdown-go">
                GO
            </div>

            <div class="countdown-label">
                ATTACK SURFACE ACTIVE
            </div>

        </div>
    `;

    document.body.appendChild(
        countdownOverlay
    );


    requestAnimationFrame(() => {

        countdownOverlay
            .classList.add("countdown-active");

    });


    setTimeout(() => {

        countdownOverlay
            .classList.add("countdown-exit");

    }, 450);


    setTimeout(() => {

        countdownOverlay.remove();

        gameStartSent = true;

        socket.emit(
            "start_game",
            {}
        );

    }, 700);

}


// =========================================================
// GAME STARTED
// =========================================================

socket.on(
    "game_started",
    (data) => {

        console.log(
            "Game started:",
            data
        );

        showGameScreen();

        displayQuestion(
            data
        );

    }
);

/*function highlightSelectedOption(direction) {

    topOption.classList.remove(
        "option-selected",
        "option-dimmed"
    );

    bottomOption.classList.remove(
        "option-selected",
        "option-dimmed"
    );

    if (direction === "UP") {

        topOption.classList.add(
            "option-selected"
        );

        bottomOption.classList.add(
            "option-dimmed"
        );

    }
    else if (direction === "DOWN") {

        bottomOption.classList.add(
            "option-selected"
        );

        topOption.classList.add(
            "option-dimmed"
        );
    }
}*/

// =========================================================
// SHOW GAME SCREEN
// =========================================================

function showGameScreen() {

    startScreen.style.display =
        "none";

    gameScreen.style.display =
        "block";

}


// =========================================================
// DISPLAY QUESTION
// =========================================================

function displayQuestion(data) {

    console.log(
        "Displaying question:",
        data
    );


    // -----------------------------------------------------
    // HEADER
    // -----------------------------------------------------

    categoryElement.textContent =
        data.category;


    questionNumberElement.textContent =
        String(
            data.question_number
        ).padStart(2, "0");


    totalQuestionsElement.textContent =
        data.total_questions;


    scoreElement.textContent =
        data.score;


    // -----------------------------------------------------
    // OPTIONS
    // -----------------------------------------------------

    topTextElement.textContent =
        data.top;


    bottomTextElement.textContent =
        data.bottom;


    // -----------------------------------------------------
    // TIMER
    // -----------------------------------------------------

    currentDuration =
        data.duration;


    questionStartTime =
        performance.now();


    startTimer();

}

function selectAnswer(direction) {

    if (answerLocked) {
        return;
    }

    answerLocked = true;

    // Clear previous selection
    topOption.classList.remove(
        "option-selected",
        "option-dimmed"
    );

    bottomOption.classList.remove(
        "option-selected",
        "option-dimmed"
    );

    // Highlight selected option
    if (direction === "UP") {

        topOption.classList.add("option-selected");
        bottomOption.classList.add("option-dimmed");

    }
    else if (direction === "DOWN") {

        bottomOption.classList.add("option-selected");
        topOption.classList.add("option-dimmed");
    }

    // Give the selection a moment to appear
    setTimeout(() => {

        socket.emit(
            "player_direction",
            {
                direction: direction
            }
        );

    }, 180);
}
// =========================================================
// CLIENT DISPLAY TIMER
// =========================================================

function startTimer() {

    stopTimer();


    timerInterval =
        setInterval(
            updateTimer,
            50
        );


    updateTimer();

}


// =========================================================
// UPDATE TIMER
// =========================================================

function updateTimer() {

    if (
        questionStartTime === null
    ) {

        return;

    }


    const elapsed =
        (
            performance.now()
            -
            questionStartTime
        ) / 1000;


    const remaining =
        Math.max(
            0,
            currentDuration - elapsed
        );


    timerElement.textContent =
        remaining.toFixed(1);


    const percentage =
        (
            remaining
            /
            currentDuration
        ) * 100;


    timerFillElement.style.width =
        `${percentage}%`;


    if (remaining <= 0) {

        stopTimer();

    }

}


// =========================================================
// STOP TIMER
// =========================================================

function stopTimer() {

    if (
        timerInterval !== null
    ) {

        clearInterval(
            timerInterval
        );

        timerInterval = null;

    }

}


// =========================================================
// ANSWER RESULT
// =========================================================

// =========================================================
// ANSWER FEEDBACK
// =========================================================

socket.on(
    "answer_result",
    (data) => {

        console.log(
            "Answer:",
            data.result
        );

        scoreElement.textContent =
            data.score;

        showAnswerFeedback(
            data.result,
            data.score
        );
    }
);

// =========================================================
// ANSWER FEEDBACK DISPLAY
// =========================================================

function showAnswerFeedback(result, score) {

    // Remove any previous feedback
    const existingFeedback =
        document.getElementById(
            "answerFeedback"
        );

    if (existingFeedback) {
        existingFeedback.remove();
    }

    let title = "";
    let subtitle = "";
    let className = "";

    if (result === "CORRECT") {

        title = "CORRECT";
        subtitle = "+10";
        className = "feedback-correct";

    }

    else if (result === "WRONG") {

        title = "WRONG";
        subtitle = "THREAT DETECTED";
        className = "feedback-wrong";

    }

    else if (result === "TIMEOUT") {

        title = "TIMEOUT";
        subtitle = "RESPONSE WINDOW CLOSED";
        className = "feedback-timeout";
    }

    const feedback =
        document.createElement("div");

    feedback.id =
        "answerFeedback";

    feedback.className =
        `answer-feedback ${className}`;

    feedback.innerHTML = `

        <div class="feedback-scan"></div>

        <div class="feedback-content">

            <div class="feedback-status">
                ${title}
            </div>

            <div class="feedback-detail">
                ${subtitle}
            </div>

        </div>

    `;

    document.body.appendChild(
        feedback
    );

    // Start glow animation
    requestAnimationFrame(() => {

        feedback.classList.add(
            "feedback-active"
        );

    });

    // Start exit animation
    setTimeout(() => {

        feedback.classList.add(
            "feedback-exit"
        );

    }, 500);

    // Remove feedback
    setTimeout(() => {

        feedback.remove();

    }, 700);
}

// =========================================================
// NEXT QUESTION
// =========================================================

socket.on(
    "next_question",
    (data) => {

        console.log(
            "Next question:",
            data
        );

        // Give the answer feedback time to display
        setTimeout(() => {

            // Reset previous selection
            topOption.classList.remove(
                "option-selected",
                "option-dimmed"
            );

            bottomOption.classList.remove(
                "option-selected",
                "option-dimmed"
            );

            // Load next question
            displayQuestion(
                data
            );

            // Allow another answer
            answerLocked = false;

        }, 700);
    }
);

// =========================================================
// GAME FINISHED
// =========================================================

socket.on(
    "game_finished",
    (data) => {

        console.log(
            "GAME FINISHED"
        );

        console.log(
            data
        );

        stopTimer();

        playerScreen.style.display =
            "block";

        gameScreen.style.display =
            "none";

        resultsScreen.style.display =
            "none";

        playerName.value = "";
        playerId.value = "";

        playerPreview.textContent =
            "IDENTITY // ENTER DETAILS";

        continueButton.disabled = false;

        playerName.focus();

    }
);

socket.on(
    "identity_submitted",
    (data) => {

        console.log(
            "IDENTITY SUBMITTED:",
            data
        );

        continueButton.disabled =
            false;

        lastGameResult = 
            data;

        playerScreen.style.display =
            "none";

        showResults(
            data
        );

    }
);
// =========================================================
// SHOW RESULTS
// =========================================================

function showResults(data) {

    gameScreen.style.display =
        "none";

    resultsScreen.style.display =
        "block";


    finalScoreElement.textContent =
        data.score;


    correctAnswersElement.textContent =
        `${data.correct_answers} / ${data.total_questions}`;


    finalTimeElement.textContent =
        `${data.time_seconds.toFixed(3)}s`;

}

// =========================================================
// REPLAY
// =========================================================

reviewPlayAgainButton.addEventListener(
    "click",
    () => {

        reviewScreen.style.display =
            "none";

        resultsScreen.style.display =
            "none";

        playerScreen.style.display =
            "none";

        gameScreen.style.display =
            "none";

        startScreen.style.display =
            "block";

        playerName.value =
            "";

        playerId.value =
            "";

        playerPreview.textContent =
            "IDENTITY // --";

        gameStartSent =
            false;

        startButton.style.display =
            "";
    }
);

seeAnswersButton.addEventListener(
    "click",
    () => {

        if (
            !lastGameResult ||
            !lastGameResult.answer_history
        ) {
            console.error(
                "Answer history not available."
            );
            return;
        }

        resultsScreen.style.display =
            "none";

        reviewScreen.style.display =
            "block";

        renderAnswerReview();
    }
);


// =========================================================
// ANSWER REVIEW
// =========================================================

function renderAnswerReview() {

    const history =
        lastGameResult.answer_history;

    reviewSummary.textContent =
        `REVIEWING ${history.length} RESPONSES`;

    reviewList.innerHTML = "";

    history.forEach(
        (question, index) => {

            const correctDirection =
                question.correct_direction;

            const selectedDirection =
                question.selected_direction;

            const topIsCorrect =
                correctDirection === "UP";

            const bottomIsCorrect =
                correctDirection === "DOWN";

            const topIsChosen =
                selectedDirection === "UP";

            const bottomIsChosen =
                selectedDirection === "DOWN";


            const card =
                document.createElement("div");

            card.className =
                "review-question";


            // =================================================
            // TOP OPTION
            // =================================================

            let topClass =
                topIsCorrect
                    ? "review-option correct-option"
                    : "review-option wrong-option";

            if (topIsChosen) {
                topClass +=
                    " chosen-option";
            }


            // =================================================
            // BOTTOM OPTION
            // =================================================

            let bottomClass =
                bottomIsCorrect
                    ? "review-option correct-option"
                    : "review-option wrong-option";

            if (bottomIsChosen) {
                bottomClass +=
                    " chosen-option";
            }


            // =================================================
            // STATUS
            // =================================================

            let statusClass =
                "review-status";

            if (
                question.result === "CORRECT"
            ) {
                statusClass +=
                    " review-status-correct";
            }
            else if (
                question.result === "WRONG"
            ) {
                statusClass +=
                    " review-status-wrong";
            }
            else {
                statusClass +=
                    " review-status-timeout";
            }


            card.innerHTML = `

                <div class="review-question-header">

                    <div class="review-question-number">
                        Q${String(index + 1).padStart(2, "0")}
                    </div>

                    <div class="review-category">
                        ${question.category}
                    </div>

                    <div class="${statusClass}">
                        ${question.result}
                    </div>

                </div>


                <div class="review-options">

                    <div class="${topClass}">

                        <div class="review-direction">
                            ↑
                        </div>

                        <div class="review-option-text">
                            ${question.top}
                        </div>

                        <div class="review-option-badge">
                            ${
                                topIsCorrect
                                    ? "CORRECT"
                                    : "WRONG"
                            }
                        </div>


                    </div>


                    <div class="${bottomClass}">

                        <div class="review-direction">
                            ↓
                        </div>

                        <div class="review-option-text">
                            ${question.bottom}
                        </div>

                        <div class="review-option-badge">
                            ${
                                bottomIsCorrect
                                    ? "CORRECT"
                                    : "UNSAFE"
                            }
                        </div>

                    </div>

                </div>

            `;

            reviewList.appendChild(card);
        }
    );
}

reviewPlayAgainButton.addEventListener(
    "click",
    () => {

        reviewScreen.style.display =
            "none";

        resultsScreen.style.display =
            "none";

        startScreen.style.display =
            "block";

        playerScreen.style.display =
            "none";

        gameScreen.style.display =
            "none";

        playerName.value =
            "";

        playerId.value =
            "";

        playerPreview.textContent =
            "IDENTITY // --";

        gameStartSent =
            false;

        startButton.style.display =
            "";
    }
);

playerId.addEventListener(
    "input",
    () => {

        playerId.value =
            playerId.value
                .replace(g, "")
                .slice(0, 7);

        updatePlayerPreview();
    }
);
// =========================================================
// KEYBOARD CONTROLS
// =========================================================

const pressedKeys = new Set();

document.addEventListener(
    "keydown",
    (event) => {

        console.log(
            "KEY:",
            event.key
        );

        // -------------------------------------------------
        // ENTER
        // -------------------------------------------------

        if (event.key === "Enter") {

            event.preventDefault();

            // START SCREEN
            if (
                startScreen.style.display !== "none"
            ) {

                startButton.click();

                return;
            }

            // PLAYER IDENTIFICATION
            if (
                playerScreen.style.display !== "none"
            ) {

                if (
                    document.activeElement === playerName
                ) {

                    playerId.focus();

                    return;
                }

                if (
                    document.activeElement === playerId
                ) {

                    continueButton.click();

                    return;
                }

                return;
            }


            // SCORECARD → ANSWER REVIEW
            if (
                resultsScreen.style.display !== "none"
            ) {

                seeAnswersButton.click();

                return;
            }


            // ANSWER REVIEW → PLAY AGAIN
            if (
                reviewScreen.style.display !== "none"
            ) {

                reviewPlayAgainButton.click();

                return;
            }

            return;
        }


        // -------------------------------------------------
        // ARROW UP / DOWN
        // -------------------------------------------------

        if (
            event.key !== "ArrowUp" &&
            event.key !== "ArrowDown"
        ) {

            return;
        }


        // ARROWS DURING GAME
        if (
            gameScreen.style.display !== "none"
        ) {

            event.preventDefault();

            // Ignore browser key-repeat.
            if (
                pressedKeys.has(event.key)
            ) {

                return;
            }

            pressedKeys.add(event.key);

            const direction =
                event.key === "ArrowUp"
                    ? "UP"
                    : "DOWN";

            console.log(
                "KEYBOARD:",
                direction
            );
            
            selectAnswer(direction);

            return;
        }


        // ARROWS ON ANSWER REVIEW
        if (reviewScreen.style.display !== "none") {

            event.preventDefault();

            if (pressedKeys.has(event.key)) {
                return;
            }

            pressedKeys.add(event.key);

            if (event.key === "ArrowDown") {

                reviewList.scrollBy({
                    top: 420,
                    behavior: "smooth"
                });

            }
            else if (event.key === "ArrowUp") {

                reviewList.scrollBy({
                    top: -420,
                    behavior: "smooth"
                });

            }

        return;
}

    }
);


// ---------------------------------------------------------
// KEY RELEASE
// ---------------------------------------------------------

document.addEventListener(
    "keyup",
    (event) => {

        if (
            event.key === "ArrowUp" ||
            event.key === "ArrowDown"
        ) {

            pressedKeys.delete(
                event.key
            );

        }

    }
);

// =========================================================
// GAMEPAD CONTROLS
// =========================================================

let gamepadPreviousDirection = null;
let gamepadPreviousA = false;

function pollGamepad() {

    const gamepads = navigator.getGamepads();

    if (!gamepads) {
        requestAnimationFrame(pollGamepad);
        return;
    }

    const gamepad = gamepads[0];

    if (!gamepad) {
        requestAnimationFrame(pollGamepad);
        return;
    }

    // -----------------------------------------------------
    // RIGHT STICK
    // Axis 3 = vertical
    // -----------------------------------------------------

    const rightStickY =
        gamepad.axes[3] || 0;

    let direction = null;

    if (rightStickY < -0.5) {
        direction = "UP";
    }
    else if (rightStickY > 0.5) {
        direction = "DOWN";
    }

    // Send direction only once when stick crosses threshold
    if (
        direction &&
        direction !== gamepadPreviousDirection
    ) {

        // During gameplay → answer question
        if (
            gameScreen.style.display !== "none"
        ) {
            
            selectAnswer(direction);
        }

        // During answer review → scroll
        else if (
            reviewScreen.style.display !== "none"
        ) {

            if (direction === "DOWN") {

                reviewList.scrollBy({
                    top: 420,
                    behavior: "smooth"
                });

            }
            else if (direction === "UP") {

                reviewList.scrollBy({
                    top: -420,
                    behavior: "smooth"
                });

            }
        }
    }

    // Reset direction when stick returns to center
    if (!direction) {
        gamepadPreviousDirection = null;
    }
    else {
        gamepadPreviousDirection = direction;
    }


    // -----------------------------------------------------
    // A BUTTON → ENTER
    // -----------------------------------------------------

    const aPressed =
        gamepad.buttons[0]?.pressed === true;

    if (
        aPressed &&
        !gamepadPreviousA
    ) {

        const enterEvent =
            new KeyboardEvent(
                "keydown",
                {
                    key: "Enter",
                    code: "Enter",
                    bubbles: true
                }
            );

        document.dispatchEvent(enterEvent);
    }

    gamepadPreviousA = aPressed;

    requestAnimationFrame(pollGamepad);
}

pollGamepad();