import discord
from discord.ext import commands

class Info(commands.Cog):
    """Infos about the Bot"""


    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def creator(self, ctx):
        """Shows the owner of the bot"""

        bot_owner = ctx.guild.get_member(398926591859752960)

        if bot_owner:
            await ctx.send(f"{bot_owner.mention} has written me 😊")
        else:
            await ctx.send("TippTop#0155 has written me 😊")

    @commands.command(aliases=["github", "repositoriy"])
    async def git(self, ctx):
        """Shows Canyons Git-Repositry"""
        await ctx.send("https://github.com/tipptop3d/Canyon")



def setup(bot):
    bot.add_cog(Info(bot))