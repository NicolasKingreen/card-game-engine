from enum import Enum
import pygame

from textures import TextureID
from resource_holder import TextureHolder

from math import sin, cos, asin, acos, radians, degrees, sqrt, factorial


CARD_SIZE = 120, 180

# display_width, display_height = pygame.display.get_window_size()

display_width, display_height = 800, 600
CIRCLE_POS = display_width / 2, display_height + 400
CIRCLE_RADIUS = 700

MAX_CARDS_IN_HAND = 12


class CardType(Enum):
    EMPTY = 0,
    TEST_CARD1 = 1,
    TEST_CARD2 = 2


def card_type_to_texture_id(card_type):
    if card_type == CardType.EMPTY:
        return TextureID.EMPTY_CARD
    elif card_type == CardType.TEST_CARD1:
        return TextureID.TEST_CARD1


class Card:
    def __init__(self, card_type=CardType.EMPTY):
        self.attack = 3
        self.health = 2
        self.cost = 6

        self.scale = 1
        self._texture_id = card_type_to_texture_id(card_type)
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
            image = pygame.transform.scale(image,
                                           (image.get_width() * self.scale, image.get_height() * self.scale))
        return image


    def hover(self):
        if not self.is_hovered:
            self.is_hovered = True
            self.set_scale(1.2)
            #self.y_offset = 0
            self.y_offset = CARD_SIZE[1] / 3
        # print(self.is_hovered)

    def unhover(self):
        if self.is_hovered:
            self.is_hovered = False
            self.set_scale(1)
            self.y_offset = 0

    def set_scale(self, value):
        self.scale = value

    def set_on_circle_position(self, pos: (int, int)):
        self.on_circle_position = pos

    def set_angle(self, value):
        self.angle = value

    def smooth_scale_up(self, value):
        if self.scale <= value:
            self.scale += 0.1


