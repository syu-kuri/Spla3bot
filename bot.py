from typing import Self

import discord
import discord.app_commands
from discord.ext import commands

from config.config import PREFIX
from constants.message import Messages
from utils.log_util import LogUtil


class Spla3Bot(commands.Bot):
    def __init__(self: Self):
        intents=discord.Intents.all()
        super(Spla3Bot, self).__init__(
            command_prefix=commands.when_mentioned_or(PREFIX),
            intents=intents,
            help_command=None
        )

    async def on_ready(self: Self):
        count_guilds = len(self.guilds)
        presence = discord.Game(f"/help | {str(count_guilds)}guilds")
        await self.change_presence(activity=presence)
        LogUtil.info(Messages.BI0000000001)

    async def setup_hook(self: Self):
        await self.tree.sync()
