import discord
from discord.ext import commands

from lib.functions import *
from lib.config import *


class OpenCog(commands.Cog, name="バンカラ(オープン)"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot


    @commands.hybrid_group()
    async def open(self, ctx):
        if ctx.invoked_subcommand is None:
            emb = discord.Embed("エラーが発生しました", description="このコマンドは引数が必要です。", color=discord.Colour.red())
            await ctx.reply(embed=emb)

    @open.command(description="現在のバンカラマッチ(オープン)情報を表示します。")
    async def now(self, ctx: discord.Interaction):
        data = molding(get_schedule("bankara-open", "now"))

        embed = discord.Embed(title="開催時間", description=f"{data[0]} - {data[1]} (開催中)", color=0xff7213)
        embed.add_field(name="`ステージ`", value=data[3][0] + "\n" + data[3][1], inline=False)
        embed.set_thumbnail(url=f"{get_rule_image(data[2])}")
        embed.set_author(name=data[2], icon_url=f"{get_rule_image(data[2])}")
        embed.set_footer(text="Creator： しゅーくり#9118(Discord)/syu-kuri(GitHub)")

        await ctx.reply(embed=embed)

    @open.command(description="次のバンカラマッチ(オープン)情報を表示します。")
    async def next(self, ctx: discord.Interaction):
        data = molding(get_schedule("bankara-open", "next"))

        embed = discord.Embed(title="開催時間", description=f"{data[0]} - {data[1]}", color=0xff7213)
        embed.add_field(name="`ステージ`", value=data[3][0] + "\n" + data[3][1], inline=False)
        embed.set_thumbnail(url=f"{get_rule_image(data[2])}")
        embed.set_author(name=data[2], icon_url=f"{get_rule_image(data[2])}")
        embed.set_footer(text="Creator： しゅーくり#9118(Discord)/syu-kuri(GitHub)")

        await ctx.reply(embed=embed)

    @open.command(description="現在から最大12個のバンカラマッチ(オープン)情報を表示します。")
    async def all(self, ctx: discord.Interaction):
        data = schedule_molding("bankara-open")

        embed = discord.Embed(title=f"現在から{len(data)}個先までのスケジュール", description="", color=0xff7213)
        for i in range(len(data)):
            new_data = data[i]
            rule = "ルール：" + data[i][2]
            stages = "マップ：" + new_data[3][0] + "、" + new_data[3][1]
            value = rule + "\n" + stages
            embed.add_field(name=new_data[0] + "-" + new_data[1], value=value, inline=False)
        embed.set_thumbnail(url=f"{get_rule_image('バンカラマッチ')}")
        embed.set_author(name="バンカラマッチ(オープン))", icon_url=f"{get_rule_image('バンカラマッチ')}")
        embed.set_footer(text="Creator： しゅーくり#9118(Discord)/syu-kuri(GitHub)")

        await ctx.reply(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(OpenCog(bot))