import discord
from discord.ext import commands

import colour
import re


class ToColor(commands.Converter):
    async def convert(self, ctx, argument):
        argument = argument.replace(' ', '').lower()
        # search for RGB Color codes
        match = re.match(r'^\([0-9]+,[0-9]+,[0-9]+\)$', argument)
        if match:
            rgb = match.group(0).strip('()').split(',')  # make tuple of match
            # make every entry in tuple the percentage of 255
            return colour.Color(rgb=(int(x) / 255 for x in rgb))
        elif argument.startswith('0x'):  # search for color codes with prefix 0x
            argument = '#' + argument[2:]
        return colour.Color(argument)


class Fun(commands.Cog):

    """Fun or Utility Commands"""

    def __init__(self, bot):
        self.bot = bot
        self.emoji = '⚽'

    @commands.command()
    async def color(self, ctx, *, query: ToColor):
        await ctx.send(query)

    @color.error
    async def color_error(self, ctx, error):
        if isinstance(error, commands.ConversionError):
            await ctx.send(f'Could not regnonize color. Accepts either HTML Names, HTML Codes, Hex Codes or rgb tuples `(255, 255, 255)`')


def setup(bot):
    bot.add_cog(Fun(bot))
