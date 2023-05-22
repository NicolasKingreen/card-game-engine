from enum import Enum
from typing import Iterable
from math import copysign

# TODO: add different ease functions


class AnimationType(Enum):
    NONE = 0,
    SCALE = 1,
    Y_OFFSET = 2,
    X_MOVE = 3,
    Y_MOVE = 4,
    MOVE_TO_2D = 5  # couldn't implement


class Animation:

    def __init__(self, animation_type: AnimationType, start_value, end_value, time_s):

        self.type = animation_type

        self.start_value = start_value
        self.end_value = end_value
        self.current_value = start_value

        self.time_s = time_s
        self.current_time_s = 0

        # animation speed based on ease function
        # currently only linear
        self.speed_sign = 1 if end_value >= start_value else -1
        self.speed = self.speed_sign * abs(self.end_value - self.start_value) / self.time_s

    def update(self, frame_time_s):
        self.current_time_s = min(self.current_time_s + frame_time_s, self.time_s)

        # weird way
        new_value = self.current_value + self.speed * frame_time_s
        if self.speed_sign > 0:
            self.current_value = min(new_value, self.end_value)
        else:
            self.current_value = max(new_value, self.end_value)

    def is_finished(self):
        return self.current_time_s >= self.time_s

    def __repr__(self):
        return f'Animation(start_value={self.start_value}, end_value={self.end_value}): ' \
               f'{self.current_value}/{self.end_value} - {self.current_time_s}/{self.time_s}s'


class AnimationManager:

    def __init__(self):
        # can contain only one animation type example
        self.animations = []  # could be dict
        self._animations_to_remove = []

    @property
    def present_types(self):
        return [animation.type for animation in self.animations]

    def is_animation_type_present(self, animation_type: AnimationType):
        return animation_type in self.present_types

    def is_active(self):
        return len(self.animations) > 0

    def update(self, frame_time_s):
        for animation in self.animations:
            if not animation.is_finished():
                animation.update(frame_time_s)
                # if animation.is_finished():
                #     self._animations_to_remove.append(animation)

        # removing finished animations
        # for animation in self._animations_to_remove:
        #     self.animations.remove(animation)

    def _add_animation(self, animation):
        existing_animation = self.get_animation_by_type(animation.type)
        if existing_animation is not None:
            # new animation of the same type
            # continues from the current value
            # BUT: creating the second object seems cumbersome
            animation = Animation(animation.type,
                                  existing_animation.current_value,
                                  animation.end_value,
                                  animation.time_s)
            self.remove_by_type(animation.type)
        self.animations.append(animation)

    def add(self, what: Animation | Iterable[Animation]):
        if isinstance(what, Animation):
            self._add_animation(what)
        else:
            for animation in what:
                self._add_animation(animation)

    def remove_by_type(self, animation_type):
        # [self.animations.remove(animation) for animation in self.animations if animation.type == animation_type]
        if animation_type in self.present_types:
            self.animations.remove(self.get_animation_by_type(animation_type))

    def get_animation_by_type(self, animation_type: AnimationType) -> Animation | None:
        return next((animation for animation in self.animations if animation.type == animation_type), None)

    def get_current_value_by_type(self, animation_type: AnimationType):
        # if self.is_animation_type_present(animation_type):

        animation = self.get_animation_by_type(animation_type)
        if animation is not None:
            return animation.current_value


if __name__ == "__main__":
    manager = AnimationManager()
    scale_animation = Animation(AnimationType.SCALE, 1.0, 1.5, 0.2)
    manager.add(scale_animation)
    # print(manager.get_animation_by_type(AnimationType.SCALE))
    # manager.remove_by_type(AnimationType.Y_OFFSET)

    print(manager.get_current_value_by_type(AnimationType.SCALE))
    manager.update(0.12)
    print(manager.get_current_value_by_type(AnimationType.SCALE))
    manager.update(0.12)
    print(manager.get_current_value_by_type(AnimationType.SCALE))

