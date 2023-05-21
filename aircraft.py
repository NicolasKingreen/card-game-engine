from enum import Enum


from entity import Entity
import textures
from scene_node import SceneNode
from resource_holder import TextureHolder


class Type(Enum):
    EAGLE = 0,
    RAPTOR = 1


def to_texture_id(aircraft_type: Type):
    if aircraft_type == Type.EAGLE:
        return textures.ID.EAGLE
    elif aircraft_type == Type.RAPTOR:
        return textures.ID.RAPTOR


class Aircraft(SceneNode, Entity):
    def __init__(self, aircraft_type: Type, texture_holder):
        Entity.__init__(self)
        self.type = aircraft_type
        self.image = texture_holder.get(to_texture_id(aircraft_type))

    def draw_current(self, surface):
        surface.blit(self.image, ...)



