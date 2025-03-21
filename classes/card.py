from dataclasses import dataclass
from functools import total_ordering
from .rank import Rank
from .suit import Suit


@total_ordering
@dataclass
class Card:
    """
    Represents a playing card, with a Rank and Suit
    """

    rank: int | str
    suit: str

    def _block_cross_type_comaprisons(self, other):
        if not isinstance(other, Card):
            return NotImplemented

    def __post_init__(self):
        self.rank = Rank(str(self.rank))
        self.suit = Suit(self.suit)

    def __repr__(self):
        return f"{self.rank} of {self.suit}"

    def __eq__(self, other):
        self._block_cross_type_comaprisons(other)
        return self.rank == other.rank

    def __lt__(self, other):
        self._block_cross_type_comaprisons(other)
        return self.rank < other.rank
