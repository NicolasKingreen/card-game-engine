import pygame

from enum import Enum, IntEnum

from textures import TextureID
from resource_holder import TextureHolder

from animation import Animation, AnimationType, AnimationManager

CARD_SIZE = 120, 180

# animation times (in seconds)
SELECTION_SCALE_TIME = 0.1
SELECTION_Y_OFFSET_TIME = 0.1


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

        # for displaying
        self.scale = 1
        self._texture_id = suit_rank_to_texture_id(suit, rank)
        self.rect = self.image.get_rect()
        self.y_offset = 0

        self.on_circle_position = 0
        self.angle = 0

        # animations
        self.animation_manager = AnimationManager()

        self.is_hovered = False

    @property
    def image(self):
        image = TextureHolder.get(self._texture_id)
        if self.scale != 1:
            target_size = (image.get_width() * self.scale,
                           image.get_height() * self.scale)
            image = pygame.transform.scale(image, target_size)
        return image

    def update(self, frame_time_s):
        if self.animation_manager.is_active():
            self.animation_manager.update(frame_time_s)
            self.scale = self.animation_manager.get_current_value_by_type(AnimationType.SCALE)
            self.y_offset = self.animation_manager.get_current_value_by_type(AnimationType.Y_OFFSET)

    def hover(self):
        if not self.is_hovered:
            self.is_hovered = True

            # animate selected card
            scale_animation = Animation(AnimationType.SCALE, 1.0, 1.5, SELECTION_SCALE_TIME)
            y_offset_animation = Animation(AnimationType.Y_OFFSET, 0, CARD_SIZE[1] / 3, SELECTION_Y_OFFSET_TIME)
            self.animation_manager.add([scale_animation, y_offset_animation])

    def unhover(self):
        if self.is_hovered:
            self.is_hovered = False

            # animate it back to hand
            scale_animation = Animation(AnimationType.SCALE, 1.5, 1.0, SELECTION_SCALE_TIME)
            y_offset_animation = Animation(AnimationType.Y_OFFSET, CARD_SIZE[1] / 3, 0, SELECTION_Y_OFFSET_TIME)
            self.animation_manager.add([scale_animation, y_offset_animation])

    def set_scale(self, value):
        self.scale = value

    def set_on_circle_position(self, pos: (int, int)):
        self.on_circle_position = pos

    def set_angle(self, value):
        self.angle = value

    # def smooth_scale_up(self, value):
    #     if self.scale <= value:
    #         self.scale += 0.1
