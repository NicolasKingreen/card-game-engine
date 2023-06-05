from enum import Enum, auto
import sys


class TextureID(Enum):
    # EMPTY_CARD = 0,
    # TEST_CARD1 = 1,
    # TEST_CARD2 = 2,

    # utility
    SWAP = auto(),

    # suits
    SUIT_DIAMONDS = auto(),
    SUIT_HEARTS = auto(),
    SUIT_CLUBS = auto(),
    SUIT_SPADES = auto(),

    # diamonds cards
    DIAMONDS_ACE = auto(),
    DIAMONDS_TWO = auto(),
    DIAMONDS_THREE = auto(),
    DIAMONDS_FOUR = auto(),
    DIAMONDS_FIVE = auto(),
    DIAMONDS_SIX = auto(),
    DIAMONDS_SEVEN = auto(),
    DIAMONDS_EIGHT = auto(),
    DIAMONDS_NINE = auto(),
    DIAMONDS_TEN = auto(),
    DIAMONDS_JACK = auto(),
    DIAMONDS_QUEEN = auto(),
    DIAMONDS_KING = auto(),

    # hearts cards
    HEARTS_ACE = auto(),
    HEARTS_TWO = auto(),
    HEARTS_THREE = auto(),
    HEARTS_FOUR = auto(),
    HEARTS_FIVE = auto(),
    HEARTS_SIX = auto(),
    HEARTS_SEVEN = auto(),
    HEARTS_EIGHT = auto(),
    HEARTS_NINE = auto(),
    HEARTS_TEN = auto(),
    HEARTS_JACK = auto(),
    HEARTS_QUEEN = auto(),
    HEARTS_KING = auto(),

    # clubs cards
    CLUBS_ACE = auto(),
    CLUBS_TWO = auto(),
    CLUBS_THREE = auto(),
    CLUBS_FOUR = auto(),
    CLUBS_FIVE = auto(),
    CLUBS_SIX = auto(),
    CLUBS_SEVEN = auto(),
    CLUBS_EIGHT = auto(),
    CLUBS_NINE = auto(),
    CLUBS_TEN = auto(),
    CLUBS_JACK = auto(),
    CLUBS_QUEEN = auto(),
    CLUBS_KING = auto(),

    # spades cards
    SPADES_ACE = auto(),
    SPADES_TWO = auto(),
    SPADES_THREE = auto(),
    SPADES_FOUR = auto(),
    SPADES_FIVE = auto(),
    SPADES_SIX = auto(),
    SPADES_SEVEN = auto(),
    SPADES_EIGHT = auto(),
    SPADES_NINE = auto(),
    SPADES_TEN = auto(),
    SPADES_JACK = auto(),
    SPADES_QUEEN = auto(),
    SPADES_KING = auto(),

# how to create variables in code?
# this = sys.modules[__name__]
# for field in ID:
#     setattr(this, field.name, field.value)
