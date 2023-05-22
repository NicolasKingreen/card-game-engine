from enum import Enum, IntEnum
import pygame
from pygame import Vector2

from settings import Settings

from math import sin, cos, asin, acos, radians, degrees, sqrt, factorial

from card import Card, CardSuit, CardRank, CARD_SIZE


# doesn't update if toggle fullscreen
# display_width, display_height = Settings.window_size
# CIRCLE_POS = Vector2(display_width / 2, display_height + 600)
CIRCLE_RADIUS = 700
CIRCLE_Y_OFFSET = 600


MAX_CARDS_IN_HAND = 12


# TODO: add in-hand cards reordering


class Hand:

    def __init__(self, starting_cards):
        self.cards_amount = 3
        # self.cards = [Card(CardSuit.HEARTS, CardRank.ACE) for i in range(self.cards_amount)]
        # self.cards = [
        #     Card(CardSuit.HEARTS, CardRank.ACE),
        #     Card(CardSuit.SPADES, CardRank.EIGHT),
        #     Card(CardSuit.DIAMONDS, CardRank.TWO),
        #     Card(CardSuit.CLUBS, CardRank.THREE)
        # ]

        self.cards = starting_cards

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
            on_circle_x = Settings.window_size.x / 2 + cos(radians(-90 + angles[i])) * CIRCLE_RADIUS
            on_circle_y = Settings.window_size.y + CIRCLE_Y_OFFSET + sin(radians(-90 + angles[i])) * CIRCLE_RADIUS
            self.cards[i].set_on_circle_position((on_circle_x, on_circle_y))
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

        hand_left_pos = self.cards[-1].on_circle_position[0] - CARD_SIZE[0] / 2, \
            self.cards[-1].on_circle_position[1] - CARD_SIZE[1] // 2
        hand_right_pos = self.cards[0].on_circle_position[0] - CARD_SIZE[0] / 2, \
            self.cards[0].on_circle_position[1] - CARD_SIZE[1] // 2

        hand_width = hand_right_pos[0] - hand_left_pos[0]

        hand_rect = pygame.rect.Rect(hand_left_pos[0], hand_left_pos[1], hand_width + CARD_SIZE[0], CARD_SIZE[1])

        if hand_rect.collidepoint(mouse_pos):  # rect width must depend on the cards amount

            card_angles = self.find_angles()

            mouse_angle = degrees(acos((mouse_pos[0] - Settings.window_size.x / 2) / CIRCLE_RADIUS)) - 90
            # this angle doesn't work well,
            # it projects mouse x directly onto circle underneath;
            # a better way would be to cast a ray to the circle's center
            # and find an intersection with that circle (?)

            # left_card_angle = sqrt(20 * (len(self.cards) - 1)) * 2

            hand_arc = card_angles[0] - card_angles[-1] if len(card_angles) > 1 else 5
            card_arc = hand_arc / (len(self.cards))  # actually half an arc (?)

            # mouse_angle += card_arc
            # mouse_angle *= -1
            # mouse_angle = min(mouse_angle, card_angles[0] - 0.1)

            match_index = -111
            min_diff = 999
            for i, angle in enumerate(card_angles[::-1]):
                # TODO: think about
                # user sees only part of a card, so it doesn't make sense
                # to compare mouse position to a card center;
                # card_angle is as card center
                # gotta offset by card_arc (basically card width on the arc)
                #
                # whole another way would be to detect collision
                # between mouse position and card rectangle,
                # but the rectangle should not update
                # when card scales and offsets
                # BUT: cards are rotated and their rectangles aren't

                # if (abs(angle + card_arc - mouse_angle)) < min_diff:
                if (abs(angle - mouse_angle)) < min_diff:
                    min_diff = abs(angle - mouse_angle)
                    match_index = i

            card_index = match_index

            # card_index = int(mouse_angle / card_arc)
            # card_index = min(max(card_index, 0), len(self.cards)-1)

            print(f"{hand_arc:.2f} {card_angles[0]:.2f}..{card_angles[-1]:.2f}, {mouse_angle:.2f}, {card_index}")

            for i, card in enumerate(self.cards):
                if i == card_index:
                    self.cards[card_index].hover()
                    # if not pygame.mouse.get_pressed()[0]:
                    self.active_card_index = i  # ?
                else:
                    self.cards[i].unhover()
        else:
            for card in self.cards:
                card.unhover()

        self.drag_and_drop()

    def draw(self, surface):
        # active_card = [] if self.active_card_index is None else [self.cards[self.active_card_index]]
        # for card in self.cards[::-1] + active_card:

        for card in self.cards[::-1]:
            new_image = pygame.transform.rotate(card.image, -card.angle)
            rect = new_image.get_rect(center=card.on_circle_position)
            card.rect = rect
            rect.y -= card.y_offset
            surface.blit(new_image, rect)

        # TODO: find a better way
        # basically goes through the all hand cards
        # just to find the selected card and draw it on top
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

        if Settings.draw_debug:

            # card centers
            for card in self.cards:
                pygame.draw.circle(surface, (255, 0, 0), card.on_circle_position, 5)

            # vertical line
            pygame.draw.line(surface,
                             (255, 0, 0),
                             (Settings.window_size.x / 2, 0),
                             (Settings.window_size.x / 2, Settings.window_size.y),
                             1)

            # hand arc forming circle
            pygame.draw.circle(surface,
                               (255, 0, 0),
                               (Settings.window_size.x / 2,
                                Settings.window_size.y + CIRCLE_Y_OFFSET),
                               CIRCLE_RADIUS, 1)
