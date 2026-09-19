import pygame

from ui.theme import (
    WIDTH,
    HEIGHT,
    BACKGROUND,
    WHITE,
    GREEN,
    RED,
    YELLOW,
    CYAN,
    OPTION_BACKGROUND,
    OPTION_BORDER,
    START_TITLE,
    START_SUBTITLE,
    START_BUTTON_TEXT,
    START_FOOTER,
    FONT_TITLE,
    FONT_SUBTITLE,
    FONT_BUTTON,
    FONT_FOOTER,
    NEON_BUTTON_WIDTH,
    NEON_BUTTON_HEIGHT,
    get_font,
)

from ui.animations import (
    draw_neon_rect,
    draw_scanlines,
    pulse_value,
)


def draw_text(screen, text, font, color, center):

    surface = font.render(
        text,
        True,
        color
    )

    rect = surface.get_rect(
        center=center
    )

    screen.blit(
        surface,
        rect
    )


def draw_start_screen(
    screen,
    particle_system
):

    screen.fill(BACKGROUND)

    # --------------------------------------------------------
    # Background particles
    # --------------------------------------------------------

    particle_system.update()
    particle_system.draw(screen)

    # --------------------------------------------------------
    # Outer neon frame
    # --------------------------------------------------------

    outer_rect = pygame.Rect(
        25,
        25,
        WIDTH - 50,
        HEIGHT - 50
    )

    draw_neon_rect(
        screen,
        outer_rect,
        CYAN,
        border_width=2,
        glow_radius=14
    )

    # --------------------------------------------------------
    # Title
    # --------------------------------------------------------

    draw_text(
        screen,
        START_TITLE,
        get_font(FONT_TITLE),
        CYAN,
        (WIDTH // 2, 145)
    )

    # --------------------------------------------------------
    # Subtitle
    # --------------------------------------------------------

    draw_text(
        screen,
        START_SUBTITLE,
        get_font(FONT_SUBTITLE),
        WHITE,
        (WIDTH // 2, 215)
    )

    # --------------------------------------------------------
    # Start button
    # --------------------------------------------------------

    button_rect = pygame.Rect(
        0,
        0,
        NEON_BUTTON_WIDTH,
        NEON_BUTTON_HEIGHT
    )

    button_rect.center = (
        WIDTH // 2,
        370
    )

    pulse = pulse_value(
        0.9,
        1.1,
        2.0
    )

    button_color = (
        min(255, int(CYAN[0] * pulse)),
        min(255, int(CYAN[1] * pulse)),
        min(255, int(CYAN[2] * pulse))
    )

    draw_neon_rect(
        screen,
        button_rect,
        button_color,
        border_width=3,
        glow_radius=18
    )

    draw_text(
        screen,
        START_BUTTON_TEXT,
        get_font(FONT_BUTTON),
        WHITE,
        button_rect.center
    )

    # --------------------------------------------------------
    # Footer
    # --------------------------------------------------------

    draw_text(
        screen,
        START_FOOTER,
        get_font(FONT_FOOTER),
        CYAN,
        (WIDTH // 2, 555)
    )

    # --------------------------------------------------------
    # CRT scanlines
    # --------------------------------------------------------

    draw_scanlines(screen)


def draw_game_screen(
    screen,
    question,
    question_number,
    total_questions,
    remaining_time,
    score
):

    screen.fill(BACKGROUND)

    draw_text(
        screen,
        "CYBER RAPID FIRE",
        get_font(52),
        CYAN,
        (WIDTH // 2, 55)
    )

    draw_text(
        screen,
        f"QUESTION {question_number}/{total_questions}",
        get_font(28),
        WHITE,
        (WIDTH // 2, 105)
    )

    timer_color = GREEN

    if remaining_time <= 1.5:
        timer_color = RED
    elif remaining_time <= 2.5:
        timer_color = YELLOW

    draw_text(
        screen,
        f"{remaining_time:.2f}",
        get_font(64),
        timer_color,
        (WIDTH // 2, 165)
    )

    top_rect = pygame.Rect(
        140,
        240,
        1000,
        150
    )

    bottom_rect = pygame.Rect(
        140,
        440,
        1000,
        150
    )

    pygame.draw.rect(
        screen,
        OPTION_BACKGROUND,
        top_rect,
        border_radius=20
    )

    pygame.draw.rect(
        screen,
        OPTION_BORDER,
        top_rect,
        width=3,
        border_radius=20
    )

    pygame.draw.rect(
        screen,
        OPTION_BACKGROUND,
        bottom_rect,
        border_radius=20
    )

    pygame.draw.rect(
        screen,
        OPTION_BORDER,
        bottom_rect,
        width=3,
        border_radius=20
    )

    draw_text(
        screen,
        "↑",
        get_font(45),
        CYAN,
        (95, 315)
    )

    draw_text(
        screen,
        "↓",
        get_font(45),
        CYAN,
        (95, 515)
    )

    draw_text(
        screen,
        question["top"],
        get_font(34),
        WHITE,
        top_rect.center
    )

    draw_text(
        screen,
        question["bottom"],
        get_font(34),
        WHITE,
        bottom_rect.center
    )

    draw_text(
        screen,
        f"SCORE: {score}",
        get_font(30),
        WHITE,
        (WIDTH // 2, 660)
    )


def draw_result_screen(
    screen,
    score,
    total_time,
    correct_answers
):

    screen.fill(BACKGROUND)

    draw_text(
        screen,
        "GAME COMPLETE!",
        get_font(64),
        CYAN,
        (WIDTH // 2, 150)
    )

    draw_text(
        screen,
        f"{score} POINTS",
        get_font(70),
        GREEN,
        (WIDTH // 2, 280)
    )

    draw_text(
        screen,
        f"TIME: {total_time:.3f}s",
        get_font(42),
        WHITE,
        (WIDTH // 2, 380)
    )

    draw_text(
        screen,
        f"CORRECT: {correct_answers}/10",
        get_font(36),
        WHITE,
        (WIDTH // 2, 460)
    )

    draw_text(
        screen,
        "Press ENTER to return",
        get_font(28),
        YELLOW,
        (WIDTH // 2, 590)
    )