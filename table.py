from pygame import Vector2
from settings import Settings


MAX_CARDS_ON_TABLE = 12  # should be equal hand size

MIN_X_GAP = 400/3
MAX_CARDS_IN_ROW = 6


LAYOUTS = [
    # 1 card

    # 2 cards

    # ...

]


class Table:

    def __init__(self):
        self.cards = []

    def update(self, frame_time_s):
        pass

    def find_card_positions(self):
        x_gap = max(200 * (1 / len(self.cards) + 0.5), MIN_X_GAP)
        y_gap = 200

        positions = []
        for i in range(len(self.cards)):
            card_pos = Vector2(i % 6 * x_gap, (i//6) * y_gap)
            positions.append(card_pos)

        # offset placed cards to screen center
        offset = Vector2(x_gap * min(len(self.cards)-1, 5) / 2,
                         y_gap * ((len(self.cards)-1)//6) / 2 + 100)
        offset -= Settings.window_size / 2
        positions = [position - offset for position in positions]

        return positions

    def _update_card_positions(self):
        if len(self.cards) < 1:
            return
        card_positions = self.find_card_positions()
        for card, position in zip(self.cards, card_positions):
            card.position = position

    def place_card(self, card):
        card.scale = 1
        # placed cards could save their angle
        # to represent liveness of the game
        card.angle = 0
        self.cards.append(card)
        self._update_card_positions()

    def clear(self):
        cards_to_return = self.cards.copy()
        self.cards.clear()
        return cards_to_return

    def draw(self, surface):
        for card in self.cards:
            card.draw(surface)

