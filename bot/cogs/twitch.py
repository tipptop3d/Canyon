import discord
from discord.ext import commands as discord_commands
from twitchio.ext import commands as twitch_commands

from .utils import config

class Twitch(discord_commands.Cog):

    """Twitch Bot"""

    def __init__(self, bot):
        self.discord_bot = bot
        self.emoji = '🎥'

        self.twitch_bot = twitch_commands.Bot(
            # set up the bot
            irc_token=config.TWITCH_BOT_IRC,
            client_id=config.TWITCH_CLIENT_ID,
            nick=config.TWITCH_BOT_USERNAME,
            prefix='!',
            initial_channels=[config.TWITCH_CHANNEL_NAME]
        )
        self.discord_bot.loop.create_task(self.twitch_bot.start())
        self.twitch_bot.listen('event_message')(self.event_message)
        self.twitch_bot.command(name='test')(self.my_command)

    # TwitchIO event
    async def event_message(self, message):
        print(message.content)
        await self.twitch_bot.handle_commands(message)

    # Discord command
    @discord_commands.command()
    async def test(self, ctx):
        await ctx.send('Hai there!')

    # TwitchIO command
    # @twitch_commands.command(name='test')
    async def my_command(self, ctx):
        await ctx.send('Hai there!')



def setup(bot):
    bot.add_cog(Twitch(bot))
    