import discord
from discord.ext import commands
import sys

from cogs.utils import database, config

import cogs


description = """
Utility Bot written by TippTop. Work in Progress
"""

initial_extensions = (
    "cogs.settings",
    "cogs.admin",
    "cogs.info"
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
    print(f"Bot is ready on Python version {sys.version}")

    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print(f"Failed to load extension {extension}: {e}")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredAguments):
        pass



bot.run(config.BOT_TOKEN)




