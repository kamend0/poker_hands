from classes import Card, Deck

lower_card = Card(rank=2, suit="hearts")
higher_card = Card(rank="a", suit="clubs")
same_rank_card = Card(rank="a", suit="hearts")
same_card = Card(rank="a", suit="clubs")

assert lower_card < higher_card
assert higher_card.rank == same_rank_card.rank
assert higher_card != same_rank_card  # Must match both rank and suit
assert higher_card == same_card

d = Deck()

assert len(d.cards) == 52

d.shuffle()

assert len(d.cards) == 52

try:
    d.draw(53)
    raise Exception("More than 52 cards were drawn")
except ValueError:
    pass

assert len(d.draw(6)) == 6  # 52 - 6 = 46
assert len(d.draw_hand()) == 5  # 46 - 5 = 41

assert len(d.cards) == 41

print("All tests passed!")
