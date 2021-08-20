class Card:
    def __init__(self, card: dict[str, int]):
        self.text = card['text']
        self.pack = card['pack']

class WhiteCard(Card):
    pass

class BlackCard(Card):
    def __init__(self, card: dict[str, int, int]):
        super().__init__(card)
        self.pick = card['pick']
