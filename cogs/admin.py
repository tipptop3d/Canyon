import discord
from discord.ext import commands
import requests
import traceback

import datetime

from .utils import database, config
from .utils.embeds import MyEmbeds as embeds

class Pastebin():

    def __init__(self, url):
        self.api_key = config.PASTEBIN_KEY
        self.url = url

pastebin = Pastebin("https://pastebin.com/api/api_post.php")


class Admin(commands.Cog):

    """Debugging and Admin-Only Commands"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["eval"])
    @commands.is_owner()
    async def evaluate(self, ctx, *, code : str):
        """Evaluates a python expression"""

        try:
            result = f'Result: {eval(code.strip("`").replace("py", ""))}'
        except Exception as e:
            result = f"Error: {e}"
        try:

            embed = discord.Embed(
                title="Evaluated Python Expression",
                color= 0x34709f,
            ).set_footer(
                text=f"Requested by {ctx.author.name}",
                icon_url="https://cdn4.iconfinder.com/data/icons/logos-and-brands/512/267_Python_logo-512.png"
            )
            
            await ctx.send(f"```{result}```", embed=embed)
        
        except discord.HTTPException as e:
            print(result)
            payload = {
                "api_dev_key": pastebin.api_key,
                "api_option": "paste",
                "api_paste_name": f"Evaluated Python Expression by {ctx.author.name}",
                "api_paste_code": str(result),
                "api_paste_private": 1,
                "api_paste_expire_date": "1H",
                "api_paste_format": "json",
            }

            r = requests.post(pastebin.url, data=payload)

            content = r.content.decode('utf-8')

            if "Bad API request" in content:
                embed = discord.Embed(
                    title = "Result is over 2000 characters long",
                    description = f"Error while uploading to pastebin: {content.split(',')[2].strip(' ')}",
                    color = 0xff0000
                )

            else:
                embed = discord.Embed(
                    title="Evaluated Python Expression",
                    url=content,
                    color= 0x34709f,
                    timestamp=datetime.datetime.utcnow() + datetime.timedelta(hours=1)
                ).set_footer(
                    text=f"Requested by {ctx.author.name} ― Expires ",
                    icon_url="https://cdn4.iconfinder.com/data/icons/logos-and-brands/512/267_Python_logo-512.png"
                )

            await ctx.send(embed=embed)

    @commands.command(aliases=["exec", "code"])
    @commands.is_owner()
    async def execute(self, ctx, *, code : str):
        """Executes a code snippet"""

        try:
            exec(code.strip("`").replace("py", ""))
        except SyntaxError as e:
            await ctx.send(embed=embeds.create_error("Syntax Error in your Expression", e))
        except Exception as e:
            await ctx.send(embed=embeds.create_error(None, e))
        else:
            await ctx.send(embed=discord.Embed(
                title="Executed the Python Code",
                color= 0x34709f,
            ).set_footer(
                text=f"Requested by {ctx.author.name}",
                icon_url="https://cdn4.iconfinder.com/data/icons/logos-and-brands/512/267_Python_logo-512.png"
            ))


    @commands.command()
    @commands.is_owner()
    async def load(self, ctx, *, module : str):
        """Loads a module"""

        try:
            self.bot.load_extension(module)
        except Exception as e:
            await ctx.send(embed=embeds.create_error("Failed loading Extension", e))
        else:
            await ctx.send(embed=embeds.create_success("Success", "Successfully loaded extension"))


    @commands.command()
    @commands.is_owner()
    async def unload(self, ctx, *, module : str):
        """Unloads a module"""

        try:
            self.bot.unload_extension(module)
        except Exception as e:
            await ctx.send(embed=embeds.create_error("Failed unloading Extension", e))
        else:
            await ctx.send(embed=embeds.create_success("Success", "Successfully unloaded extension"))


    @commands.command(name='reload')
    @commands.is_owner()
    async def _reload(self, ctx, *, module : str):
        """Reloads a module"""

        try:
            self.bot.reload_extension(module)
        except Exception as e:
            await ctx.send(embed=embeds.create_error("Failed reload Extension", e))
        else:    
            await ctx.send(embed=embeds.create_success("Success", "Successfully reloaded extension"))



def setup(bot):
    bot.add_cog(Admin(bot))
    