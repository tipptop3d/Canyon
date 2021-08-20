import discord
from discord.ext import commands

from .utils import database 

class Google(commands.Cog):

    """Commands related on Google API"""

    def __init__(self, bot):
        self.bot = bot
        self.emoji = '🔍'

    @commands.command()
    async def image(self, ctx, query : str):
        pass

# //*[@id='islrg']/div[1]/div[1]/a[1]/div[1]/img


def setup(bot):
    bot.add_cog(Google(bot))
