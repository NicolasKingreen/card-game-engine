from card import Card, CardSuit, CardRank

from random import shuffle


class Deck:

    def __init__(self):
        self.cards = [Card(suit, rank) for suit in CardSuit for rank in CardRank]
        shuffle(self.cards)

    def draw_card(self):
        return self.cards.pop()
