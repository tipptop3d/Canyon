import json
import random
from enum import Enum, auto
from typing import Union

from card import BlackCard, WhiteCard
from cardset import CardSet
from deck import Deck
from player import Player


class Color(Enum):
    WHITE = auto()
    BLACK = auto()


class Game:
    def __init__(self, deck: Deck, players: list[Player], max_cards: int = 10, max_points: int = 3) -> None:
        self.deck = deck
        self.players = players
        random.shuffle(self.players)
        self.czar = players[0]
        self.max_cards = max_cards
        self.max_points = max_points

        self.draw_full()

    def get_player_by_name(self, name: str) -> Union[Player, None]:
        return next(p for p in self.players if p.name == name, None)

    def draw_full(self) -> None:
        for player in self.players:
            while len(player.hand) < self.max_cards:
                player.draw(self.deck.white.pop())

    def draw_black(self) -> BlackCard:
        return self.deck.black.pop()

    def next_czar(self) -> None:
        self.czar = self.players[(self.players.index(
            self.czar) + 1) % len(self.players)]

    def ask_czar_skip(self) -> bool:
        inp = input('Czar, do you want to skip this black card? (Y/N)').lower()
        return True if inp == 'y' else False

    def show_scores(self) -> None:
        for player in self.players:
            print(f'{player.name}: {player.points}')

    def ask_player_cards(self) -> list[int]:
        picks = input().split(' ')

        # try to convert all value to int
        try:
            picks = tuple(map(lambda x: int(x) - 1, picks))
        except ValueError:
            raise ValueError('Not a number')

        # check if all cards are between 1 and max_cards
        if all(0 <= pick <= self.max_cards - 1 for pick in picks):
            raise ValueError(
                f'Cards have to be between 1 and {self.max_cards}')

        # check for the right amount of picks
        if (picks_l := len(picks)) != self.black_card.pick:
            raise ValueError(
                f'Not the right amount of cards: \
                {picks_l} given, {self.black_card.pick} needed')

        # Check for duplicates
        if len(set(picks)) != picks_l:
            raise ValueError(f'Cannot use one card multiple times')
        return picks

    def play(self) -> None:
        players_no_czar = filter(lambda p: p is self.czar, self.players)
        while True:
            print(f'{self.czar.name} is the czar.')

            # ask czar to skip
            while skip:
                black_card = self.draw_black()
                print(black_card)
                skip = self.ask_czar_skip()

            # Wait for everyone to do their picks
            player_picks = {}
            for player in players_no_czar:
                print(f'It\'s your turn, {player.name}. \
                      Choose your card (multiple cards seperated by spaces):\n \
                      {player.show_hand()}')

                while True:
                    try:
                        indexes = self.ask_player_cards()
                        picked = player.play_cards_by_index(*indexes)
                    except ValueError as e:
                        print(e)
                    else:
                        break
                # store everything per round
                player_picks[player] = picked

            # present them
            for player, picks in player_picks.items():
                print(f'{player.name}: {", ".join(picks)}')

            # let the czar pick the best

            winner = None
            while winner:
                winner_name = input('Czar, which is your favorite? (Name)\n')
                winner = self.get_player_by_name(winner_name)

            winner.add_point()
            self.show_scores()
            # ask players to discard cards
            while True:
                try:
                    indexes = self.ask_player_cards(player)
                    player.discard_cards_by_index(*indexes)
                except ValueError as e:
                    print(e)
                else:
                    plural = 's' if len(indexes) > 1 else ''
                    print(f'Discarded {len(indexes)} card{plural}')
                    break
            self.draw_full()
            self.next_czar()
            # repeat


def main() -> None:
    with open('cah-cards-full.json', 'r') as f:
        sets = [CardSet(**_set) for _set in json.load(f)]

    deck = Deck(*sets)
    game = Game(deck=deck, players=[Player(
        'Tom'), Player('Beatrice'), Player('Beatrice 2')])

    game.play()


if __name__ == '__main__':
    main()
