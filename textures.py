from enum import Enum
import sys


class TextureID(Enum):
    EMPTY_CARD = 0,
    TEST_CARD1 = 1,
    TEST_CARD2 = 2


# how to create variables in code?
# this = sys.modules[__name__]
# for field in ID:
#     setattr(this, field.name, field.value)
