import datetime
import io
from typing import Self

import discord
from discord import app_commands
from discord.ext import commands

from config.config import SPLA3_BASE_URL
from constants.common import EmbedColor
from utils.spla3_utils import Spla3Util
from utils.image_util import ImageUtil
from utils.pagination_util import PaginationUtil


class Spla3Cog(commands.Cog):
    def __init__(self: Self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(
        name='stage',
        description='スプラトゥーン3のステージ情報を表示します。',
    )
    @app_commands.describe(match='ルールを選択してください', time='時間帯を選択してください')
    @app_commands.rename(match='ルール', time='時間帯')
    @app_commands.choices(
        match=[
            app_commands.Choice(name='ナワバリバトル', value='regular'),
            app_commands.Choice(name='バンカラマッチ(チャレンジ)', value='bankara-challenge'),
            app_commands.Choice(name='バンカラマッチ(オープン)', value='bankara-open'),
            app_commands.Choice(name='Xマッチ', value='x'),
        ],
        time=[
            app_commands.Choice(name='現在', value='now'),
            app_commands.Choice(name='次', value='next'),
            app_commands.Choice(name='スケジュール', value='schedule'),
        ]
    )
    async def stage3(self: Self, interaction: discord.Interaction, match: app_commands.Choice[str], time: app_commands.Choice[str]) -> None:
        await interaction.response.defer()
        request_url = SPLA3_BASE_URL + match.value + '/' + time.value

        spla3_util = Spla3Util()
        res = spla3_util.fetch_schedule(request_url)

        if len(res) == 0:
            embed = discord.Embed(title='データ取得失敗', description='データの取得に失敗しました。\n時間を空けて再度実行してください。\n改善されない場合はお問い合わせください。', colour=discord.Colour.red())
            return await interaction.followup.send(embed=embed)

        if time.value == 'now' or time.value == 'next':
            result = res[0]
            start_date = datetime.datetime.strptime(result['start_time'], '%Y-%m-%dT%H:%M:%S%z').strftime('%m/%d %H:%M')
            end_date = datetime.datetime.strptime(result['end_time'], '%Y-%m-%dT%H:%M:%S%z').strftime('%m/%d %H:%M')

            # check fest
            if result['is_fest']:
                embed = discord.Embed(title='splatoon3 ステージ情報 | フェス開催中', description='フェスマッチの情報は`/fes`で取得できます。', color=EmbedColor.IS_FEST)
                embed.add_field(name='開催期間', value='```{} ～ {}```'.format(start_date, end_date), inline=False)

                return await interaction.followup.send(embed=embed)
            else:
                stages = result['stages']

                # generate stage image
                img = ImageUtil.gen_image_by_url(url1=stages[0]['image'], url2=stages[1]['image'])
                img_binary = io.BytesIO()
                img.save(img_binary, format='PNG')
                img_binary.seek(0)

                # discord File
                file = discord.File(img_binary, filename='image.png')

                embed = discord.Embed(title='splatoon3 ステージ情報 | {}'.format(match.name), description='', color=EmbedColor.LIST.get(result['rule']['key']))
                embed.add_field(name='開催期間', value='```{} ～ {}```'.format(start_date, end_date), inline=False)

                if match.value != 'regular':
                    embed.add_field(name='ルール', value='```{}```'.format(result['rule']['name']), inline=False)

                embed.add_field(name='ステージ', value='```{}\n{}```'.format(stages[0]['name'], stages[1]['name']), inline=False)
                embed.set_thumbnail(url=spla3_util.get_match_logo_path(result['rule']['key']))
                embed.set_image(url='attachment://image.png')

                return await interaction.followup.send(embed=embed, file=file)
        elif time.value == 'schedule':
            pages = []
            images = []

            for i, result in enumerate(res):
                start_date = datetime.datetime.strptime(result['start_time'], '%Y-%m-%dT%H:%M:%S%z').strftime('%m/%d %H:%M')
                end_date = datetime.datetime.strptime(result['end_time'], '%Y-%m-%dT%H:%M:%S%z').strftime('%m/%d %H:%M')

                # check fest
                if result['is_fest']:
                    embed = discord.Embed(title='splatoon3 ステージ情報 | フェス開催中', description='フェスマッチの情報は`/fes`で取得できます。', color=EmbedColor.IS_FEST)
                    embed.add_field(name='開催期間', value='```{} ～ {}```'.format(start_date, end_date), inline=False)
                    pages.append(embed)
                    images.append([None, None])
                else:
                    stages = result['stages']

                    embed = discord.Embed(title='splatoon3 ステージ情報 | {}'.format(match.name), description='', color=EmbedColor.LIST.get(result['rule']['key']))
                    embed.add_field(name='開催期間', value='```{} ～ {}```'.format(start_date, end_date), inline=False)

                    if match.value != 'regular':
                        embed.add_field(name='ルール', value='```{}```'.format(result['rule']['name']), inline=False)

                    embed.add_field(name='ステージ', value='```{}\n{}```'.format(stages[0]['name'], stages[1]['name']), inline=False)
                    embed.set_thumbnail(url=spla3_util.get_match_logo_path(result['rule']['key']))

                    pages.append(embed)
                    images.append([stages[0]['image'], stages[1]['image']])

            return await PaginationUtil.start(interaction=interaction, match=match.value, embeds=pages, images=images)

    @app_commands.command(
        name='coop',
        description='スプラトゥーン3のサーモンラン情報を表示します。',
    )
    @app_commands.describe(time='時間帯を選択してください')
    @app_commands.rename(time='時間帯')
    @app_commands.choices(
        time=[
            app_commands.Choice(name='現在', value='now'),
            app_commands.Choice(name='次', value='next'),
            app_commands.Choice(name='スケジュール', value='schedule'),
        ]
    )
    async def coop3(self: Self, interaction: discord.Interaction, time: app_commands.Choice[str]) -> None:
        await interaction.response.defer()
        request_url = SPLA3_BASE_URL + 'coop-grouping' + '/' + time.value

        spla3_util = Spla3Util()
        res = spla3_util.fetch_schedule(request_url)

        if len(res) == 0:
            embed = discord.Embed(title='データ取得失敗', description='データの取得に失敗しました。\n時間を空けて再度実行してください。\n改善されない場合はお問い合わせください。', colour=discord.Colour.red())
            return await interaction.followup.send(embed=embed)

        if time.value == 'now' or time.value == 'next':
            result = res[0]
            start_date = datetime.datetime.strptime(result['start_time'], '%Y-%m-%dT%H:%M:%S%z').strftime('%m/%d %H:%M')
            end_date = datetime.datetime.strptime(result['end_time'], '%Y-%m-%dT%H:%M:%S%z').strftime('%m/%d %H:%M')

            # check big run
            if result['is_big_run']:
                embed = discord.Embed(title='splatoon3 ステージ情報 | ビッグラン開催中', description='', color=EmbedColor.COOP)
            else:
                embed = discord.Embed(title='splatoon3 ステージ情報 | サーモンラン', description='', color=EmbedColor.COOP)

            weapons = result['weapons']
            embed.add_field(name='開催期間', value='```{} ～ {}```'.format(start_date, end_date), inline=False)
            embed.add_field(name='ステージ', value='```{}```'.format(result['stage']['name']), inline=False)
            embed.add_field(name='支給ブキ', value='```{}\n{}\n{}\n{}```'.format(weapons[0]['name'], weapons[1]['name'], weapons[2]['name'], weapons[3]['name']), inline=False)
            embed.set_thumbnail(url=spla3_util.get_match_logo_path('COOP'))
            embed.set_image(url=result['stage']['image'])

            return await interaction.followup.send(embed=embed)
        elif time.value == 'schedule':
            pages = []
            images = []

            for i, result in enumerate(res):
                start_date = datetime.datetime.strptime(result['start_time'], '%Y-%m-%dT%H:%M:%S%z').strftime('%m/%d %H:%M')
                end_date = datetime.datetime.strptime(result['end_time'], '%Y-%m-%dT%H:%M:%S%z').strftime('%m/%d %H:%M')

                # check big run
                if result['is_big_run']:
                    embed = discord.Embed(title='splatoon3 ステージ情報 | ビッグラン開催中', description='', color=EmbedColor.IS_FEST)
                else:
                    embed = discord.Embed(title='splatoon3 ステージ情報 | サーモンラン', description='', color=EmbedColor.COOP)

                weapons = result['weapons']
                embed.add_field(name='開催期間', value='```{} ～ {}```'.format(start_date, end_date), inline=False)
                embed.add_field(name='ステージ', value='```{}```'.format(result['stage']['name']), inline=False)
                embed.add_field(name='支給ブキ', value='```{}\n{}\n{}\n{}```'.format(weapons[0]['name'], weapons[1]['name'], weapons[2]['name'], weapons[3]['name']), inline=False)
                embed.set_thumbnail(url=spla3_util.get_match_logo_path('COOP'))
                embed.set_image(url=result['stage']['image'])

                pages.append(embed)
                images.append([result['stage']['image']])

            return await PaginationUtil.start(interaction=interaction, match='coop', embeds=pages, images=images)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Spla3Cog(bot))
