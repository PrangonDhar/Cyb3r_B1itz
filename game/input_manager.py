import pygame


class InputManager:

    UP = "UP"
    DOWN = "DOWN"
    NONE = None

    def __init__(self):

        pygame.init()
        pygame.joystick.init()

        self.joystick = None
        self.previous_direction = self.NONE

        if pygame.joystick.get_count() > 0:

            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()

            print(
                f"Joystick detected: "
                f"{self.joystick.get_name()}"
            )

        else:

            print(
                "No joystick detected. "
                "Keyboard fallback enabled."
            )


    def get_direction(self):

        pygame.event.pump()

        direction = self.NONE


        # =================================================
        # KEYBOARD FALLBACK
        # =================================================

        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:

            direction = self.UP

        elif keys[pygame.K_DOWN]:

            direction = self.DOWN


        # =================================================
        # JOYSTICK
        # =================================================

        if self.joystick:

            axis_y = self.joystick.get_axis(1)

            if axis_y < -0.5:

                direction = self.UP

            elif axis_y > 0.5:

                direction = self.DOWN


        # =================================================
        # DEBOUNCE
        # =================================================

        if direction != self.previous_direction:

            self.previous_direction = direction

            if direction in (
                self.UP,
                self.DOWN
            ):

                return direction


        if direction == self.NONE:

            self.previous_direction = self.NONE


        return self.NONE