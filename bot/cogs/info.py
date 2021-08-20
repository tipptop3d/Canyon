import discord
from discord.ext import commands

class Info(commands.Cog):
    """Infos about the Bot and the bot creator"""


    def __init__(self, bot):
        self.bot = bot
        self.emoji = '📙'

    @commands.command()
    async def creator(self, ctx):
        """Shows the owner of the bot""" 

        if bot_owner := ctx.guild.get_member(self.bot.owner_id):
            await ctx.send(f'{bot_owner.mention} has written me 😊')
        else:
            await ctx.send('TippTop#0155 has written me 😊')

    @commands.command(aliases=['github', 'repository', 'source'])
    async def git(self, ctx):
        """Shows Canyon's Git-Repository"""
        await ctx.send('https://github.com/tipptop3d/Canyon')



def setup(bot):
    bot.add_cog(Info(bot))