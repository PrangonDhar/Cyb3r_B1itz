import math
import random

import pygame

from ui.theme import (
    WIDTH,
    HEIGHT,
    CYAN,
    NEON_PURPLE,
    NEON_GLOW_RADIUS,
    PARTICLE_COUNT,
    PARTICLE_MIN_SPEED,
    PARTICLE_MAX_SPEED,
)


class Particle:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)

        self.speed = random.uniform(
            PARTICLE_MIN_SPEED,
            PARTICLE_MAX_SPEED
        )

        self.size = random.choice([1, 1, 2, 2, 3])

        self.alpha = random.randint(40, 150)

    def update(self):
        self.y -= self.speed

        if self.y < -10:
            self.y = HEIGHT + 10
            self.x = random.randint(0, WIDTH)

    def draw(self, screen):
        particle_surface = pygame.Surface(
            (self.size * 4, self.size * 4),
            pygame.SRCALPHA
        )

        pygame.draw.circle(
            particle_surface,
            (*CYAN, self.alpha),
            (
                self.size * 2,
                self.size * 2
            ),
            self.size
        )

        screen.blit(
            particle_surface,
            (
                self.x - self.size * 2,
                self.y - self.size * 2
            )
        )


class ParticleSystem:
    def __init__(self):
        self.particles = [
            Particle()
            for _ in range(PARTICLE_COUNT)
        ]

    def update(self):
        for particle in self.particles:
            particle.update()

    def draw(self, screen):
        for particle in self.particles:
            particle.draw(screen)


def draw_neon_rect(
    screen,
    rect,
    color,
    border_width=3,
    glow_radius=18
):
    """
    Draw a glowing neon rectangle.
    """

    # Glow layers
    for radius in range(glow_radius, 0, -4):

        alpha = int(
            35 * (1 - radius / glow_radius)
        )

        glow_surface = pygame.Surface(
            screen.get_size(),
            pygame.SRCALPHA
        )

        glow_color = (*color, alpha)

        pygame.draw.rect(
            glow_surface,
            glow_color,
            rect.inflate(radius * 2, radius * 2),
            width=border_width,
            border_radius=18
        )

        screen.blit(
            glow_surface,
            (0, 0)
        )

    # Main neon border
    pygame.draw.rect(
        screen,
        color,
        rect,
        width=border_width,
        border_radius=18
    )


def draw_scanlines(screen):
    """
    Subtle CRT-style scanlines.
    """

    overlay = pygame.Surface(
        screen.get_size(),
        pygame.SRCALPHA
    )

    for y in range(0, HEIGHT, 4):

        pygame.draw.line(
            overlay,
            (0, 0, 0, 20),
            (0, y),
            (WIDTH, y)
        )

    screen.blit(
        overlay,
        (0, 0)
    )


def pulse_value(
    minimum=0.85,
    maximum=1.15,
    speed=2.0
):
    """
    Returns a smooth pulsing value.
    """

    t = pygame.time.get_ticks() / 1000

    wave = (
        math.sin(t * speed)
        + 1
    ) / 2

    return minimum + (
        maximum - minimum
    ) * wave