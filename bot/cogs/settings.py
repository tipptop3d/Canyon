import discord
from discord.ext import commands

class Settings(commands.Cog):

    """Commands for setting up the bot"""

    def __init__(self, bot):
        self.bot = bot
        self.emoji = '⚙️'


def setup(bot):
    bot.add_cog(Settings(bot))
    