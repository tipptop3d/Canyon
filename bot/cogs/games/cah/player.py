from card import WhiteCard
from typing import Iterator


class Player:
    __slots__ = ('name', 'hand', 'points', 'blanks')

    def __init__(self, name: str, blanks: int = 1) -> None:
        self.name = name
        self.hand = []
        self.points = 0
        self.blanks = blanks

    def __eq__(self, other):
        return self.name == other.name and self.hand == other.hand

    def __hash__(self):
        return hash(self.name)

    def __str__(self) -> str:
        cards = "\n".join(str(card) for card in self.hand)
        return f'Name: {self.name}, Cards: \n{cards}'

    def show_hand(self) -> str:
        return '\n'.join(f'{i+1}: {card}' for i,
                         card in enumerate(self.hand))

    def draw(self, card: WhiteCard) -> None:
        self.hand.append(card)

    def discard_cards(self, *cards: WhiteCard) -> None:
        for card in cards:
            self.hand.remove(card)

    def discard_cards_by_index(self, *indexes: int) -> Iterator[WhiteCard]:
        discarded_cards = {self.hand[i] for i in indexes}
        return self.discard_cards(*discarded_cards)

    def play_cards(self, *cards: WhiteCard) -> Iterator[WhiteCard]:
        for card in cards:
            self.hand.remove(card)
            yield card

    def play_cards_by_index(self, *indexes: int) -> Iterator[WhiteCard]:
        played_cards = {self.hand[i] for i in indexes}
        return self.play_cards(*played_cards)

    def add_point(self):
        self.points += 1
