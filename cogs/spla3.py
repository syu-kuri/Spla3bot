from typing import Optional
import json
import random

import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Cog

from lib.config import *
from lib.spla_func import *
from lib.img import *
from lib.color import *


class Spla3Cog(Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot


    @app_commands.command(
        name="stage",
        description="スプラトゥーン3のステージ情報を表示します"
    )
    @app_commands.describe(rules="ルールを選択してください", tz="時間帯を選択してください")
    @app_commands.rename(rules="ルール", tz="時間帯")
    @app_commands.choices(
        rules=[
            app_commands.Choice(name='ナワバリ', value="regular"),
            app_commands.Choice(name='バンカラ(チャレンジ)', value="bankara-challenge"),
            app_commands.Choice(name='バンカラ(オープン)', value="bankara-open"),
            app_commands.Choice(name='サーモンラン', value="coop-grouping-regular"),
        ],
        tz=[
            app_commands.Choice(name='現在', value="now"),
            app_commands.Choice(name='次', value="next"),
        ]
    )
    async def stage3(self, ctx: discord.Interaction, rules: app_commands.Choice[str], tz: Optional[app_commands.Choice[str]]):
        not_coop = ["ナワバリ", "バンカラ(チャレンジ)", "バンカラ(オープン)"]
        await ctx.response.defer()
        if tz is not None:
            data = spla3(rules.value, tz.value)
            if rules.name in not_coop:
                if data[0]:
                    if data[1]:
                        embed = discord.Embed(title="splatoon3 ステージ情報 | フェス開催中", description="", color=get_rule_color(data[4]))
                        embed.add_field(name="開催時間", value=f"```{data[2]} ～ {data[3]}```", inline=False)
                        embed.add_field(name="フェスステージ", value=f"```{data[5][0]}\n{data[5][1]}```", inline=False)
                        embed.add_field(name="トリカラステージ", value=f"```{data[6]}```", inline=False)
                        embed.set_thumbnail(url=get_rule_image(data[4]))
                        embed.set_image(url=data[7])
                    else:
                        embed = discord.Embed(title="splatoon3 ステージ情報 | フェス開催中", description="", color=get_rule_color(data[4]))
                        embed.add_field(name="開催時間", value=f"```{data[2]} ～ {data[3]}```", inline=False)
                        embed.add_field(name="フェスステージ", value=f"```{data[5][0]}\n{data[5][1]}```", inline=False)
                        embed.add_field(name="トリカラステージ", value=f"```現在トリカラは開催されていません```", inline=False)
                        embed.set_thumbnail(url=get_rule_image(data[4]))
                else:
                    embed = discord.Embed(title=f"splatoon3 ステージ情報 | {data[3]}", description="", color=get_rule_color(data[3]))
                    embed.add_field(name="開催時間", value=f"```{data[1]} ～ {data[2]}```", inline=False)
                    embed.add_field(name="ステージ", value=f"```{data[4][0]}\n{data[4][1]}```", inline=False)
                    embed.set_thumbnail(url=get_rule_image(data[3]))
            else:
                weapons = f"{data[4][0]}\n{data[4][1]}\n{data[4][2]}\n{data[4][3]}"

                embed = discord.Embed(title="splatoon3 ステージ情報 | サーモンラン", description="", color=get_rule_color("サーモンラン"))
                embed.add_field(name="開催時間", value=f"```{data[0]} ～ {data[1]}```", inline=False)
                embed.add_field(name="ステージ", value=f"```{data[2]}```", inline=False)
                embed.add_field(name="支給ブキ", value=f"```{weapons}```", inline=False)
                embed.set_thumbnail(url=f"{get_rule_image('サーモンラン')}")
                embed.set_image(url=data[3])
        else:
            data = spla3(rules.value, "now")
            if rules.name in not_coop:
                if data[0]:
                    if data[1]:
                        embed = discord.Embed(title="splatoon3 ステージ情報 | フェス開催中", description="", color=get_rule_color(data[4]))
                        embed.add_field(name="開催時間", value=f"```{data[2]} ～ {data[3]}```", inline=False)
                        embed.add_field(name="フェスステージ", value=f"```{data[5][0]}\n{data[5][1]}```", inline=False)
                        embed.add_field(name="トリカラステージ", value=f"```{data[6]}```", inline=False)
                        embed.set_thumbnail(url=get_rule_image(data[4]))
                        embed.set_image(url=data[7])
                    else:
                        embed = discord.Embed(title="splatoon3 ステージ情報 | フェス開催中", description="", color=get_rule_color(data[4]))
                        embed.add_field(name="開催時間", value=f"```{data[2]} ～ {data[3]}```", inline=False)
                        embed.add_field(name="フェスステージ", value=f"```{data[5][0]}\n{data[5][1]}```", inline=False)
                        embed.add_field(name="トリカラステージ", value=f"```現在トリカラは開催されていません```", inline=False)
                        embed.set_thumbnail(url=get_rule_image(data[4]))
                else:
                    embed = discord.Embed(title=f"splatoon3 ステージ情報 | {data[3]}", description="", color=get_rule_color(data[3]))
                    embed.add_field(name="開催時間", value=f"```{data[1]} ～ {data[2]}```", inline=False)
                    embed.add_field(name="ステージ", value=f"```{data[4][0]}\n{data[4][1]}```", inline=False)
                    embed.set_thumbnail(url=get_rule_image(data[3]))
            else:
                weapons = f"{data[4][0]}\n{data[4][1]}\n{data[4][2]}\n{data[4][3]}"

                embed = discord.Embed(title="splatoon3 ステージ情報 | サーモンラン", description="", color=get_rule_color("サーモンラン"))
                embed.add_field(name="開催時間", value=f"```{data[0]} ～ {data[1]}```", inline=False)
                embed.add_field(name="ステージ", value=f"```{data[2]}```", inline=False)
                embed.add_field(name="支給ブキ", value=f"```{weapons}```", inline=False)
                embed.set_thumbnail(url=f"{get_rule_image('サーモンラン')}")
                embed.set_image(url=data[3])
        await ctx.followup.send(embed=embed)


    @app_commands.command(
        name="weapon",
        description="ブキガチャを行います"
    )
    async def weapon(self, ctx: discord.Interaction):
        await ctx.response.defer(ephemeral=True)
        weapons3_file = "src/weapons3.json"
        with open(weapons3_file, 'r', encoding="utf-8") as f:
            json_datas = json.load(f)

        _num = len(json_datas)
        num = random.randint(0, _num - 1)
        weapon_data = json_datas[num]

        embed = discord.Embed(title=f"{ctx.user.name}のブキはこれだ！", description="", color=discord.Colour.yellow())
        embed.add_field(name="ブキ名", value=f'```{weapon_data["name"]}```', inline=False)
        embed.add_field(name="サブ", value=f'```{weapon_data["sub"]}```', inline=True)
        embed.add_field(name="スペシャル", value=f'```{weapon_data["special"]}```', inline=True)
        await ctx.followup.send(embed=embed, ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Spla3Cog(bot))