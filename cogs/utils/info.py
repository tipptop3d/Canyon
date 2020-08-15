import discord
from discord.ext import commands

class Info(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def git(self, ctx):
        await ctx.send(embed=discord.Embed(
            title = "Canyon Git-Repositry",
            url = "https://github.com/tipptop3d/Canyon",
            color = 0x0f0f0f
        ).set_footer(
            text = f"Requested by"
        ))

def setup(bot):
    bot.add_cog(Info(bot))