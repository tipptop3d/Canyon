import discord


class MyEmbeds():

    @staticmethod
    def create_error(title, description, exception: Exception = None):
        return discord.Embed(
            title=title or 'Error',
            description=description or f'{type(exception).__name__}: {exception}',
            color=0xff0000
        )

    @staticmethod
    def create_success(title, description):
        return discord.Embed(
            title=title or 'Success',
            description=description,
            color=0x00ff00
        )
