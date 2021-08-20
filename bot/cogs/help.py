import discord
from discord.ext import commands

class MyHelpCommand(commands.HelpCommand):
   # !help
    async def send_bot_help(self, mapping):
        await self.context.send('no help')
       
   # !help <command>
    async def send_command_help(self, command):
        await self.context.send('This is help command')
      
   # !help <group>
    async def send_group_help(self, group):
        await self.context.send('This is help group')
    
   # !help <cog>
    async def send_cog_help(self, cog):
        await self.context.send('This is help cog')

class Help(commands.Cog):
    """Help Commands"""

    def __init__(self, bot):
        self.bot = bot
        self.emoji = ''
        self.hidden = True
        self._original_help_command = bot.help_command
        self.bot.help_command = MyHelpCommand()
        self.bot.help_command.cog = self

    def cog_unload(self):
        self.bot.help_command = self._original_help_command


def setup(bot):
    bot.add_cog(Help(bot))