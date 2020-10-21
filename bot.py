import sys
import traceback

import discord
from discord.ext import commands

import cogs
from cogs.utils import config, database
from cogs.utils.embeds import MyEmbeds as embeds

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
async def test(ctx, arg1, arg2):
    await ctx.send(f"{arg1}, {arg2}")

@bot.event
async def on_ready():
    print(f"Bot is ready on Python version {sys.version}")

    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print(f"Failed to load extension {extension}: {e}")


bot.run(config.BOT_TOKEN)
