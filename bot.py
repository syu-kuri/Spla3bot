import asyncio

import discord
import discord.app_commands
from discord.ext import commands

from lib.config import *
from lib.discord import *


class Spla3Bot(commands.Bot):
    def __init__(self):
        intents=discord.Intents.all()
        super(Spla3Bot, self).__init__(
            command_prefix=commands.when_mentioned_or(prefix),
            intents=intents,
            help_command=None
        )

    async def on_ready(self):
        count_guilds = len(self.guilds)
        count_users = len(self.users)
        presence = discord.Game(f"/help | {str(count_guilds)}guilds | {str(count_users)}users")
        await self.change_presence(activity=presence)
        print("ログインしました")
        print('----------------')

    async def setup_hook(self):
        await self.tree.sync()

async def main():
    bot = Spla3Bot()
    for file in os.listdir(f"./cogs"):
        if file.endswith(".py"):
            extension = file[:-3]
            try:
                await bot.load_extension(f"cogs.{extension}")
                print(f"Loaded extension '{extension}'")
            except Exception as e:
                exception = f"{type(e).__name__}: {e}"
                print(f"Failed to load extension {extension}\n{exception}")

    await bot.start(token)


if __name__ == '__main__':
    asyncio.run(main())