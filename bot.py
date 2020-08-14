import discord 
from discord.ext import commands

from cogs.utils import database

import cogs


description = """
Utility Bot written by TippTop. Work in Progress
"""

initial_extensions = (
    "cogs.settings",
)

default_prefix = "c!"

bot = commands.Bot(
    command_prefix = commands.when_mentioned_or(default_prefix)
)

@bot.command()
async def test(ctx):
    await ctx.send("test")

@bot.event
async def on_ready():
    print("Bot is ready")

    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print(f"Failed to load extension {extension}: {e}")





bot.run("NzI2Mzg2NTkwNjgyNzEwMDY3.XvciOg.M3pgAlu5kEXkGm5abRhChdKmWgE")




