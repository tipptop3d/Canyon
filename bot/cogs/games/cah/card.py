class Card:
    __slots__ = ('text', 'pack')
    def __init__(self, **card) -> None:
        self.text = card['text']
        self.pack = card['pack']


class WhiteCard(Card):
    def __str__(self) -> str:
        return f'"{self.text}"'
    


class BlackCard(Card):
    __slots__ = ('pick')
    def __init__(self, **card):
        super().__init__(**card)
        self.pick = card['pick']
    
    def __str__(self) -> str:
        return f'"{self.text.replace("_", "_"*5)}" Pick: {self.pick}'
