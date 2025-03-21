from itertools import product
from random import shuffle
from .card import Card
from .rank import Rank
from .suit import Suit


class Deck:
    """
    Represents a deck of 52 cards, one per rank/suit pair
    """

    def __init__(self):
        self.cards = [
            Card(rank=rank, suit=suit) for rank, suit in product(Rank.RANKS, Suit.NAMES)
        ]

    def shuffle(self):
        shuffle(self.cards)

    def draw(self, n: int = 0):
        """
        Returns n cards from the deck. If less than n cards are available,
            raise an error
        """
        if n > len(self.cards):
            raise ValueError(
                f"Not enough cards left in deck to draw ({len(self.cards)} remaining)"
            )
        drawn_cards = self.cards[:n]
        del self.cards[:n]
        return drawn_cards

    def draw_hand(self):
        """
        Utility wrapper for draw with n == 5
        """
        return self.draw(5)
