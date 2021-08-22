from typing import Union
import re

import asyncio
from typing import Callable
from discord.ext import commands
from yarl import URL


async def multiple_wait_for(bot: commands.bot.Bot,
                            events: list[dict[str, int, Callable]]):
    done, pending = await asyncio.wait([
        bot.wait_for(event['event_type'], timeout=event['timeout'],
                     check=event['check']) for event in events
    ], return_when=asyncio.FIRST_COMPLETED)
    try:
        stuff = done.pop().result()
    except asyncio.TimeoutError:
        stuff = asyncio.TimeoutError
    for future in done:
        future.exception()

    for future in pending:
        future.cancel()

    return stuff


def remove_duplicates_n(lis, n):
    seen = set()
    for item in lis:
        if item[n] not in seen:
            yield item
            seen.add(item[n])


def to_hyperlink(match: re.Match, url: URL, arg: str) -> str:
    """Converts the match to a hyperlink discord mark"""
    text = match.group(0)
    params = dict()
    params[arg] = text.strip('[]')
    return f'{text}({url % params})'


def add_hyperlinks(text: str, url: URL, arg: str) -> str:
    """Adds a hyperlink to every occurence of [...]"""
    return re.sub(r'\[.*?\]', lambda m: to_hyperlink(m, url, arg), text)
