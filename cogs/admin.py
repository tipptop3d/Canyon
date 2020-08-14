import discord
from discord.ext import commands

from .utils import database 

class Admin(commands.Cog):

    """Debugging and Admin-Only Commands"""
++
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["eval"])
    @commands.is_owner()
    async def evaluate(self, ctx, *, code):
        """Evaluates a python expression"""

        await ctx.send(f"Code to evaluate: {code}")

        try:
            await ctx.send(eval(code.strip("`")))
        except SyntaxError as e:
            await ctx.send(f"Some kind of Syntax Error occured: {e}")
        except Exception as e:
            await ctx.send(f"An Error occured: {e}")
        else:
            await ctx.send("Evaluated Code")

    @commands.command(aliases=["exec", "code"])
    @commands.is_owner()
    async def execute(self, ctx, *, code):
        """Executes a code snippet"""

        try:
            exec(code.strip("`"))
        except SyntaxError as e:
            await ctx.send(f"Some kind of Syntax Error occured: {e}")
        except Exception as e:
            await ctx.send(f"An Error occured: {e}")
        else:
            await ctx.send("Executed Code")


    @commands.command()
    @commands.is_owner()
    async def load(self, ctx, *, module : str):
        """Loads a module"""

        try:
            self.bot.load_extension(module)
        except Exception as e:
            await ctx.send(f"Failed loading Extension: {e}")
        else:
            await ctx.send("Loaded extention")


    @commands.command()
    @commands.is_owner()
    async def unload(self, ctx, *, module : str):
        """Unloads a module"""

        try:
            self.bot.unload_extension(module)
        except Exception as e:
            await ctx.send(f"Failed unloading Extension: {e}")
        else:
            await ctx.send("Unloaded extention")


    @commands.command(name='reload')
    @commands.is_owner()
    async def _reload(self, ctx, *, module : str):
        """Reloads a module"""

        try:
            self.bot.reload_extension(module)
        except Exception as e:
            await ctx.send(f"Failed reloading Extension: {e}")
        else:
            await ctx.send("Reloaded extention")


def setup(bot):
    bot.add_cog(Admin(bot))
    