import re
from datetime import datetime
import dateutil.parser

import aiohttp
import discord
from discord.ext import commands
from yarl import URL

from .utils import config
from .utils.funcs import add_hyperlinks


class UrbanDicEntry:
    __slots__ = ('definition', 'link', 'thumbs_up', 'thumbs_down', 'sound_urls',
                'author', 'word', 'id', 'current_vote', 'written_on', 'example')

    base_url = URL('https://www.urbandictionary.com/define.php')

    def __init__(self, **kwargs) -> None:
        self.definition: str = add_hyperlinks(
            kwargs.get('definition'), self.base_url, 'term')
        self.link: str = kwargs.get('permalink')
        self.thumbs_up: int = kwargs.get('thumbs_up')
        self.thumbs_down: int = kwargs.get('thumbs_down')
        self.sound_urls: tuple[str] = tuple(kwargs.get('sound_urls'))
        self.author: str = kwargs.get('author')
        self.word: str = kwargs.get('word')
        self.id: int = kwargs.get('id')
        self.current_vote: str = kwargs.get('current_vote')
        self.written_on: datetime = dateutil.parser.isoparse(
            kwargs.get('written_on'))
        self.example: str = add_hyperlinks(
            kwargs.get('example'), self.base_url, 'term')

    @property
    def like_diff(self) -> int:
        return self.thumbs_up - self.thumbs_down

    def create_embed(self) -> discord.Embed:
        return discord.Embed(
            title=self.word,
            color=discord.Color(0x171f36),
            url=self.link,
            description=self.definition,
            timestamp=self.written_on
        ).set_author(
            name='Urban Dictionary',
            url='https://www.urbandictionary.com/'
        ).set_footer(
            text='Written on'
        ).add_field(
            name='Examples:',
            value=self.example,
            inline=False
        ).add_field(
            name='\u200b',
            value=f'👍{self.thumbs_up} ─ 👎{self.thumbs_down}',
            inline=False
        )

class toTerm(commands.Converter):
    async def convert(self, ctx, argument: str) -> str:
        if len(argument) < 2:
            raise commands.BadArgument('Term has to be at least 2 characters long')
        return argument

class TermNotFound(commands.BadArgument):
    pass
        

class UrbanDictionary(commands.Cog):

    """Search up the Urban Dictionary for definitions you never heard about"""

    url = URL('http://api.urbandictionary.com/v0/define')

    def __init__(self, bot):
        self.bot = bot
        self.emoji = '📖'

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error: commands.CommandError) -> None:
        if isinstance(error, TermNotFound):
            await ctx.reply(error)
        elif isinstance(error, commands.BadArgument):
            await ctx.reply(error)

    @commands.group(invoke_without_command=True, aliases=['u'])
    async def urban(self, ctx, *, term: toTerm):
        """Gives you the most popular definitions for the giving term"""
        async with self.bot.session.get(self.url, params={'term': term}) as response:
            definitions = (await response.json())['list']
        
        if not definitions:
            raise TermNotFound(f'No definition for term {term} found')

        entries = [UrbanDicEntry(**entry) for entry in definitions]
        entries.sort(key=lambda elem: elem.like_diff, reverse=True)
        top_entry = entries[0]
        await ctx.send(embed=top_entry.create_embed())

    @urban.command(aliases=['new'])
    async def newest(self, ctx, *, term: str):
        """Gives you the newest definition for the giving term"""
        async with self.bot.session.get(self.url, params={'term': term}) as response:
            definitions = (await response.json())['list']
      
        if not definitions:
            raise TermNotFound(f'No definition for term {term} found')

        entries = [UrbanDicEntry(**entry) for entry in definitions]
        entries.sort(key=lambda elem: elem.written_on,reverse=True)
        top_entry = entries[0]
        await ctx.send(embed=top_entry.create_embed())


def setup(bot):
    bot.add_cog(UrbanDictionary(bot))
