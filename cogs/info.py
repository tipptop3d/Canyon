import discord
from discord.ext import commands

class Info(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["github", "repositry"])
    async def git(self, ctx):
        """Shows Canyons Git-Repositry"""
        await ctx.send("https://github.com/tipptop3d/Canyon")

def setup(bot):
    bot.add_cog(Info(bot))