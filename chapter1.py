# special methods
import collections

Card = collections.namedtuple('Card', ['rank', 'suit'])

class Cards:
    ranks = [str(n) for n in range(2, 11)] + list('JQKA')
    suits = 'spades diamonds clubs hearts'.split()

    def __init__(self):
        self.c = [Card(rank, suit) for suit in self.suits
                        for rank in self.ranks]

    def __repr__(self):
        return f'Cards({self.c!r})'

    def __len__(self):
        return len(self.c)

    def __getitem__(self, item):
        return self.c[item]

c = Cards()
print(c)
print(len(c))

# get a random card
from random import choice
print(choice(c))

# sort

suit_values = dict(spades=3, hearts=2, diamonds=1, clubs=0)

def spades_high(card):
    rank_value = Cards.ranks.index(card.rank)
    return rank_value * len(suit_values) + suit_values[card.suit]

for card in sorted(c, key=spades_high): # doctest: +ELLIPSIS
    print(card)



