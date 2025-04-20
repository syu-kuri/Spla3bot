import discord
import discord.app_commands
from discord.ext import commands

from lib.config import *
from lib.discord import *


class Spla3Bot(commands.Bot):
    def __init__(self, **kwargs):
        self.database = kwargs.pop('database')
        intents=discord.Intents.default()
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
