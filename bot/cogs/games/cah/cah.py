import json
from enum import Enum, auto

from player import Player
from cardset import CardSet
from deck import Deck

class Color(Enum):
    WHITE = auto()
    BLACK = auto()


class Game:
    def __init__(self, deck: Deck, players: list[Player], max_cards: int=7, rounds=30):
        self.deck = deck
        self.players = players
        self.max_cards = max_cards
        self.rounds = rounds
    
    def draw_full(self):
        for player in self.players:
            while len(player.hand) < self.max_cards:
                player.draw(self.deck.white.pop())

def main() -> None:
    with open('cah-cards-full.json', 'r') as f:
        sets = [CardSet(_set) for _set in json.load(f)]

    deck = Deck(*sets)
    game = Game(deck=deck, players=[Player('Tom'), Player('Franz'), Player('Beatrice')])

    game.draw_full()
    for i in game.players:
        print(i)


if __name__ == '__main__':
    main()



