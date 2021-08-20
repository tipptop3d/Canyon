from card import WhiteCard

class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
    
    def draw(self, card: WhiteCard):
        self.hand.append(card)

    def discard_cards(self, *cards: WhiteCard):
        for card in cards:
            self.hand.remove(card)

    def play_cards(self, *cards: WhiteCard, blanks: list[str]=None):
        for blank in blanks or []:
            yield WhiteCard(text=blank, pack=-1)
        for card in cards:
            self.hand.remove(card)
            yield card

    def __str__(self):
        cards = "\n".join(str(card) for card in self.hand)
        return f'Name: {self.name}, Cards: \n{cards}'
