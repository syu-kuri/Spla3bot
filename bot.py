import asyncio

import discord
import discord.app_commands
from discord.ext import commands

from lib.config import *
from lib.discord import *

extensions = [
    'cogs.admin',
    'cogs.error',
    'cogs.spla3',
]

class Spla3Bot(commands.Bot):
    def __init__(self):
        intents=discord.Intents.all()
        super(Spla3Bot, self).__init__(
            command_prefix=commands.when_mentioned_or(prefix),
            intents=intents,
            help_command=JapaneseHelpCommand()
        )

    async def on_ready(self):
        presence = discord.Game(f"{prefix}help")
        await self.change_presence(activity=presence)
        print("ログインしました")
        print('----------------')

    async def setup_hook(self):
        await self.tree.sync()


async def main():
    bot = Spla3Bot()
    for extension in extensions:
        await bot.load_extension(extension)

    await bot.start(token)


if __name__ == '__main__':
    asyncio.run(main())