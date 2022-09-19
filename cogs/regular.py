import discord
from discord.ext import commands

from lib.functions import *
from lib.config import *


class RegularCog(commands.Cog, name="ナワバリ"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot


    @commands.hybrid_group()
    async def regular(self, ctx):
        if ctx.invoked_subcommand is None:
            emb = discord.Embed("エラーが発生しました", description="このコマンドは引数が必要です。", color=discord.Colour.red())
            await ctx.reply(embed=emb)

    @regular.command(description="現在のナワバリ情報を表示します。")
    async def now(self, ctx: discord.Interaction):
        data = molding(get_schedule("regular", "now"))

        embed = discord.Embed(title="開催時間", description=f"{data[0]} - {data[1]} (開催中)", color=0x7eff00)
        embed.add_field(name="`ステージ`", value=data[3][0] + "\n" + data[3][1], inline=False)
        embed.set_thumbnail(url=f"{get_rule_image(data[2])}")
        embed.set_author(name=data[2], icon_url=f"{get_rule_image(data[2])}")
        embed.set_footer(text="Creator： しゅーくり#9118(Discord)/syu-kuri(GitHub)")

        await ctx.reply(embed=embed)

    @regular.command(description="次のナワバリ情報を表示します。")
    async def next(self, ctx: discord.Interaction):
        data = molding(get_schedule("regular", "next"))

        embed = discord.Embed(title="開催時間", description=f"{data[0]} - {data[1]}", color=0x7eff00)
        embed.add_field(name="`ステージ`", value=data[3][0] + "\n" + data[3][1], inline=False)
        embed.set_thumbnail(url=f"{get_rule_image(data[2])}")
        embed.set_author(name=data[2], icon_url=f"{get_rule_image(data[2])}")
        embed.set_footer(text="Creator： しゅーくり#9118(Discord)/syu-kuri(GitHub)")

        await ctx.reply(embed=embed)

    @regular.command(description="現在から最大12個のナワバリ情報を表示します。")
    async def all(self, ctx: discord.Interaction):
        """現在から24時間先までのナワバリのステージ情報を表示します。"""
        data = schedule_molding("regular")

        embed = discord.Embed(title="現在から24時間先までのスケジュール", description="", color=0x7eff00)
        for i in range(len(data)):
            new_data = data[i]
            embed.add_field(name=new_data[0] + "-" + new_data[1], value=new_data[3][0] + "、" + new_data[3][1], inline=False)
        embed.set_thumbnail(url=f"{get_rule_image(data[0][2])}")
        embed.set_author(name=data[0][2], icon_url=f"{get_rule_image(data[0][2])}")
        embed.set_footer(text="Creator： しゅーくり#9118(Discord)/syu-kuri(GitHub)")

        await ctx.reply(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(RegularCog(bot))