import pygame

from enum import Enum, IntEnum

from textures import TextureID
from resource_holder import TextureHolder


CARD_SIZE = 120, 180


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

        self.is_hovered = False

        # pygame.draw.rect(self.image, (124, 230, 40), (0, 0, CARD_SIZE[0], CARD_SIZE[1]))
        # pygame.draw.rect(self.image, (123, 123, 123), (0, 0, CARD_SIZE[0], CARD_SIZE[1]), 1)

    @property
    def image(self):
        image = TextureHolder.get(self._texture_id)
        if self.scale != 1:
            target_size = (image.get_width() * self.scale,
                           image.get_height() * self.scale)
            image = pygame.transform.scale(image, target_size)
        return image

    def hover(self):
        if not self.is_hovered:
            self.is_hovered = True
            # self.set_scale(1.2)
            # self.y_offset = CARD_SIZE[1] / 3
        self.animate_hover()
        # print(self.is_hovered)

    def animate_hover(self):
        if self.scale < 1.5:
            self.scale += 0.06
        if self.y_offset < CARD_SIZE[1] / 3:
            self.y_offset += 20

    def unhover(self):
        if self.is_hovered:
            self.is_hovered = False
            self.set_scale(1)
            self.y_offset = 0
        self.animate_unhover()

    def animate_unhover(self):
        if self.scale > 1:
            self.scale = max(self.scale - 0.06, 1)
        if self.y_offset > 0:
            self.y_offset = max(self.y_offset - 20, 0)

    def set_scale(self, value):
        self.scale = value

    def set_on_circle_position(self, pos: (int, int)):
        self.on_circle_position = pos

    def set_angle(self, value):
        self.angle = value

    def smooth_scale_up(self, value):
        if self.scale <= value:
            self.scale += 0.1
