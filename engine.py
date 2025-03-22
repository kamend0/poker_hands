from collections import Counter
from itertools import combinations


from classes import Card


"""
Logic to discover Poker Hands in a set of five cards
"""


def is_high_straight(cards: list[Card]) -> bool:
    """
    Helper function used to both take care of the ace-high exception for straights, as
    well as help identify royal flushes from regular straight flushes.
    """
    return sorted([c.rank.order for c in cards]) == [1, 10, 11, 12, 13]


def find_hands(cards: list[Card]) -> dict:
    """
    Given a set of five cards, find all available Poker hands.

    Returns a dictionary of all possible hands, whose values indicate the cards in the
    hand which comprise them. If none are found, the values are empty lists.
    For those hands which it is possible to have multiple ways to make (e.g., pairs
    when there are >= 3 occurences of a given rank), its corresponding value is a list
    of tuples.
    For those hands which it is only possible to make a single way (e.g., a straight),
    then a tuple of the hand is returned ordered in a sensible way (this mainly has to
    do with straights of ace-low vs. ace-high).
    """
    high_card: Card = max(cards)  # Too simple to need a function
    pairs: list[tuple[Card]] = find_matching_ranks(cards, 2)
    two_pairs: list[tuple[Card]] = find_two_pairs(pairs)
    toaks: list[tuple[Card]] = find_matching_ranks(cards, 3)
    straight: tuple[Card] = find_straight(cards)
    flush: tuple[Card] = find_flush(cards)
    full_house: tuple[Card] = find_full_house(cards)
    foaks: tuple[Card] = find_matching_ranks(cards, 4)
    # Both straight flushes and royal flushes are trivial with our work so far
    straight_flush: tuple[Card] = (
        tuple(sorted(cards, key=lambda c: (c.rank.value, c.rank.order, c.suit)))
        if straight and flush
        else ()
    )
    royal_flush: tuple[Card] = (
        tuple(sorted(cards, key=lambda c: (c.rank.value, c.rank.order, c.suit)))
        if straight_flush and is_high_straight(cards)
        else ()
    )

    return {
        "high card": high_card,
        "pairs": pairs,
        "two pairs": two_pairs,
        "three of a kinds": toaks,
        "straight": straight,
        "flush": flush,
        "four of a kinds": foaks,
        "straight flush": straight_flush,
        "full house": full_house,
        "royal flush": royal_flush,
    }


"""
HAND-SPECIFIC FUNCTIONS
"""


def find_matching_ranks(cards: list[Card], n: int) -> list[tuple[Card]] | tuple[Card]:
    """
    For a given set of cards, find all sets of matching ranks of size n; for instance,
    n = 2 finds all pairs; n = 3, all three-of-a-kinds.

    Returns a list of tuples showing all possible combinations; e.g., if there are three
    2s in the hand, returns all six possible combinations of those three 2s in the form
    of a list of six tuples.
    Special case: four-of-a-kinds are returned as a single tuple because there is only
    one possible way to make a four-of-a-kind with a hand of five drawn from a standard
    deck of cards.
    """
    combos = []

    # First: count occurences of each rank in the given hand
    card_rank_counts = Counter([c.rank for c in cards])

    for card_rank, count in card_rank_counts.items():
        if count >= n:
            # Find all possible combinations of two cards
            # Trivial if there are 2; n! for n > 2
            ranks_in_hand = [c for c in cards if c.rank == card_rank]
            combos.extend(combinations(ranks_in_hand, n))

    if combos and n == 4:
        # Only one possible way to make four-of-a-kind with a hand of five cards
        return tuple(combos[0])

    return combos


def find_two_pairs(pairs: list[tuple[Card]]) -> list[tuple[Card]]:
    """
    Finds all two pairs, which is a hand consisting of two distinct pairs, e.g.,
    a pair of twos and a pair of threes.

    A four-of-a-kind does not count as a two pair, but a full house necessarily always
    contains a two pair. If you havbe a full house, then there are two possible two
    pairs you could play.
    """
    two_pairs = []

    for pair1, pair2 in combinations(pairs, 2):
        # If the two pairs are unique, they can be used
        if not set(pair1) & set(pair2):
            two_pairs.append(pair1 + pair2)

    return two_pairs


def find_straight(cards: list[Card]) -> tuple[Card]:
    """
    Find straights, hands consisting of incrementally increasing rank, e.g,
    [2, 3, 4, 5, 6]. Ace-low, e.g., [A, 2, 3, 4, 5] and ace-high, e.g., [10, J, Q, K, A]
    are both valid straights.
    """
    # First: check for special case of ace-high
    if is_high_straight(cards):
        # Return such that Ace is ranked high
        return tuple(sorted(cards, key=lambda c: (c.rank.value, c.rank.order)))

    # Otherwise, business as usual: check for strictly- and incrementally-increasing
    # rank order
    ordered_ranks = sorted([c.rank.order for c in cards])

    for i in range(len(ordered_ranks) - 1):
        if (ordered_ranks[i] + 1) != ordered_ranks[i + 1]:
            return ()

    return tuple(sorted(cards, key=lambda c: (c.rank.order)))


def find_flush(cards: list[Card]) -> tuple[Card]:
    if len(set([c.suit for c in cards])) == 1:
        return tuple(cards)
    return ()


def find_full_house(cards: list[Card]) -> tuple[Card]:
    """
    For a given set of cards, find all full houses, which is a hand consisting of a pair
    and a three-of-a-kind. By definition, and limitation of a hand size to 5, there can
    only ever be a single arrangement, so no usage of combinatoric functions is needed.

    Returns tuple of cards in hand, rank-ordered.
    """
    card_rank_counts = Counter([c.rank for c in cards])
    if len(card_rank_counts) == 2 and sorted(card_rank_counts.values()) == [
        2,
        3,
    ]:
        return tuple(sorted(cards, key=lambda c: c.rank))
    return ()
