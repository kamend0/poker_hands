"""
Goal: provide a hand of n cards; find the available Poker hands within those n cards; 
    return the playable Poker hands in that hand, and rank them (Royal Flush > Flush,
    etc.)
"""

from random import shuffle

from constants import FACES, SUITS, UNIQUE_CARDINALITIES, UNIQUE_VALUES


class Card:
    def __init__(self, rank, suit):
        """
        Rank can either be a string--"ace", "king", "queen", "jack"--or an integer for
            the regular number cards.
        Suit is one of the four suits: "spade", "club", "diamond", "heart".
        Cardinality is the ordering of the given card; aces come first, numbers in
            their order, and face cards after, in order of Jack, Queen, then King.
        Value is equal to the number; 10 for faces; 11 for aces.
        """
        self.rank = rank
        self.suit = suit
        self.cardinality = UNIQUE_CARDINALITIES.get(self.rank, self.rank)
        self.value = UNIQUE_VALUES.get(self.rank, self.rank)

    def __repr__(self):
        """
        Represent a Card object as its natural language descriptor
        """
        return f"{str(self.rank).title()} of {self.suit.title()}s"

    def __eq__(self, other):
        """
        Two cards are equal if they have the same rank and suit
        """
        if isinstance(other, Card):
            return (self.rank == other.rank) and (self.suit == other.suit)
        return False


class Deck:
    def __init__(self):
        self._build_deck()

    def _build_deck(self):
        self.cards = []
        for suit in SUITS:
            for rank in ["ace"] + list(range(2, 11)) + FACES:
                self.cards.append(Card(rank=rank, suit=suit))

    def shuffle(self):
        shuffle(self.cards)

    def reshuffle(self):
        self._build_deck()
        self.shuffle()

    def look_through(self):
        for card in self.cards:
            print(card)

    def deal(self, n: int):
        """
        Return list of Cards of length n from deck
        """
        return [self.cards.pop(0) for _ in range(n)]


