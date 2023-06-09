import pygame
from pygame import Vector2


class Settings:
    default_size = Vector2(1280, 720)
    max_size = Vector2(pygame.display.list_modes()[0])
    desktop_size = Vector2(pygame.display.get_desktop_sizes()[0])
    fullscreen = True
    window_size = desktop_size if fullscreen else default_size

    target_fps = 60

    draw_debug = False
