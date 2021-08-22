from card import WhiteCard, BlackCard


class CardSet:
    __slots__ = ('name', 'white_cards', 'black_cards', 'official')
    def __init__(self, **_set) -> None:
        self.name = _set['name']

        self.white_cards = []
        for card in _set['white']:
            self.white_cards.append(WhiteCard(**card))

        self.black_cards = []
        for card in _set['black']:
            self.black_cards.append(BlackCard(**card))

        self.official = _set['official']
