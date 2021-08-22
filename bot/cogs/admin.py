import datetime
import sys
import traceback
from typing import Optional

import discord
from discord.ext import commands

from .utils import config
from .utils.embeds import MyEmbeds as embeds


class Admin(commands.Cog):

    """Debugging owner-only Commands"""

    def __init__(self, bot):
        self.bot = bot
        self.hidden = True
        self.emoji = '🔬'

        self.last_reloaded = None

    @commands.command(hidden=True)
    @commands.is_owner()
    async def load(self, ctx, *, module: str):
        """Loads a module"""

        try:
            self.bot.load_extension(f'cogs.{module}')
        except Exception as e:
            await ctx.send(embed=embeds.create_error('Failed loading Extension', str(e)))
        else:
            await ctx.send(embed=embeds.create_success('Success', 'Successfully loaded extension'))

    @commands.command(hidden=True)
    @commands.is_owner()
    async def unload(self, ctx, *, module: str):
        """Unloads a module"""

        try:
            self.bot.unload_extension(f'cogs.{module}')
        except Exception as e:
            await ctx.send(embed=embeds.create_error('Failed unloading Extension', str(e)))
        else:
            await ctx.send(embed=embeds.create_success('Success', 'Successfully unloaded extension'))

    @commands.command(name='reload', hidden=True)
    @commands.is_owner()
    async def _reload(self, ctx, *, module: Optional[str]):
        """Reloads a module. If no module is given, the last module reloaded will be reloaded"""
        if not module:
            module = self.last_reloaded
        else:
            self.last_reloaded = module

        try:
            self.bot.reload_extension(f'cogs.{module}')
        except Exception as e:
            await ctx.send(embed=embeds.create_error('Failed reload Extension', str(e)))
        else:
            await ctx.send(embed=embeds.create_success('Success', 'Successfully reloaded extension'))

    @commands.command(hidden=True)
    @commands.is_owner()
    async def reloadall(self, ctx):
        """Reloads all modules"""

        log = []
        succeeded = 0

        for module in config.INITIAL_EXTENSIONS:
            try:
                self.bot.reload_extension(f'{module}')
            except Exception as e:
                log.append(
                    f'```diff\n- Failed reloading extension {module}: {str(e)}```')
            else:
                succeeded += 1
                log.append(
                    f'```diff\n+ Successfully reloaded extension {module}```')

        embed = discord.Embed(
            title=f'Reloaded {succeeded}/{len(config.INITIAL_EXTENSIONS)} cogs',
            description='\n'.join(log)
        )

        await ctx.reply(embed=embed)


def setup(bot):
    bot.add_cog(Admin(bot))
