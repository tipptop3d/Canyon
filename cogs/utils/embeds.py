import discord

class MyEmbeds():
    
    @classmethod
    def create_error(cls, title, description, exception : Exception = None):
        return discord.Embed(
            title = title or "Error",
            description = description or f"{type(exception).__name__}: {exception}",
            color = 0xff0000
        )

    @classmethod
    def create_success(cls, title, description):
        return discord.Embed(
            title = title or "Error",
            description=description,
            color = 0x00ff00
        )
    

