from classes import Deck, PokerHands

"""
I want to answer this question:
"Are these N cards an X?"
Where N is a number and X is a Poker hand: pair, three of a kind, etc.
"""

score = 0

print("Looking for a full house...")
while score != 6:
    deck = Deck()
    deck.shuffle()

    hand = PokerHands(cards=deck.deal(n=5))

    score = hand.score

    if score == 6:
        print("Found it!\n")
        hand.show_hand()
        print("\n")
        hand.show_best_hand()
