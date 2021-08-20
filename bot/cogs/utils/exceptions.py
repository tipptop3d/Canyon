import discord
from discord.ext import commands

class AInotImplemented(commands.CommandError):
    pass

class CurrencyNotFound(commands.BadArgument):
    pass