import random
from cardset import CardSet

class Deck:
    def __init__(self, *sets: CardSet):
        self.white = []
        self.black = []
        for _set in sets:
            self.white.extend(_set.white_cards)
            self.black.extend(_set.black_cards)
        random.shuffle(self.white)
        random.shuffle(self.black)
        