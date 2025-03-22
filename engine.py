from collections import Counter
from itertools import combinations
from time import sleep

from classes import Card, Deck

"""
Logic to discover Poker Hands in a set of five cards
"""

def find_matching_ranks(cards: list[Card], n: int) -> list[tuple[Card]]:
    """
    For a given set of cards, find all sets of matching ranks of size n;
    for instance, n = 2 finds all pairs; n = 3, all three-of-a-kinds.

    Returns a list of tuples showing all possible combinations; e.g., if there
    are three 2s in the hand, returns all six possible combinations of those
    three 2s in the form of a list of six tuples
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

    return combos


