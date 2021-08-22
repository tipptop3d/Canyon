import re
from pathlib import Path

import discord
import pandas
from alpha_vantage.async_support.alphavantage import AlphaVantage as av
from alpha_vantage.async_support.cryptocurrencies import CryptoCurrencies
from discord.ext import commands

from cogs.utils.config import AV_KEY
from cogs.utils.exceptions import CurrencyNotFound

DCL_PATH = Path(__file__).parent.parent / 'data' / 'digital_currency_list.csv'
DIGITAL_CURRENCY_LIST = pandas.read_csv(DCL_PATH).set_index('currency code')


@av._output_format
@av._call_api_on_func
def get_intraday(self, symbol, market='USD', interval='15min', outputsize='compact'):
    _FUNCTION_KEY = 'CRYPTO_INTRADAY'
    return _FUNCTION_KEY, 'Time Series Crypto ({})'.format(interval), 'Meta Data'


CryptoCurrencies.get_intraday = get_intraday


async def get_intraday_data(**kwargs):
    cc = CryptoCurrencies(key=AV_KEY, output_format='pandas')
    data, _ = await cc.get_intraday(**kwargs)
    await cc.close()
    return data


async def get_daily_data(**kwargs):
    cc = CryptoCurrencies(key=AV_KEY, output_format='pandas')
    data, _ = await cc.get_digital_currency_daily(**kwargs)
    await cc.close()
    return data


class toSymbol(commands.Converter):
    async def convert(self, ctx, argument):
        filt = DIGITAL_CURRENCY_LIST['currency name'].str.contains(
            rf'^{argument}$', flags=re.IGNORECASE)
        symbol = DIGITAL_CURRENCY_LIST.loc[filt]
        if not symbol.empty:
            return symbol.index[0]
        elif argument.upper() in DIGITAL_CURRENCY_LIST.index.values:
            return argument.upper()
        raise CurrencyNotFound


class Crypto(commands.Cog):

    """Crypto-Related Data, Intra-Day, Daily, Trading"""

    def __init__(self, bot):
        self.bot = bot
        self.emoji = '\N{COIN}'

    @commands.command()
    async def test(self, ctx):
        embed = discord.Embed(
            title='Test', description='Lorem Lorem Lorem Lorem Lorem Lorem Lorem Lorem Lorem Lorem Lorem Lorem Lorem Lorem Lorem Lorem Lorem Lorem Lorem Lorem Lorem', color=0x00ff00)
        file = discord.File('graphtest smol2.png', filename='image.png')
        embed.set_image(url='attachment://image.png')
        await ctx.send(file=file, embed=embed)

    @commands.group(invoke_without_command=True)
    async def crypto(self, ctx, currency: toSymbol):
        print(currency)
        await ctx.send(f'{type(currency)}: ```{currency}```')

        data = await get_intraday_data(symbol=currency, market='USD')

        await ctx.send(f'```{data}```')

    @crypto.command()
    async def daily(self, ctx, currency: toSymbol):
        data = await get_daily_data(symbol=currency, market='USD')
        await ctx.send(f'```{data}```')

    @crypto.error
    async def crypto_error(self, ctx, error):
        if isinstance(error, CurrencyNotFound):
            await ctx.reply('Sorry, I could not find the currency searched for')
        else:
            raise error


def setup(bot):
    bot.add_cog(Crypto(bot))
