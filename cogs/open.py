import discord
from discord.ext import commands

from lib.functions import *
from lib.config import *


class OpenCog(commands.Cog, name="バンカラ(オープン)"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.hybrid_command(name="現在のバンカラオープン", description="現在のバンカラマッチ(オープン)のステージ情報を表示します。", with_app_command=True)
    async def now_bankara_open(self, ctx: discord.Interaction):
        """現在のバンカラマッチ(オープン)のステージ情報を表示します。"""
        data = molding(get_schedule("bankara-open", "now"))

        embed = discord.Embed(title="開催時間", description=f"{data[0]} - {data[1]} (開催中)", color=0xf02c7d)
        embed.add_field(name="`ステージ`", value=data[3][0] + "\n" + data[3][1], inline=False)
        embed.set_thumbnail(url=f"{get_rule_image(data[2])}")
        embed.set_author(name=data[2], icon_url=f"{get_rule_image(data[2])}")

        await ctx.reply(embed=embed)

    @commands.hybrid_command(name="次のバンカラオープン", description="次のバンカラマッチ(オープン)のステージ情報を表示します。", with_app_command=True)
    async def next_bankara_open(self, ctx: discord.Interaction):
        """次のバンカラマッチ(オープン)のステージ情報を表示します。"""
        data = molding(get_schedule("bankara-open", "next"))

        embed = discord.Embed(title="開催時間", description=f"{data[0]} - {data[1]}", color=0xf02c7d)
        embed.add_field(name="`ステージ`", value=data[3][0] + "\n" + data[3][1], inline=False)
        embed.set_thumbnail(url=f"{get_rule_image(data[2])}")
        embed.set_author(name=data[2], icon_url=f"{get_rule_image(data[2])}")

        await ctx.reply(embed=embed)

    @commands.hybrid_command(name="すべてのバンカラオープン", description="現在から24時間先までのバンカラマッチ(オープン)のステージ情報を表示します。", with_app_command=True)
    async def all_bankara_open(self, ctx: discord.Interaction):
        """現在から24時間先までのバンカラマッチ(オープン)のステージ情報を表示します。"""
        data = schedule_molding("bankara-open")

        embed = discord.Embed(title="現在から24時間先までのスケジュール", description="", color=0xf02c7d)
        for i in range(len(data)):
            new_data = data[i]
            rule = "ルール：" + data[i][2]
            stages = "マップ：" + new_data[3][0] + "、" + new_data[3][1]
            value = rule + "\n" + stages
            embed.add_field(name=new_data[0] + "-" + new_data[1], value=value, inline=False)
        embed.set_thumbnail(url=f"{get_rule_image('バンカラマッチ')}")
        embed.set_author(name="バンカラマッチ(オープン)", icon_url=f"{get_rule_image('バンカラマッチ')}")

        await ctx.reply(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(OpenCog(bot))