class PokerHands:
    """
    Class containing logic to find a Poker Hand within the provided cards.
    V1: Analyzes only a set of five cards.
    """

    def __init__(self, cards: list[Card]):
        self.cards = cards
        self.sorted_cards = sorted(cards, key=lambda x: x.cardinality)
        self._find_hands()

    def _find_hands(self):
        self._find_high_card()
        self._find_pairs()
        self._find_three_of_a_kinds()
        self._find_full_houses()
        self._find_four_of_a_kinds()
        self._find_straight()
        self._find_flush()
        self._find_straight_flushes()
        self._find_royal_flush()

        if self.royal_flushes:
            self.score = 9
        elif self.straight_flushes:
            self.score = 8
        elif self.four_of_a_kinds:
            self.score = 7
        elif self.full_houses:
            self.score = 6
        elif self.flushes:
            self.score = 5
        elif self.straights:
            self.score = 4
        elif self.three_of_a_kinds:
            self.score = 3
        elif self.pairs:
            self.score = 2
        else:
            self.score = 1

    """
    DISPLAY METHODS
    Prints various slices of the hand(s) to terminal
    """

    def _list_cards(self, cards: list[Card]):
        return ", ".join([str(card) for card in cards])

    def show_hand(self):
        print("Hand drawn:")
        print(self._list_cards(self.cards))

    def show_best_hand(self):
        print("Best hand:")

        if self.royal_flushes:
            print("Royal Flush: " + self._list_cards(self.royal_flushes[0]))
        elif self.straight_flushes:
            print("Straight Flush: " + self._list_cards(self.straight_flushes[0]))
        elif self.four_of_a_kinds:
            print("Four of a kind: " + self._list_cards(self.four_of_a_kinds[0]))
        elif self.full_houses:
            print("Full house: " + self._list_cards(self.full_houses[0]))
        elif self.flushes:
            print("Flush: " + self._list_cards(self.flushes[0]))
        elif self.straights:
            print("Straight: " + self._list_cards(self.straights[0]))
        # For the remaining hands, show the highest value hands, which will be the
        #   last in the lists, since they're sorted already
        # TODO Two pair -_-
        elif self.three_of_a_kinds:
            print("Three of a kind: " + self._list_cards(self.three_of_a_kinds[-1]))
        elif self.pairs:
            print("Pair: " + self._list_cards(self.pairs[-1]))
        else:
            print("High card: " + str(self.high_card))

    """
    HELPER METHODS:
    The following are used to intepret cards and within the hand-finding logic
    """

    def _all_are_distinct(self, cards: tuple[Card]):
        # Helper method to determine whether all cards in a set are distinct; mainly
        #   to ensure different hands (pairs/threes) are not overlapping
        for i in range(len(cards) - 1):
            for j in range(len(cards)):
                if cards[i] == cards[j]:
                    return False
        return True

    def _all_are_equal_rank(self, cards: list[Card]):
        return all([card.rank == cards[0].rank for card in cards])

    def _all_are_equal_suit(self, cards: list[Card]):
        return all([card.suit == cards[0].suit for card in cards])

    def _all_are_in_cardinal_order(self, cards: list[Card]):
        return all(
            [
                (cards[i].cardinality + 1) == cards[i + 1].cardinality
                for i in range(len(cards) - 1)
            ]
        )

    def _find_n_of_a_kind(self, n: int = 2):
        """
        Loop through sorted cards with a sliding window of size x, and return a list of
        tuples of those found
        """
        hits = []
        for i in range(len(self.sorted_cards) - n + 1):
            card_set = self.sorted_cards[i : i + n]
            if self._all_are_equal_rank(cards=card_set):
                hits.append(tuple(card_set))

        return hits

    """
    FIND METHODS:
    Finds the present hands in the comprising cards and saves to class attributes.
    """

    def _find_high_card(self):
        # High card is the highest-value card in hand. By definition, there can only
        #   be one. Check first for the value, but if there are multiple face cards,
        #   then rely on cardinality
        self.high_card = max(
            self.cards, key=lambda card: (card.value, card.cardinality)
        )

    def _find_pairs(self):
        # A pair is two cards of any suit sharing the same rank
        # Note that not all cards in all pairs will necessarily be unique; a three of a
        #   kind will result in two pairs each sharing a card
        self.pairs = self._find_n_of_a_kind(n=2)

    def _find_three_of_a_kinds(self):
        # A three of a kind is three cards of any suit sharing the same rank
        # Similar note to pairs, but with four of a kinds
        self.three_of_a_kinds = self._find_n_of_a_kind(n=3)

    def _find_four_of_a_kinds(self):
        # A three of a kind is three cards of any suit sharing the same rank
        self.four_of_a_kinds = self._find_n_of_a_kind(n=4)

    def _find_full_houses(self):
        # A full house is a pair and a three of a kind
        # Leverages previous pair/three-of-a-kind logic and attributes
        # TODO This does not generalize to hands larger than 5
        # TODO This doesn't work
        self.full_houses = []

        if self.three_of_a_kinds:
            print("-------")

            for pair in self.pairs:
                for three in self.three_of_a_kinds:
                    # Ensure that no cards comprising the pair is also present in
                    #   the three of a kind
                    print(
                        "Checking for distinction between the following: "
                        + str(pair)
                        + ", "
                        + str(three)
                    )
                    if self._all_are_distinct(pair + three):
                        self.full_houses.append(pair + three)

    def _find_flush(self):
        # A flush is a set of five cards which all share the same suit
        # Because a hand is only five cards, a whole hand is either a flush or not
        # TODO This does not generalize to hands larger than 5. For that, would need
        #   to account for various orderings of cards and stuff
        self.flushes = []
        if self._all_are_equal_suit(cards=self.cards):
            self.flushes.append(tuple(self.sorted_cards))

    def _is_a_high_straight(self):
        # Special case of straight which breaks regular cardinality and counts for a
        #   stronger hand if also a flush (Royal Flush)
        high_straight_ranks = ["ace", 10, "jack", "queen", "king"]
        return all(
            [
                self.sorted_cards[i].rank == high_straight_ranks[i]
                for i in range(len(self.sorted_cards))
            ]
        )

    def _find_straight(self):
        # A straight is a set of five cards which are "in order": 2 through 6,
        #   or 8, 9, J, Q, K. Ace counts as either first when followed by 2, or last
        #   when following K. In the latter case, we check it directly as a special case
        self.straights = []

        if self._is_a_high_straight() or self._all_are_in_cardinal_order(
            cards=self.sorted_cards
        ):
            self.straights.append(tuple(self.sorted_cards))

    def _find_straight_flushes(self):
        # A straight flush is a straight with all of the same suit that is *not* a
        #   royal flush
        self.straight_flushes = []
        if self.straights and self.flushes and not self._is_a_high_straight():
            self.straight_flushes.append(tuple(self.sorted_cards))

    def _find_royal_flush(self):
        # A royal flush is a high straight which is also a flush
        self.royal_flushes = []
        if self._is_a_high_straight() and self.flushes:
            self.royal_flushes.append(tuple(self.sorted_cards))
