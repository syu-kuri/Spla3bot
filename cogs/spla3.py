import io
import json
import random
from pathlib import Path
from typing import Optional

import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Cog

from lib.color import get_rule_color
from lib.api import Spla3APIError
from lib.img import ImageFetchError, get_concat_h_cut, get_rule_image
from lib.models import BattleStage, CoopStage, FestStage, TricolorStage
from lib.spla_func import spla3
from lib.text import hiraToKata

WEAPONS_FILE = Path("src/weapons3.json")


class Spla3Cog(Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.weapons = self._load_weapons()
        self.sub_list = self._unique_weapon_values("sub")
        self.special_list = self._unique_weapon_values("special")

    def _load_weapons(self) -> list[dict]:
        with WEAPONS_FILE.open("r", encoding="utf-8") as f:
            return json.load(f)

    def _unique_weapon_values(self, field: str) -> list[str]:
        return sorted({weapon[field] for weapon in self.weapons if weapon.get(field)})

    # ── オートコンプリート ─────────────────────────────

    async def sp_autocomplete(self, interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
        target = hiraToKata(current)
        return [app_commands.Choice(name=name, value=name) for name in self.special_list if target in name][:25]

    async def sub_autocomplete(self, interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
        target = hiraToKata(current)
        return [app_commands.Choice(name=name, value=name) for name in self.sub_list if target in name][:25]

    # ── 共通ヘルパー ──────────────────────────────────

    async def _send_stage_embed(self, ctx: discord.Interaction, embed: discord.Embed, image_urls: list[str]) -> None:
        """ステージ画像2枚を横並びにしてembedを送信する"""
        img = await get_concat_h_cut(image_urls[0], image_urls[1])
        img_binary = io.BytesIO()
        img.save(img_binary, format='PNG')
        img_binary.seek(0)
        file = discord.File(img_binary, filename='image.png')
        embed.set_image(url="attachment://image.png")
        await ctx.followup.send(embed=embed, file=file)

    async def _search_weapon(self, ctx: discord.Interaction, field: str, value: str) -> None:
        """サブ/スペシャルでブキを検索してembedを送信する"""
        await ctx.response.defer()

        items = [w for w in self.weapons if w[field] == value]
        if items:
            weapons = "\n".join(w["name"] for w in items)
            embed = discord.Embed(
                title=f"{len(items)}件のブキが見つかりました",
                description=f"```{weapons}```",
                color=discord.Colour.blue()
            )
        else:
            embed = discord.Embed(
                title="ブキが見つかりませんでした",
                description=f"{value}で検索した結果、このブキは見つかりませんでした",
                color=discord.Colour.red()
            )
        await ctx.followup.send(embed=embed)

    # ── /stage ────────────────────────────────────────

    @app_commands.command(name="stage", description="スプラトゥーン3のステージ情報を表示します")
    @app_commands.describe(rules="ルールを選択してください", tz="時間帯を選択してください")
    @app_commands.rename(rules="ルール", tz="時間帯")
    @app_commands.choices(
        rules=[
            app_commands.Choice(name='ナワバリ', value="regular"),
            app_commands.Choice(name='バンカラ(チャレンジ)', value="bankara-challenge"),
            app_commands.Choice(name='バンカラ(オープン)', value="bankara-open"),
            app_commands.Choice(name='Xマッチ', value="x"),
            app_commands.Choice(name='サーモンラン', value="coop-grouping"),
        ],
        tz=[
            app_commands.Choice(name='現在', value="now"),
            app_commands.Choice(name='次', value="next"),
        ]
    )
    async def stage3(self, ctx: discord.Interaction, rules: app_commands.Choice[str], tz: Optional[app_commands.Choice[str]]):
        await ctx.response.defer()
        time_slot = tz.value if tz is not None else "now"
        try:
            data = await spla3(rules.value, time_slot)

            not_coop = ["ナワバリ", "バンカラ(チャレンジ)", "バンカラ(オープン)", "Xマッチ"]

            if rules.name in not_coop:
                await self._send_battle_stage(ctx, rules.name, data)
            else:
                await self._send_coop_stage(ctx, data)
        except (Spla3APIError, ImageFetchError):
            embed = discord.Embed(
                title="ステージ情報を取得できませんでした",
                description="しばらく時間をおいてから再度お試しください。",
                color=discord.Colour.red()
            )
            await ctx.followup.send(embed=embed)

    async def _send_battle_stage(self, ctx: discord.Interaction, rule_display_name: str, data: BattleStage | FestStage | TricolorStage) -> None:
        if data.is_fest:
            if isinstance(data, TricolorStage):
                # トリカラあり
                embed = discord.Embed(title="splatoon3 ステージ情報 | フェス開催中", color=get_rule_color(data.rule_name))
                embed.add_field(name="開催時間", value=f"```{data.start_time} ～ {data.end_time}```", inline=False)
                embed.add_field(name="フェスステージ", value=f"```{data.stages[0]}\n{data.stages[1]}```", inline=False)
                embed.add_field(name="トリカラステージ", value=f"```{data.tricolor_stage}```", inline=False)
                embed.set_thumbnail(url=get_rule_image(data.rule_name))
                embed.set_image(url=data.tricolor_image_url)
                await ctx.followup.send(embed=embed)
            else:
                # トリカラなし
                embed = discord.Embed(title="splatoon3 ステージ情報 | フェス開催中", color=get_rule_color(data.rule_name))
                embed.add_field(name="開催時間", value=f"```{data.start_time} ～ {data.end_time}```", inline=False)
                embed.add_field(name="フェスステージ", value=f"```{data.stages[0]}\n{data.stages[1]}```", inline=False)
                embed.add_field(name="トリカラステージ", value="```現在トリカラは開催されていません```", inline=False)
                embed.set_thumbnail(url=get_rule_image(data.rule_name))
                await self._send_stage_embed(ctx, embed, data.image_urls)
        else:
            # 通常マッチ
            embed = discord.Embed(title=f"splatoon3 ステージ情報 | {rule_display_name}", color=get_rule_color(data.rule_name))
            embed.add_field(name="開催時間", value=f"```{data.start_time} ～ {data.end_time}```", inline=False)
            embed.add_field(name="ルール", value=f"```{data.rule_name}```", inline=False)
            embed.add_field(name="ステージ", value=f"```{data.stages[0]}\n{data.stages[1]}```", inline=False)
            embed.set_thumbnail(url=get_rule_image(data.rule_name))
            await self._send_stage_embed(ctx, embed, data.image_urls)

    async def _send_coop_stage(self, ctx: discord.Interaction, data: CoopStage) -> None:
        title = "splatoon3 ステージ情報 | サーモンラン ビッグラン中" if data.is_big_run else "splatoon3 ステージ情報 | サーモンラン"
        weapons = "\n".join(data.weapons)
        embed = discord.Embed(title=title, color=get_rule_color("サーモンラン"))
        embed.add_field(name="開催時間", value=f"```{data.start_time} ～ {data.end_time}```", inline=False)
        embed.add_field(name="ステージ", value=f"```{data.stage}```", inline=False)
        embed.add_field(name="支給ブキ", value=f"```{weapons}```", inline=False)
        embed.set_thumbnail(url=get_rule_image("サーモンラン"))
        embed.set_image(url=data.image_url)
        await ctx.followup.send(embed=embed)

    # ── /weapon ───────────────────────────────────────

    @app_commands.command(name="weapon", description="ブキガチャを行います")
    async def random_weapon(self, ctx: discord.Interaction):
        await ctx.response.defer(ephemeral=True)

        weapon_data = random.choice(self.weapons)
        embed = discord.Embed(title=f"{ctx.user.name}のブキはこれだ！", color=discord.Colour.yellow())
        embed.add_field(name="ブキ名", value=f'```{weapon_data["name"]}```', inline=False)
        embed.add_field(name="サブ", value=f'```{weapon_data["sub"]}```', inline=True)
        embed.add_field(name="スペシャル", value=f'```{weapon_data["special"]}```', inline=True)
        await ctx.followup.send(embed=embed, ephemeral=True)

    # ── /sub ──────────────────────────────────────────

    @app_commands.command(name="sub", description="サブウェポンからブキを検索します")
    @app_commands.describe(subs="検索するサブウェポンを選択してください")
    @app_commands.rename(subs="サブウェポン")
    @app_commands.autocomplete(subs=sub_autocomplete)
    async def sub_weapon(self, ctx: discord.Interaction, subs: str):
        await self._search_weapon(ctx, "sub", subs)

    # ── /special ──────────────────────────────────────

    @app_commands.command(name="special", description="スペシャルからブキを検索します")
    @app_commands.describe(specials="検索するスペシャルを選択してください")
    @app_commands.rename(specials="スペシャル")
    @app_commands.autocomplete(specials=sp_autocomplete)
    async def special_weapon(self, ctx: discord.Interaction, specials: str):
        await self._search_weapon(ctx, "special", specials)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Spla3Cog(bot))
