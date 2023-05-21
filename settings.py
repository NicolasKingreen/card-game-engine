import pygame
from pygame import Vector2


class Settings:
    default_size = Vector2(1280, 720)
    max_size = Vector2(pygame.display.list_modes()[0])
    desktop_size = Vector2(pygame.display.get_desktop_sizes()[0])
    fullscreen = False

    window_size = desktop_size if fullscreen else default_size

