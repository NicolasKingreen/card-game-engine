from enum import Enum, IntEnum
import pygame
from pygame import Vector2
from typing import Iterable

from settings import Settings
from input import Input

from math import sin, cos, asin, acos, radians, degrees, sqrt, factorial

from card import Card, CardSuit, CardRank, CARD_SIZE


# doesn't update when toggling fullscreen
# CIRCLE_POS = Vector2(display_width / 2, display_height + 600)

def get_circle_pos():
    return Vector2(Settings.window_size.x / 2, Settings.window_size.y + 600)


# CIRCLE_POS =
CIRCLE_RADIUS = 700
CIRCLE_Y_OFFSET = 600


MAX_CARDS_IN_HAND = 12
START_CARDS_AMOUNT = 6


# TODO: implement game mechanics, ui (text, buttons)


class Hand:

    def __init__(self, starting_cards):
        self.cards = starting_cards

        self.interaction_rect = None

        self.active_card_index = None
        self.current_card_index = None

        self.update_card_positions()

    def add(self, what: Card | Iterable[Card]):
    # def add(self, *cards):

        new_cards = []
        if isinstance(what, Card):
            new_cards.append(what)
        else:
            new_cards.extend(what)

        self.cards.extend(new_cards)
        # self.cards.extend(*cards)
        new_positions = self.find_card_positions()
        for card, position in zip(self.cards[-len(new_cards)+1:], new_positions[-len(new_cards)+1:]):
            # print(card.position, "goes to", position)
            card.release(position)
        self.update_card_positions()

    def remove(self, card_or_index: Card | int):
        if isinstance(card_or_index, Card):
            self.cards.remove(card_or_index)
        else:
            self.cards.pop(card_or_index)
        self.update_card_positions()

    def sort_cards(self):
        self.cards.sort(key=lambda x: (x.suit.value, x.rank.value))
        self.update_card_positions()

    def drag_and_drop(self):

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

            # if holding a card
            elif Input.mouse_buttons_held[0]:
                self.cards[self.active_card_index].position = Input.mouse_pos
                on_screen_normalized_x = max(min((Input.mouse_pos.x - Settings.window_size.x / 2) / CIRCLE_RADIUS, 1), -1)
                mouse_angle = degrees(acos(on_screen_normalized_x)) - 90
                self.cards[self.active_card_index].angle = mouse_angle

    def switch_cards(self, index_card_a, index_card_b):
        self.cards[index_card_a], self.cards[index_card_b] = self.cards[index_card_b], self.cards[index_card_a]
        self.update_card_positions()

    # TODO: implement card insertion (between two cards)

    def insert_card(self, card):
        if len(self.cards) < MAX_CARDS_IN_HAND:
            # print(card.scale)
            old_card_list = self.cards.copy()
            cards_before_index = old_card_list[:self.current_card_index]
            cards_after_index = old_card_list[self.current_card_index:]
            new_card_index = len(cards_before_index) + 1

            self.cards = cards_before_index + [card] + cards_after_index
            card_home_position = self.find_card_positions()[new_card_index]
            # print(card.rect)
            self.cards[new_card_index].release(card_home_position)
            self.update_card_positions()
            card.hover()
            #card.unhover()
            return True
        else:
            return False

    def find_card_angles(self):
        angles = []
        left_angle = sqrt(20 * (len(self.cards) - 1))
        angle_step = (left_angle * 2 / (len(self.cards) - 1)) if len(self.cards) > 1 else 0
        for i in range(len(self.cards)):
            new_angle = left_angle - angle_step * i
            angles.append(new_angle)
        return angles

    def update_card_angles(self):
        angles = self.find_card_angles()
        for card, new_angle in zip(self.cards, angles):
            card.angle = new_angle
        return angles

    def find_card_positions(self):
        angles = self.find_card_angles()
        positions = []
        for i in range(len(self.cards)):
            on_circle_x = Settings.window_size.x / 2 + cos(radians(90 + angles[i])) * CIRCLE_RADIUS
            on_circle_y = Settings.window_size.y + CIRCLE_Y_OFFSET + sin(radians(-90 + angles[i])) * CIRCLE_RADIUS
            positions.append(Vector2(on_circle_x, on_circle_y))
        return positions

    def update_card_positions(self):
        positions = self.find_card_positions()
        for card, new_position in zip(self.cards, positions):
            card.position = new_position
        self.interaction_rect = self.find_hand_rect()
        return positions

    def find_hand_rect(self):
        # Y position of hand = middle card Y position
        topleft_x = self.cards[0].position.x - CARD_SIZE.x / 2
        topleft_y = self.cards[len(self.cards)//2:len(self.cards)//2+1][0].position.y - CARD_SIZE.y // 2
        right_x = self.cards[-1].position.x + CARD_SIZE.x / 2
        hand_width = right_x - topleft_x
        hand_height = CARD_SIZE[1] + 10
        hand_rect = pygame.rect.Rect(topleft_x, topleft_y,
                                     hand_width, hand_height)
        return hand_rect

    def get_active_card_index(self):
        for i, card in enumerate(self.cards):
            if i == self.current_card_index and i != self.active_card_index:
                self.cards[self.current_card_index].hover()
                # if Input.mouse_buttons_held_timers[0] >= 0.2:  # could be used with hold timer
                if Input.mouse_buttons_pressed[0]:
                    self.active_card_index = i  # ?
            else:
                self.cards[i].unhover()

    def update(self, frame_time_s):
        # self.update_card_positions()
        card_angles = self.update_card_angles()

        if self.interaction_rect.collidepoint(Input.mouse_pos):

            mouse_angle = degrees(acos((Input.mouse_pos.x - Settings.window_size.x / 2) / CIRCLE_RADIUS)) - 90
            # this angle doesn't work well,
            # it projects mouse x directly onto circle underneath;
            # a better way would be to cast a ray to the circle's center
            # and find an intersection with that circle (?)

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
            self.get_active_card_index()

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
            # if card.scale is None:
            #     print(card)
            #     continue
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

        if Settings.draw_debug:
            pygame.draw.rect(surface, (255, 0, 0), self.interaction_rect, 1)
