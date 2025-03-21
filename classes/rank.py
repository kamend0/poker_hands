from dataclasses import dataclass
from functools import total_ordering


@total_ordering
@dataclass
class Rank:
    """
    Represents the rank of a playing card from A to K.
    Comparison operations based on order rather than value; to compare value,
        access that attribute directly.
    """

    rank: str

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

    def _block_cross_type_comaprisons(self, other):
        if not isinstance(other, Rank):
            return NotImplemented

    def __post_init__(self):
        """Validates rank and sets the order value for easier comparison"""
        if not isinstance(self.rank, str):
            raise TypeError("Rank must be provided as a string")

        self.rank = self.rank.upper()

        if self.rank in self.BROADWAY_RANKS:
            # These are acceptable to pass as well, we just convert to
            #   shorthand for convenience
            self.rank = self.BROADWAY_RANKS[self.rank]

        if self.rank not in self.RANKS:
            raise ValueError(f"Invalid rank provided: {self.rank}")

        self.value = self.RANKS[self.rank][0]
        self.order = self.RANKS[self.rank][1]
        self.name = self.RANKS[self.rank][2]

    def __repr__(self):
        return self.name.title()

    def __eq__(self, other):
        self._block_cross_type_comaprisons(other)
        return self.value == other.value

    def __lt__(self, other):
        self._block_cross_type_comaprisons(other)
        return self.value < other.value
