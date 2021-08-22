import discord
from discord.ext import commands
import asyncio
import typing
import re

from .utils.exceptions import AInotImplemented


class Player():

    def __init__(self, color: str):
        self.color = color
        self.symbol = color[0]
        self.won = False

    def __repr__(self):
        return f"Player('{self.color}')"

    def __str__(self):
        return self.color


class Connect4():

    def __init__(self, width=7, height=6, win_con=4, board=None):
        self.board = board if board is not None else [
            [0 for _ in range(width)] for _ in range(height)]
        self.RED = Player('Red')
        self.BLUE = Player('Blue')
        self.WIN_CON = win_con
        self.turn = self.RED

    def __repr__(self):
        return '\n'.join([str(i) for i in self.board])

    def __getitem__(self, item: int):
        return self.board[item]

    def __setitem__(self, item: int, value: str):
        self.board[item] = value

    def _copy(self):
        return Connect4(board=self.board)

    @property
    def height(self) -> int:
        return len(self.board)

    @property
    def width(self) -> int:
        return len(self.board[0])

    @property
    def running(self) -> bool:
        return not (self.RED.won or self.BLUE.won)

    def get_won(self) -> Player:
        return self.RED if self.RED.won else (self.BLUE if self.BLUE.won else None)

    def switch_turn(self):
        self.turn = self.BLUE if self.turn is self.RED else self.RED

    def drop_piece(self, column: int, player: Player) -> tuple[int, int]:
        if not 0 <= column < self.width:
            raise ValueError(f'Column has to be between 1 and {self.width}')
        if self[0][column] != 0:
            raise ValueError('Cannot place more pieces in this column')
        for y in range(self.height):
            if y == self.height - 1 or self[y+1][column] != 0:
                self[y][column] = player
                return column, y

    def check_win(self, last_position: tuple[int, int], player: Player) -> bool:
        """
        Strategy:
            1. from last position: |
                a) count downwards: true if >= 4, else False
            2. from last position: -
                a) count left till no more of color
                b) then count right: true if >= 4, else False
            3. from last position: /
                a) count diagonal up rigth till no more of color
                b) then count diagonal down left: true if >= 4, else False
            4. from last position: \
                a) count diagonal up left till no more of color
                b) then count diagonal down rigth: true if >= 4, else False
        """

        x, y = last_position
        # 1. look down
        try:
            counter = 0
            while self[y+counter][x] is player:
                counter += 1
                if counter >= self.WIN_CON:
                    return True
        except IndexError:  # ignore
            pass

        # 2. look horizontally
        counter_left = 0
        counter_right = 0
        try:
            while self[y][x-counter_left] is player:
                if x-counter_left < 0:  # do not allow negative indexing
                    break
                counter_left += 1
        except IndexError:
            pass
        try:
            # offset by 1, not counting first piece twice
            while self[y][x+1+counter_right] is player:
                counter_right += 1
        except IndexError:
            pass

        if counter_left + counter_right >= self.WIN_CON:
            return True

        # 3. look diagonally /
        counter_upper_right = 0
        counter_bottom_left = 0
        try:
            while self[y-counter_upper_right][x+counter_upper_right] is player:
                if y-counter_upper_right < 0:
                    break
                counter_upper_right += 1
        except IndexError:
            pass
        try:
            while self[y+1+counter_bottom_left][x-1-counter_bottom_left] is player:
                if x-counter_bottom_left < 0:
                    break
                counter_bottom_left += 1
        except IndexError:
            pass

        if counter_upper_right + counter_bottom_left >= self.WIN_CON:
            return True

        # 4. look diagonally \
        counter_upper_left = 0
        counter_bottom_right = 0
        try:
            while self[y-counter_upper_left][x-counter_upper_left] is player:
                if y-counter_upper_left < 0 or x-counter_upper_left < 0:
                    break
                counter_upper_left += 1
        except IndexError:
            pass
        try:
            while self[y+1+counter_bottom_right][x+1+counter_bottom_right] is player:
                counter_bottom_right += 1
        except IndexError:
            pass

        if counter_upper_left + counter_bottom_right >= self.WIN_CON:
            return True

        return False  # win is found


class Games(commands.Cog):

    """Play simple games with your friends in Discord!"""

    def __init__(self, bot):
        self.bot = bot
        self.emoji = '🏓'

    @commands.command()
    async def connect4(self, ctx, opponent: discord.Member):
        if opponent == self.bot.user:
            raise AInotImplemented('Godlike AI is not implemented')
        elif opponent.bot:
            raise AInotImplemented('AI is not implemented')
        else:
            pass

    @commands.command()
    async def debug(self, ctx, emoji: discord.Emoji):
        vs = self.bot.get_emoji(850856551060602910)
        embed = discord.Embed(
            title=f'A {str(vs)} B', description=(str(emoji) * 7 + '\n') * 6)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Games(bot))
