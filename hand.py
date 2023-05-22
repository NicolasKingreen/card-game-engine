from enum import Enum, IntEnum
import pygame
from pygame import Vector2
from typing import Iterable

from settings import Settings
from input import Input

from math import sin, cos, asin, acos, radians, degrees, sqrt, factorial

from card import Card, CardSuit, CardRank, CARD_SIZE


# doesn't update if toggle fullscreen
# display_width, display_height = Settings.window_size
# CIRCLE_POS = Vector2(display_width / 2, display_height + 600)
CIRCLE_RADIUS = 700
CIRCLE_Y_OFFSET = 600


MAX_CARDS_IN_HAND = 12
START_CARDS_AMOUNT = 6


# TODO: implement game mechanics


class Hand:

    def __init__(self, starting_cards):
        self.cards = starting_cards

        self.hand_rect = None

        self.active_card_index = None
        self.current_card_index = None

        self.update_card_positions()

    def add(self, what: Card | Iterable[Card]):
        if isinstance(what, Card):
            self.cards.append(what)
        else:
            for card in what:
                self.cards.append(card)
        self.update_card_positions()

    def remove(self, card_or_index: Card | int):
        if isinstance(card_or_index, Card):
            self.cards.remove(card_or_index)
        else:
            self.cards.pop(card_or_index)
        self.update_card_positions()

    def drag_and_drop(self):
        mouse_pos = Input.mouse_pos

        # if there is a grabbed card
        if self.active_card_index is not None:
            if Input.mouse_buttons_released[0]:
                if self.active_card_index != self.current_card_index and self.current_card_index is not None:
                    self.switch_cards(self.active_card_index, self.current_card_index)
                    # TODO: add swap indicator
                else:
                    card_home_position = self.find_card_positions()[self.active_card_index]
                    self.cards[self.active_card_index].release(card_home_position)
                self.active_card_index = None

            # if Input.mouse_buttons_held[0]:
            elif Input.mouse_buttons_held[0]:
                self.cards[self.active_card_index].position = mouse_pos
                # BUG: on wide window edges acos breakes the code

                #if self.cards[self.active_card_index].angle < 30:

                self.cards[self.active_card_index].angle = (degrees(acos(min(max((mouse_pos[0] - Settings.window_size.x / 2) / CIRCLE_RADIUS, -1), 1))) - 90)


                    #self.cards[self.active_card_index].angle = 90
                #print((mouse_pos[0] - Settings.window_size.x / 2) / CIRCLE_RADIUS)
                #min(max((mouse_pos[0] - Settings.window_size.x / 2) / CIRCLE_RADIUS, -1), 1)

    def switch_cards(self, index_card_a, index_card_b):
        self.cards[index_card_a], self.cards[index_card_b] = self.cards[index_card_b], self.cards[index_card_a]
        self.update_card_positions()

    # TODO: implement card insertion (between two cards)

    def find_card_angles(self):
        angles = []
        left_angle = sqrt(20 * (len(self.cards) - 1))
        angle_step = (left_angle * 2 / (len(self.cards) - 1)) if len(self.cards) > 1 else 0
        for i in range(len(self.cards)):
            new_angle = -(left_angle - angle_step * i)
            angles.append(new_angle)
        return angles[::-1]

    def update_card_angles(self):
        angles = self.find_card_angles()
        for card, new_angle in zip(self.cards, angles):
            card.angle = new_angle

    def find_card_positions(self):
        angles = self.find_card_angles()
        positions = []
        for i in range(len(self.cards)):
            on_circle_x = Settings.window_size.x / 2 + cos(radians(-90 + angles[i])) * CIRCLE_RADIUS
            on_circle_y = Settings.window_size.y + CIRCLE_Y_OFFSET + sin(radians(-90 + angles[i])) * CIRCLE_RADIUS
            positions.append(Vector2(on_circle_x, on_circle_y))
        return positions[::-1]

    def update_card_positions(self):
        positions = self.find_card_positions()
        for card, new_position in zip(self.cards, positions):
            card.position = new_position

        self.hand_rect = self.find_hand_rect()

    def find_hand_rect(self):
        # Y position of hand = middle card Y position
        topleft_x = self.cards[0].position.x - CARD_SIZE.x / 2
        topleft_y = self.cards[len(self.cards)//2:len(self.cards)//2+1][0].position[1] - CARD_SIZE[1] // 2

        right_x = self.cards[-1].position.x + CARD_SIZE.x / 2

        hand_width = right_x - topleft_x
        hand_height = CARD_SIZE[1] + 10

        hand_rect = pygame.rect.Rect(topleft_x, topleft_y,
                                     hand_width, hand_height)
        return hand_rect

    def update(self, frame_time_s):
        # self.update_card_positions()
        self.update_card_angles()

        if self.hand_rect.collidepoint(Input.mouse_pos):  # rect width must depend on the cards amount

            card_angles = self.find_card_angles()

            mouse_angle = degrees(acos((Input.mouse_pos.x - Settings.window_size.x / 2) / CIRCLE_RADIUS)) - 90
            # this angle doesn't work well,
            # it projects mouse x directly onto circle underneath;
            # a better way would be to cast a ray to the circle's center
            # and find an intersection with that circle (?)

            # left_card_angle = sqrt(20 * (len(self.cards) - 1)) * 2

            hand_arc = card_angles[-1] - card_angles[0] if len(card_angles) > 1 else 5
            card_arc = hand_arc / (len(self.cards))  # actually half an arc (?)

            match_index = -111
            min_diff = 999
            for i, angle in enumerate(card_angles):
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

            self.current_card_index = match_index

            # print(f"{hand_arc:.2f} {card_angles[0]:.2f}..{card_angles[-1]:.2f}, {mouse_angle:.2f}, {card_index}")

            for i, card in enumerate(self.cards):
                if i == self.current_card_index:
                    self.cards[self.current_card_index].hover()
                    # if Input.mouse_buttons_held_timers[0] >= 0.2:
                    if Input.mouse_buttons_pressed[0]:
                        self.active_card_index = i  # ?
                else:
                    self.cards[i].unhover()
        else:
            for card in self.cards:
                card.unhover()
            self.current_card_index = None

        self.drag_and_drop()

        # update animations
        for card in self.cards:
            card.update(frame_time_s)

    def draw(self, surface):

        card_for_later_draw = None
        for i, card in enumerate(self.cards):
            if self.active_card_index is not None:
                if self.active_card_index == i:
                    card_for_later_draw = card
                    continue
            elif card.is_hovered:
                card_for_later_draw = card
                continue
            card.draw(surface)

        if card_for_later_draw:
            card_for_later_draw.draw(surface)


