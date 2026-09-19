import json

import pygame

from game.game_engine import GameEngine


def load_config():
    with open("config/config.json", "r", encoding="utf-8") as file:
        return json.load(file)


def main():

    config = load_config()

    pygame.init()

    width = config["window"]["width"]
    height = config["window"]["height"]

    screen = pygame.display.set_mode(
        (width, height)
    )

    pygame.display.set_caption(
        "Cyber Rapid Fire"
    )

    game = GameEngine(
        screen,
        config
    )

    game.run()

    pygame.quit()


if __name__ == "__main__":
    main()