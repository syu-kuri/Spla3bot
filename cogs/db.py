import sys
import asyncio
from asyncpg import PostgresError, UniqueViolationError
sys.path.append("../src/")

import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Cog

from lib.config import *
from lib.text import *


class DBCog(Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.db = bot.database

    @app_commands.command(
        name="register",
        description="フレンドコードの登録を行います"
    )
    @app_commands.describe(fc="フレンドコードを入力してください")
    @app_commands.rename(fc="フレンドコード")
    async def register(self, ctx: discord.Interaction, fc: str):
        await ctx.response.defer(ephemeral=True)

        user_id = ctx.user.id
        try:
            async with self.db.acquire() as connection:
                await connection.execute('''
                    INSERT INTO users(
                        user_id,
                        friend_code
                    )
                    VALUES(
                        $1,
                        $2
                    )
                ''',
                    str(user_id),
                    fc
                )
            await asyncio.sleep(1)
            async with self.db.acquire() as connection:
                row = await connection.fetchrow('''
                    SELECT * FROM users
                    WHERE user_id = $1
                ''',
                    str(user_id)
                )
            await asyncio.sleep(1)
            _user = await self.bot.fetch_user(row['user_id'])
            embed = discord.Embed(title="登録完了", description="", color=discord.Colour.blue())
            embed.add_field(name="登録ユーザー", value=f"```{_user}```")
            embed.add_field(name="フレンドコード", value=f"```{row['friend_code']}```")
            await ctx.followup.send(embed=embed, ephemeral=True)
        except UniqueViolationError as u_e:
            embed = discord.Embed(title="登録済み", description="あなたのフレンドコードは登録済みです。", color=discord.Colour.red())
            await ctx.followup.send(embed=embed, ephemeral=True)
        except PostgresError as p_e:
            embed = discord.Embed(title="接続エラー", description=f"接続に失敗しました\n{p_e}", color=discord.Colour.red())
            await ctx.followup.send(embed=embed, ephemeral=True)
        except:
            embed = discord.Embed(title="登録済み", description="あなたのフレンドコードは登録済みです。", color=discord.Colour.red())
            await ctx.followup.send(embed=embed, ephemeral=True)

    @app_commands.command(
        name="search",
        description="ユーザーのフレンドコードを検索します"
    )
    @app_commands.describe(user="ユーザーを選択してください")
    @app_commands.rename(user="ユーザー")
    async def search(self, ctx: discord.Interaction, user: discord.User):
        await ctx.response.defer()

        try:
            row = await self.db.fetchrow('''
                SELECT * FROM users
                WHERE user_id = $1
            ''',
                str(user.id)
            )
            _user = await self.bot.fetch_user(row['user_id'])
            embed = discord.Embed(title=f"{user}のフレンドコード", description="", color=discord.Colour.blue())
            embed.add_field(name="ユーザー", value=f"```{_user}```")
            embed.add_field(name="フレンドコード", value=f"```{row['friend_code']}```")
            await ctx.followup.send(embed=embed)
        except PostgresError as p_e:
            embed = discord.Embed(title="エラー", description=f"接続に失敗しました\n{p_e}", color=discord.Colour.red())
            await ctx.followup.send(embed=embed)
        except:
            embed = discord.Embed(title="未登録", description=f"<@{user.id}>のフレンドコードは登録されていません。", color=discord.Colour.red())
            await ctx.followup.send(embed=embed)

    @app_commands.command(
        name="update",
        description="ユーザーのフレンドコードを更新します"
    )
    @app_commands.describe(fc="フレンドコードを入力してください")
    @app_commands.rename(fc="フレンドコード")
    async def update(self, ctx: discord.Interaction, fc: str):
        await ctx.response.defer(ephemeral=True)

        try:
            await self.db.execute('''
                UPDATE users
                SET friend_code = $1
                WHERE user_id = $2
            ''',
                fc,
                str(ctx.user.id)
            )
            await asyncio.sleep(1)
            row = await self.db.fetchrow('''
                SELECT * FROM users
                WHERE user_id = $1
            ''',
                str(ctx.user.id)
            )
            _user = await self.bot.fetch_user(row['user_id'])
            embed = discord.Embed(title="更新完了", description="", color=discord.Colour.blue())
            embed.add_field(name="登録ユーザー", value=f"```{_user}```")
            embed.add_field(name="フレンドコード", value=f"```{row['friend_code']}```")
            await ctx.followup.send(embed=embed, ephemeral=False)
        except PostgresError as p_e:
            embed = discord.Embed(title="エラー", description=f"接続に失敗しました\n{p_e}", color=discord.Colour.red())
            await ctx.followup.send(embed=embed, ephemeral=True)
        except:
            embed = discord.Embed(title="未登録", description=f"<@{ctx.user.id}>のフレンドコードは登録されていません。", color=discord.Colour.red())
            await ctx.followup.send(embed=embed, ephemeral=False)

    @app_commands.command(
        name="delete",
        description="ユーザーのフレンドコードを削除します"
    )
    async def delete(self, ctx: discord.Interaction):
        await ctx.response.defer(ephemeral=True)

        try:
            await self.db.execute('''
                DELETE FROM users
                WHERE user_id = $1
            ''',
                str(ctx.user.id)
            )
            embed = discord.Embed(title="削除完了", description=f"<@{ctx.user.id}>のフレンドコードは削除されました。", color=discord.Colour.blue())
            await ctx.followup.send(embed=embed, ephemeral=False)
        except PostgresError as p_e:
            embed = discord.Embed(title="エラー", description=f"接続に失敗しました\n{p_e}", color=discord.Colour.red())
            await ctx.followup.send(embed=embed, ephemeral=True)
        except:
            embed = discord.Embed(title="未登録", description=f"<@{ctx.user.id}>のフレンドコードは登録されていません。", color=discord.Colour.red())
            await ctx.followup.send(embed=embed, ephemeral=False)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(DBCog(bot))