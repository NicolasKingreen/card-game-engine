import pygame
from pygame import Rect, Vector2
from enum import Enum

import textures
from aircraft import Aircraft, Type
from scene import Scene
from layer import Layer
from resource_holder import TextureHolder
from scene_node import SceneNode, SpriteNode


class World:
    def __init__(self, surface):
        # private
        self._surface = surface
        self._world_view = Rect((0, 0), pygame.display.get_window_size())
        self._texture_holder = TextureHolder()
        self._scene_graph = Scene()
        self._scene_layers = [self.Layer.BACKGROUND, self.Layer.AIR]

        self._world_bounds = Rect(0, 0, self._world_view.width, 2000)
        self._spawn_position = Vector2(self._world_view.width / 2,
                                       self._world_bounds.height - self._world_view.height)
        self._scroll_speed = 12.0
        self.player_aircraft = None  # Aircraft(Type.EAGLE, self._texture_holder)

        self._load_textures()
        self._build_scene()

        self._world_view.center = self._spawn_position

    def update(self, frame_time_s):
        self._world_view.move(0, self._scroll_speed * frame_time_s)

        position = self.player_aircraft.get_position()
        velocity = self.player_aircraft.velocity

        if (position.x <= self._world_bounds.left + 150 or
                position.x >= self._world_bounds.left + self._world_bounds.width - 150):
            velocity.x = -velocity.x
            self.player_aircraft.velocity = velocity

        self._scene_graph.update(frame_time_s)

    def draw(self):
        # how to set view?

        self._scene_graph.draw(self._surface)

    # private

    def _load_textures(self):
        self._texture_holder.load(textures.ID.EAGLE, "resources/textures/eagle.png")
        self._texture_holder.load(textures.ID.RAPTOR, "resources/textures/raptor.png")
        self._texture_holder.load(textures.ID.DESERT, "resources/textures/desert.png")

    def _build_scene(self):
        for i in range(self.Layer.LAYER_COUNT.value):
            layer = Layer()
            self._scene_graph.attach_child(layer)

        # background layer
        background_image = self._texture_holder.get(textures.ID.DESERT)
        background_rect = self._world_bounds
        # gotta repeat image to fit rect
        background_node = SpriteNode(background_image, background_rect)
        background_node.set_position(self._world_bounds.left, self._world_bounds.top)
        self._scene_layers[self.Layer.BACKGROUND.value].attach_child(background_node)

        # air layer
        leader = Aircraft(Type.EAGLE, self._texture_holder)
        self.player_aircraft = leader
        self.player_aircraft.set_position(self._spawn_position)
        self.player_aircraft.velocity = Vector2(40, self._scroll_speed)
        self._scene_layers[self.Layer.AIR.value].attach_child(self.player_aircraft)

        left_escort = Aircraft(Type.RAPTOR, self._texture_holder)
        left_escort.set_position(-80, 50)
        self.player_aircraft.attach_child(left_escort)

        right_escort = Aircraft(Type.RAPTOR, self._texture_holder)
        right_escort.set_position(80, 50)
        self.player_aircraft.attach_child(right_escort)


    class Layer(Enum):
        BACKGROUND = 0,
        AIR = 1,
        LAYER_COUNT = 2


