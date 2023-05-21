from abc import ABC, abstractmethod

from pygame import Rect


class Transformable(ABC):
    def __init__(self):
        self.states = Rect(1, 1, 1, 1)

    def get_transform(self):
        pass

    def get_position(self):
        return self.states.topleft

    def set_position(self, x, y):
        self.states.topleft = x, y


class Drawable(ABC):
    @abstractmethod
    def draw(self, surface):
        pass

    @abstractmethod
    def draw_current(self, surface):
        pass


class SceneNode(ABC, Transformable, Drawable):

    def __init__(self):
        self.children = []
        self.parent = None

    def attach_child(self, child):
        child.parent = self
        self.children.append(child)

    def detach_child(self, child):
        if child in self.children:
            child.parent = None
            self.children.remove(child)

    def update(self, frame_time_s):
        self.update_current(frame_time_s)
        self.update_children(frame_time_s)

    def update_current(self, frame_time_s):
        pass

    def update_children(self, frame_time_s):
        for child in self.children:
            child.update(frame_time_s)

    def draw(self, surface):
        self.draw_current(surface)
        for child in self.children:
            child.draw(surface)

    def get_world_transform(self):
        transform = ...  # matrix?
        if self.parent is not None:
            transform = self.parent.get_world_transform() * transform
        else:
            transform = self.get_transform()

        return transform

    def get_world_position(self):
        return self.get_world_transform() * position  # 1, 1, 1 vector?


class SpriteNode(ABC, SceneNode):
    def __init__(self, image, states):
        SceneNode.__init__(self)
        self.image = image
        self.states = states

    def draw_current(self, surface):
        surface.blit(self.image, self.get_transform())


