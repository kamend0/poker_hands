from functools import total_ordering
from itertools import product
from random import shuffle


@total_ordering
class Suit:
    """
    Represents the four suits: clubs, diamonds, hearts, and spades.
    Their cardinality from lowest to highest is in that order.
    """

    NAMES = ["clubs", "diamonds", "hearts", "spades"]
    SYMBOLS = ["♣", "♦", "♥", "♠"]

    def __init__(self, suit: str):
        if not isinstance(suit, str):
            raise TypeError("Suit must be identified by a string")

        self.suit = suit.lower()

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

    def __key(self):
        """Hash key"""
        return (self.name)

    def _block_cross_type_comaprisons(self, other):
        if not isinstance(other, Suit):
            return NotImplemented

    def __repr__(self):
        return self.name.title()

    def __eq__(self, other):
        self._block_cross_type_comaprisons(other)
        return self.symbol == other.symbol

    def __lt__(self, other):
        # We compare by alphabetical order (English ranking)
        self._block_cross_type_comaprisons(other)
        return self.NAMES.index(self.name) < self.NAMES.index(other.name)

    def __hash__(self):
        return hash(self.__key())


@total_ordering
class Rank:
    """
    Represents the rank of a playing card from A to K.
    Comparison operations based on order rather than value; to compare value,
        access that attribute directly.
    """

    # Value tuples are (value, order, proper name)
    RANKS = {
        "A": (11, 1, "ace"),  # Ace-high in straights handled by hand logic
        "2": (2, 2, "2"),
        "3": (3, 3, "3"),
        "4": (4, 4, "4"),
        "5": (5, 5, "5"),
        "6": (6, 6, "6"),
        "7": (7, 7, "7"),
        "8": (8, 8, "8"),
        "9": (9, 9, "9"),
        "10": (10, 10, "10"),
        "J": (10, 11, "jack"),
        "Q": (10, 12, "queen"),
        "K": (10, 13, "king"),
    }

    # "Broadway" usually includes 10, but whatever
    BROADWAY_RANKS = {"ACE": "A", "JACK": "J", "QUEEN": "Q", "KING": "K"}

    def __init__(self, rank: str):
        """Validates rank and sets the order value for easier comparison"""
        if not isinstance(rank, str):
            raise TypeError("Rank must be provided as a string")

        self.rank = rank.upper()

        if self.rank in self.BROADWAY_RANKS:
            # These are acceptable to pass as well, we just convert to
            #   shorthand for convenience
            self.rank = self.BROADWAY_RANKS[self.rank]

        if self.rank not in self.RANKS:
            raise ValueError(f"Invalid rank provided: {self.rank}")

        self.value = self.RANKS[self.rank][0]
        self.order = self.RANKS[self.rank][1]
        self.name = self.RANKS[self.rank][2]

    def __key(self):
        """Hash key"""
        return (self.value)

    def _block_cross_type_comaprisons(self, other):
        if not isinstance(other, Rank):
            return NotImplemented

    def __repr__(self):
        return self.name.title()

    def __eq__(self, other):
        self._block_cross_type_comaprisons(other)
        return self.name == other.name

    def __lt__(self, other):
        self._block_cross_type_comaprisons(other)
        return self.value < other.value

    def __hash__(self):
        return hash(self.__key())


@total_ordering
class Card:
    """
    Represents a playing card, with a Rank and Suit
    Crucially: equality of two cards is based on both their rank and suit.
    This deviates from Poker and many other games; this is crucial for the
    hashability of Cards.
    """

    def __init__(self, rank: int | str, suit: str):
        self.rank = Rank(str(rank))
        self.suit = Suit(suit)

    def __key(self):
        """Hash key"""
        return (self.rank, self.suit)

    def _block_cross_type_comaprisons(self, other):
        if not isinstance(other, Card):
            return NotImplemented

    def __repr__(self):
        return f"{self.rank} of {self.suit}"

    def __eq__(self, other):
        self._block_cross_type_comaprisons(other)
        return self.rank == other.rank and self.suit == other.suit

    def __lt__(self, other):
        self._block_cross_type_comaprisons(other)
        if self.rank < other.rank:
            return True
        elif self.rank == other.rank:
            # Use suits to break ties
            return self.suit < other.suit
        else:
            return False

    def __hash__(self):
        return hash(self.__key())


class Deck:
    """
    Represents a deck of 52 cards, one per rank/suit pair
    """

    def __init__(self, shuffled: bool = False):
        self.cards = [
            Card(rank=rank, suit=suit) for rank, suit in product(Rank.RANKS, Suit.NAMES)
        ]

        if shuffled:
            self.shuffle()

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
