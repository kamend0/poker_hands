from dataclasses import dataclass
from functools import total_ordering


@total_ordering
@dataclass
class Suit:
    """
    Represents the four suits: clubs, diamonds, hearts, and spades.
    Their cardinality from lowest to highest is in that order.
    """

    suit: str

    NAMES = ["clubs", "diamonds", "hearts", "spades"]
    SYMBOLS = ["♣", "♦", "♥", "♠"]

    def _block_cross_type_comaprisons(self, other):
        if not isinstance(other, Suit):
            return NotImplemented

    def __post_init__(self):
        if not isinstance(self.suit, str):
            raise TypeError("Suit must be identified by a string")

        self.suit = self.suit.lower()

        if self.suit not in self.NAMES + self.SYMBOLS:
            raise ValueError(
                f"Suit must be one of: {', '.join(self.NAMES)}; or: {', '.join(self.SYMBOLS)}"
            )
        elif self.suit in self.NAMES:  # User provided self.suit by name
            self.name = self.suit
            self.symbol = self.SYMBOLS[self.NAMES.index(self.suit)]
        elif self.suit in self.SYMBOLS:  # or, by symbol
            self.name = self.NAMES[self.SYMBOLS.index(self.suit)]
            self.symbol = self.suit

    def __repr__(self):
        return self.name.title()

    def __eq__(self, other):
        self._block_cross_type_comaprisons(other)
        return self.symbol == other.symbol

    def __lt__(self, other):
        # We compare by alphabetical order (English ranking)
        self._block_cross_type_comaprisons(other)
        return self.NAMES.index(self.name) < self.NAMES.index(other.name)
