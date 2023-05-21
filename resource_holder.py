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
            raise Exception("Resource not found!")
        return image


