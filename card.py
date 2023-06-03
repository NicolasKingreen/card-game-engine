import pygame
from pygame import Vector2

from enum import Enum, IntEnum

from settings import Settings
from textures import TextureID
from resource_holder import TextureHolder

from animation import Animation, AnimationType, AnimationManager

CARD_SIZE = Vector2(120, 180)


DECK_POSITION = Vector2(0, Settings.window_size.y / 2)


# animation values
SELECTION_SCALE = 1.1
SELECTION_Y_OFFSET = CARD_SIZE.y / 4

# animation times (in seconds)
SELECTION_SCALE_TIME = 0.1
SELECTION_Y_OFFSET_TIME = 0.1
RELEASE_TIME = 0.2
MOVE_TIME = 0.2


class CardRank(IntEnum):
    ACE = 1,
    TWO = 2,
    THREE = 3,
    FOUR = 4,
    FIVE = 5,
    SIX = 6,
    SEVEN = 7,
    EIGHT = 8,
    NINE = 9,
    TEN = 10,
    JACK = 11,
    QUEEN = 12,
    KING = 13


class CardSuit(IntEnum):
    DIAMONDS = 0,
    HEARTS = 1,
    CLUBS = 2,
    SPADES = 3


def build_card_image(card_rank: CardRank, card_suit: CardSuit):
    pass


# def card_type_to_texture_id(card_type):
#     if card_type == CardType.EMPTY:
#         return TextureID.EMPTY_CARD
#     elif card_type == CardType.TEST_CARD1:
#         return TextureID.TEST_CARD1


def suit_rank_to_texture_id(suit: CardSuit, rank: CardRank):
    texture_name = (suit.name + '_' + rank.name).upper()
    return TextureID[texture_name]


class Card:
    def __init__(self, suit=CardSuit.HEARTS, rank=CardRank.ACE):

        self.suit = suit
        self.rank = rank

        # for animations
        self.animation_manager = AnimationManager()
        self.scale = 1
        self.y_offset = 0
        self.angle = 0

        # for displaying
        self._texture_id = suit_rank_to_texture_id(suit, rank)
        self.rect = self.image.get_rect()

        self.position = DECK_POSITION

        self.is_hovered = False

    @property
    def image(self):
        image = TextureHolder.get(self._texture_id)
        if self.scale != 1:
            target_size = (image.get_width() * self.scale,
                           image.get_height() * self.scale)
            image = pygame.transform.scale(image, target_size)
        if self.angle != 0:
            image = pygame.transform.rotate(image, self.angle)
        return image

    def update(self, frame_time_s):
        if self.animation_manager.is_active():
            self.animation_manager.update(frame_time_s)

            scale = self.animation_manager.get_current_value_by_type(AnimationType.SCALE)
            if scale is not None:
                self.scale = scale

            angle = self.animation_manager.get_current_value_by_type(AnimationType.ROTATE)
            if angle is not None:
                self.angle = angle

            y_offset = self.animation_manager.get_current_value_by_type(AnimationType.Y_OFFSET)
            if y_offset is not None:
                self.y_offset = y_offset

            x = self.animation_manager.get_current_value_by_type(AnimationType.X_MOVE)
            if x is not None:
                self.position = Vector2(x, self.position.y)

            y = self.animation_manager.get_current_value_by_type(AnimationType.Y_MOVE)
            if y is not None:
                self.position = Vector2(self.position.x, y)

            # weirdos below

            x_move_anim = self.animation_manager.get_animation_by_type(AnimationType.X_MOVE)
            if x_move_anim and x_move_anim.is_finished():
                self.animation_manager.remove_by_type(AnimationType.X_MOVE)

            y_move_anim = self.animation_manager.get_animation_by_type(AnimationType.Y_MOVE)
            if y_move_anim and y_move_anim.is_finished():
                self.animation_manager.remove_by_type(AnimationType.Y_MOVE)

            rotate_anim = self.animation_manager.get_animation_by_type(AnimationType.ROTATE)
            if rotate_anim and rotate_anim.is_finished():
                self.animation_manager.remove_by_type(AnimationType.ROTATE)

    def hover(self):
        if not self.is_hovered:
            self.is_hovered = True

            # animate selected card
            scale_animation = Animation(AnimationType.SCALE, 1.0, SELECTION_SCALE, SELECTION_SCALE_TIME)
            y_offset_animation = Animation(AnimationType.Y_OFFSET, 0, SELECTION_Y_OFFSET, SELECTION_Y_OFFSET_TIME)
            self.animation_manager.add([scale_animation, y_offset_animation])

    def unhover(self):
        if self.is_hovered:
            self.is_hovered = False

            # animate it back to hand
            scale_animation = Animation(AnimationType.SCALE, SELECTION_SCALE, 1.0, SELECTION_SCALE_TIME)
            y_offset_animation = Animation(AnimationType.Y_OFFSET, SELECTION_Y_OFFSET, 0, SELECTION_Y_OFFSET_TIME)
            self.animation_manager.add([scale_animation, y_offset_animation])

    def release(self, home_position, start_angle):
        x_move_animation = Animation(AnimationType.X_MOVE, self.position[0], home_position[0], RELEASE_TIME)
        y_move_animation = Animation(AnimationType.Y_MOVE, self.position[1], home_position[1], RELEASE_TIME)
        self.animation_manager.add([x_move_animation, y_move_animation])

        rotate_animation = Animation(AnimationType.ROTATE, start_angle, 0, RELEASE_TIME)
        self.animation_manager.add(rotate_animation)

    def move_to(self, position):
        # print("moving", self, "from", self.position, "to", position)
        x_move_animation = Animation(AnimationType.X_MOVE, self.position.x, position.x, MOVE_TIME)
        self.animation_manager.add(x_move_animation)
        y_move_animation = Animation(AnimationType.Y_MOVE, self.position.y, position.y, MOVE_TIME)
        self.animation_manager.add(y_move_animation)

    def draw(self, surface):
        new_image = self.image
        rect = new_image.get_rect(center=self.position)
        self.rect = rect
        rect.y -= self.y_offset
        surface.blit(new_image, rect)

    def __repr__(self):
        return f'Card<{self.suit.name}:{self.rank.name}>'

