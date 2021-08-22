import asyncio
import sys
from difflib import SequenceMatcher
import logging
from pathlib import Path

import aiohttp
import asqlite
import discord
from discord.ext import commands

from cogs.utils import config

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(
    filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter(
    '%(asctime)s:%(levelname)s: %(message)s'))
logger.addHandler(handler)

BASE_DIR = Path(__file__).parent.parent


class MyContext(commands.Context):
    async def add_reaction(self, *args, **kwargs) -> None:
        await self.message.add_reaction(*args, **kwargs)

    async def remove_reaction(self, *args, **kwargs) -> None:
        await self.message.remove_reaction(*args, **kwargs)

    async def clear_reaction(self, *args, **kwargs) -> None:
        await self.message.clear_reaction(*args, **kwargs)

    async def clear_reactions(self, *args, **kwargs) -> None:
        await self.message.clear_reactions(*args, **kwargs)


class CanyonBot(commands.Bot):

    """Experimenting Bot by TippTop"""

    def __init__(self, command_prefix, help_command, **options):
        super().__init__(command_prefix, help_command=help_command, **options)

    async def on_ready(self):
        print(f'Bot is ready on Python version {sys.version}\n{__file__=}')

        for extension in config.INITIAL_EXTENSIONS:
            try:
                self.load_extension(extension)
            except Exception as e:
                print(f'Failed to load extension {extension}: {e}')

    async def get_context(self, message: discord.Message) -> MyContext:
        return await super().get_context(message, cls=MyContext)

    async def on_command_error(self, ctx: MyContext, error: commands.CommandError):
        if isinstance(error, commands.NotOwner):
            pass

        if isinstance(error, commands.CommandNotFound):
            await ctx.add_reaction('❓')
            name = ctx.invoked_with
            suggestions = []

            for command in self.walk_commands():
                if any([command.hidden, getattr(command.cog, 'hidden', False)].extend([cmd.hidden for cmd in command.parents])):
                    continue
                for alias in (command.name, *command.aliases):
                    ratio = SequenceMatcher(None, name, alias).quick_ratio()
                    if ratio > 0.72:
                        if command.root_parent:
                            alias = f'{command.full_parent_name} {alias}'
                        suggestions.append((ratio, alias))
                        break

            suggestions.sort(key=lambda item: item[0], reverse=True)
            str_suggestions = '\n'.join(
                f'> {ctx.prefix}**{alias}** ({ratio:.0%})'
                for ratio, alias in suggestions)

            if str_suggestions:
                await ctx.reply(f'Maybe you mean:\n{str_suggestions}')

        elif isinstance(error, commands.DisabledCommand):
            await ctx.send('This command is currently disabled')

        elif isinstance(error, commands.NSFWChannelRequired):
            await ctx.send('This command is only usable in NSFW-channels')

        elif isinstance(error, commands.BotMissingPermissions):
            missing_perms = ', '.join(
                f'`{perm}`' for perm in error.missing_perms)
            await ctx.send(f'I am missing permissions to perform this command.\
                            Please inform an Admin if this is not intended.\n \
                            Missing Permissions: {missing_perms}')

        elif isinstance(error, commands.NoPrivateMessage):
            await ctx.author.send('This command is not usable in private messages')


default_prefix = 'c!'

intents = discord.Intents.default()
intents.members = True

bot = CanyonBot(
    command_prefix=commands.when_mentioned_or(default_prefix),
    help_command=commands.MinimalHelpCommand(),
    intents=intents
)


@bot.command()
async def candgranyon(ctx: MyContext):
    await ctx.send('https://www.youtube.com/watch?v=ANiRJpjeqoM')


async def startup() -> None:
    async with aiohttp.ClientSession() as session:
        async with asqlite.connect(BASE_DIR / 'canyon.db') as db:
            bot.session = session
            bot.db = db
            await bot.start(config.BOT_TOKEN)


def main() -> None:
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(startup())
    except KeyboardInterrupt:
        loop.run_until_complete(bot.close())
    finally:
        loop.close()


if __name__ == '__main__':
    main()
