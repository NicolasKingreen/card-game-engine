import pygame
from pygame import Vector2


MOUSE_BUTTONS_AMOUNT = 3  # or 5


class Input:

    mouse_pos = (0, 0)
    mouse_buttons_pressed = [False for _ in range(MOUSE_BUTTONS_AMOUNT)]
    mouse_buttons_held = [False for _ in range(MOUSE_BUTTONS_AMOUNT)]
    mouse_buttons_held_timers = [0 for _ in range(MOUSE_BUTTONS_AMOUNT)]
    mouse_buttons_released = [False for _ in range(MOUSE_BUTTONS_AMOUNT)]

    @staticmethod
    def update(frame_time_s):
        Input.mouse_pos = Vector2(pygame.mouse.get_pos())
        Input.mouse_buttons_pressed = [False for _ in range(MOUSE_BUTTONS_AMOUNT)]
        Input.mouse_buttons_released = [False for _ in range(MOUSE_BUTTONS_AMOUNT)]

        pressed_buttons = pygame.mouse.get_pressed(MOUSE_BUTTONS_AMOUNT)

        # HOOOOWOWOWOWO?!??!?

        for i in range(len(pressed_buttons)):
            if pressed_buttons[i] and not Input.mouse_buttons_held[i]:
                Input.mouse_buttons_pressed[i] = True
            if not pressed_buttons[i] and Input.mouse_buttons_held[i]:
                Input.mouse_buttons_released[i] = True

            if Input.mouse_buttons_held[i]:
                Input.mouse_buttons_held_timers[i] += frame_time_s
            else:
                Input.mouse_buttons_held_timers[i] = 0

        # Input.mouse_buttons_held = [i for i, is_pressed in enumerate(pressed_buttons) if is_pressed]
        Input.mouse_buttons_held = pressed_buttons



