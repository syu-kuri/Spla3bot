import discord
from discord.ext import commands

from lib.functions import *
from lib.config import *


class RegularCog(commands.Cog, name="サーモンラン"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.hybrid_command(name="現在のサーモンラン", description="現在のサーモンランのステージ情報を表示します。", with_app_command=True)
    async def now_regular(self, ctx: discord.Interaction):
        """現在のサーモンランのステージ情報を表示します。"""
        data = coop_molding(get_schedule("coop-grouping-regular", "now"))

        weapons = f"{data[3][0]} \n {data[3][1]}\n {data[3][2]}\n {data[3][3]}"

        embed = discord.Embed(title="開催時間", description=f"{data[0]} - {data[1]} (開催中)", color=0x7eff00)
        embed.add_field(name="`ステージ`", value=data[2], inline=False)
        embed.add_field(name="`ブキ`", value=weapons, inline=False)
        embed.set_thumbnail(url=f"{get_rule_image(data[2])}")
        embed.set_author(name=data[2], icon_url=f"{get_rule_image('サーモンラン')}")

        await ctx.reply(embed=embed)

    @commands.hybrid_command(name="次のサーモンラン", description="次のサーモンランのステージ情報を表示します。", with_app_command=True)
    async def next_regular(self, ctx: discord.Interaction):
        """次のサーモンランのステージ情報を表示します。"""
        data = coop_molding(get_schedule("coop-grouping-regular", "next"))

        weapons = f"{data[3][0]} \n {data[3][1]}\n {data[3][2]}\n {data[3][3]}"

        embed = discord.Embed(title="開催時間", description=f"{data[0]} - {data[1]}", color=0x7eff00)
        embed.add_field(name="`ステージ`", value=data[2], inline=False)
        embed.add_field(name="`ブキ`", value=weapons, inline=False)
        embed.set_thumbnail(url=f"{get_rule_image(data[2])}")
        embed.set_author(name=data[2], icon_url=f"{get_rule_image('サーモンラン')}")

        await ctx.reply(embed=embed)

    @commands.hybrid_command(name="すべてのサーモンラン", description="現在から24時間先までのサーモンランのステージ情報を表示します。", with_app_command=True)
    async def all_regular(self, ctx: discord.Interaction):
        """現在から24時間先までのサーモンランのステージ情報を表示します。"""
        data = schedule_molding("coop-grouping-regular")

        embed = discord.Embed(title="現在から24時間先までのスケジュール", description="", color=0x7eff00)
        for i in range(len(data)):
            new_data = data[i]

            stage = "ステージ：" + new_data[3][0]
            weapons = "ブキ：" + data[i][2][0] + "\n" + data[i][2][1] + "\n" + data[i][2][2] + "\n" + data[i][2][3]
            value = stage + "\n" + weapons

            embed.add_field(name=new_data[0] + "-" + new_data[1], value=value, inline=False)
        embed.set_thumbnail(url=f"{get_rule_image(data[0][2])}")
        embed.set_author(name=data[0][2], icon_url=f"{get_rule_image('サーモンラン')}")

        await ctx.reply(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(RegularCog(bot))