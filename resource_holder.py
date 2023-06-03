import pygame
from abc import ABC, abstractmethod


class ResourceHolder(ABC):

    def __init__(self):
        self.resources = dict()  # id:resource mapping

    @abstractmethod
    def load(self, resource_id, filename):
        pass

    @abstractmethod
    def get(self, resource_id):
        pass


class TextureHolder:
    resources = {}

    @staticmethod
    def load(resource_id, filename):
        image = pygame.image.load(filename)
        TextureHolder.resources[resource_id] = image

    @staticmethod
    def add_surface(resource_id, surface):
        TextureHolder.resources[resource_id] = surface

    @staticmethod
    def get(resource_id):
        image = TextureHolder.resources.get(resource_id)
        if image is None:
            raise Exception("Texture not found!")
        return image


class FontHolder:
    resources = {}

    @staticmethod
    def load(resource_id, filename, font_size=16):
        font = pygame.font.Font(filename, font_size)
        FontHolder.resources[resource_id] = font

    @staticmethod
    def load_from_system(resource_id, font_name, font_size=16):
        font = pygame.font.SysFont(font_name, font_size)
        FontHolder.resources[resource_id] = font

    @staticmethod
    def get(resource_id):
        font = FontHolder.resources.get(resource_id)
        if font is None:
            raise Exception("Font not found!")
        return font

