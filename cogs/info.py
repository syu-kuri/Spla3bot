import sys
sys.path.append("../src/")
from platform import python_version

import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Cog

from lib.config import *


class InfoCog(Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(
        name="info",
        description="Botの情報を返します"
    )
    async def information(self, ctx: discord.Interaction):
        await ctx.response.defer()

        guilds = len(self.bot.guilds)
        users = len(self.bot.users)
        version = discord.__version__
        py_version = python_version()

        raw_ping = self.bot.latency
        ping = round(raw_ping * 1000)

        embed = discord.Embed(title="Bot情報", description="", color=discord.Colour.blue())
        embed.add_field(name="開発環境", value=f"Python: {py_version}\nDiscord.py: {version}", inline=False)
        embed.add_field(name="応答速度(Ping)", value=f"{ping}ms", inline=False)
        embed.add_field(name="サーバー", value=f"{guilds}guilds", inline=True)
        embed.add_field(name="ユーザー", value=f"{users}users", inline=True)
        embed.add_field(name="クリエイター", value=f"しゅーくり#9118", inline=False)

        await ctx.followup.send(embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(InfoCog(bot))