class Hand:

    def __init__(self):
        self.cards_amount = 3
        # self.cards = [Card() for i in range(self.cards_amount)]
        self.cards = [Card(), Card(), Card(CardType.TEST_CARD1)]

        self.active_card_index = None

    def set_cards_amount(self, amount):
        self.cards_amount = min(max(amount, 1), MAX_CARDS_IN_HAND)
        self.cards = [Card() for i in range(self.cards_amount)]
    def drag_and_drop(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.active_card_index is not None:
            if pygame.mouse.get_pressed()[0]:
                self.cards[self.active_card_index].on_circle_position = mouse_pos


    def find_card_positions(self):
        positions = []
        heights = []
        # heights = [CARD_SIZE[1] / 3, ]
        screen_size = pygame.display.get_surface().get_size()
        all_card_width = CARD_SIZE[0] * len(self.cards) * 0.7

        step = all_card_width / len(self.cards)
        height_step = (CARD_SIZE[1]) / 2 / len(self.cards)

        pos = screen_size[0] // 2 - all_card_width // 2, screen_size[1] - CARD_SIZE[1] // 2
        for i in range(len(self.cards)):
            additional_height = abs((i - len(self.cards) // 2) * height_step)
            heights.append(additional_height)
            new_pos = pos[0] + i * step + CARD_SIZE[0]/2, pos[1] + additional_height
            # print((i - len(self.cards) //2 ) * height_step)
            self.cards[i].set_on_circle_position(new_pos)
            #positions.append(new_pos)
        #print(heights)
        #return positions

    def find_card_positions_2(self):
        angles = self.find_angles()
        on_circle_positions = []
        for i in range(len(self.cards)):
            # on_circle_positions.append(
            #     (400 + cos(radians(-90 + angles[i])) * 700,
            #      1200 + sin(radians(-90 + angles[i])) * 700)) # + CARD_SIZE[1] - 300))
            self.cards[i].set_on_circle_position((400 + cos(radians(-90 + angles[i])) * 700,
                                                  1200 + sin(radians(-90 + angles[i])) * 700))
        # return on_circle_positions

    def find_angles(self):
        angles = []
        left_angle = sqrt(20 * (len(self.cards) - 1))  # 0 for 1 card, 5 for 2, ..., 20 for 5+  hyperb?
        #left_angle = factorial(len(self.cards)) / pow(len(self.cards), 2)

        angle_step = (left_angle * 2 / (len(self.cards) - 1)) if len(self.cards) > 1 else 0

        for i in range(len(self.cards)):
            new_angle = left_angle - angle_step * i
            self.cards[i].set_angle(new_angle)
            angles.append(new_angle)
        #print(angles)
        return angles

    def update(self, frame_time_s):
        self.find_angles()
        self.find_card_positions_2()

        mouse_pos = pygame.mouse.get_pos()

        hand_left_pos = self.cards[-1].on_circle_position[0] - CARD_SIZE[0] / 2, self.cards[-1].on_circle_position[1] - \
                        CARD_SIZE[1] // 2
        hand_right_pos = self.cards[0].on_circle_position[0] - CARD_SIZE[0] / 2, self.cards[0].on_circle_position[1] - \
                         CARD_SIZE[1] // 2

        hand_width = hand_right_pos[0] - hand_left_pos[0]

        hand_rect = pygame.rect.Rect(hand_left_pos[0], hand_left_pos[1], hand_width + CARD_SIZE[0], CARD_SIZE[1])

        if hand_rect.collidepoint(mouse_pos):  # rect with must depend on cards amount

            card_angles = self.find_angles()
            mouse_angle = degrees(acos((mouse_pos[0] - 400) / 700)) - 90

            left_card_angle = sqrt(20 * (len(self.cards) - 1)) * 2  # wrong

            hand_arc = card_angles[0] - card_angles[-1] if len(card_angles) > 1 else 5
            card_arc = hand_arc / (len(self.cards))

            # mouse_angle += card_arc
            # mouse_angle *= -1
            # mouse_angle = min(mouse_angle, card_angles[0] - 0.1)

            match_index = 0
            min_diff = 999
            for i, angle in enumerate(card_angles[::-1]):
                if (abs(angle - mouse_angle)) < min_diff:
                    min_diff = abs(angle - mouse_angle)
                    match_index = i

            card_index = match_index


            # card_index = int(mouse_angle / card_arc)
            # card_index = min(max(card_index, 0), len(self.cards)-1)

            #print(f"{hand_arc:.2f} {card_angles[0]:.2f}..{card_angles[-1]:.2f}, {mouse_angle:.2f}, {card_index}, {left_card_angle}")

            for i, card in enumerate(self.cards):
                if i == card_index:
                    self.cards[card_index].hover()
                    self.cards[card_index].smooth_scale_up(1.5)
                    self.active_card_index = i
                else:
                    self.cards[i].unhover()
        else:
            for card in self.cards:
                card.unhover()

        self.drag_and_drop()



        # mouse_pos = abs(mouse_pos[0] - left_side)
        # for card in self.cards:
        #
        #     if mouse_pos[0]
        #         card.hover()
        #         break
        #     else:
        #         card.unhover()

    def draw(self, surface):
        for card in self.cards[::-1]:
            new_image = pygame.transform.rotate(card.image, -card.angle)
            rect = new_image.get_rect(center=card.on_circle_position)
            card.rect = rect
            rect.y -= card.y_offset
            surface.blit(new_image, rect)

        for card in self.cards[::-1]:
            if card.is_hovered:
                new_image = pygame.transform.rotate(card.image, -card.angle)
                rect = new_image.get_rect(center=card.on_circle_position)
                card.rect = rect
                rect.y -= card.y_offset
                surface.blit(new_image, rect)

        # pos = self.find_card_positions()
        # angles = self.find_angles()[::-1]
        # on_circle_positions = self.find_card_positions_2()[::-1]
        # for i, card in enumerate(self.cards[::-1]):
        #     on_circle_position = on_circle_positions[i]
        #     # print(on_circle_position)
        #     new_image = pygame.transform.rotate(card.image, -angles[i])
        #     rect = new_image.get_rect(center=on_circle_position)
        #     card.rect = rect
        #     rect.y -= card.y_offset
        #     surface.blit(new_image, rect)
        #     pygame.draw.circle(surface, (255, 0, 0), on_circle_position, 10)
        # pygame.draw.line(surface, (255, 0, 0), (400, 0), (400, 600), 1)
        # pygame.draw.circle(surface, (255, 0, 0), (400, 1200), 700, 1)
