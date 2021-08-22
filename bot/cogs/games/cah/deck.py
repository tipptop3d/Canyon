import random
from cardset import CardSet

class Deck:
    __slots__ = ('white', 'black')
    def __init__(self, *sets: CardSet):
        self.white = []
        self.black = []
        for _set in sets:
            self.white.extend(_set.white_cards)
            self.black.extend(_set.black_cards)
        self.shuffle()

    def shuffle(self):
        self.shuffle_w()
        self.shuffle_b()

    def shuffle_w(self):
        random.shuffle(self.white)
    
    def shuffle_b(self):
        random.shuffle(self.black)