import sys
sys.path.append("../src/")

import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Cog

from lib.config import *


class HelpCog(Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot


    @app_commands.command(
        name="help",
        description="Botのヘルプ情報を返します"
    )
    async def help(self, ctx: discord.Interaction):
        await ctx.response.defer()

        view = discord.ui.View()
        style = discord.ButtonStyle.link
        Server = discord.ui.Button(style=style, label="Support server", url="https://discord.gg/zwbvUPTZHc")
        Twitter = discord.ui.Button(style=style, label="Twitter", url="https://twitter.com/syukur1ch")
        GitHub = discord.ui.Button(style=style, label="GitHub", url="https://github.com/syu-kuri/Spla3bot")
        view.add_item(item=Server)
        view.add_item(item=Twitter)
        view.add_item(item=GitHub)

        embed = discord.Embed(title="HELP", description="", color=discord.Colour.blue())
        embed.add_field(name="/stage [ルール] Option[時間帯]", value="```選択したルールとオプションで選択した時間帯のステージ情報を表示します```", inline=False)
        embed.add_field(name="/weapon", value="```ランダムで武器を1つ選択します```", inline=False)
        embed.add_field(name="/sub [サブウェポン名]", value="```選択したサブウェポンのブキを検索して表示します```", inline=False)
        embed.add_field(name="/special [スペシャル名]", value="```選択したスペシャルのブキを検索して表示します```", inline=False)
        embed.add_field(name="/info", value="```Botの情報を表示します```", inline=False)

        await ctx.followup.send(embed=embed, view=view)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(HelpCog(bot))