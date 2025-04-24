from datetime import datetime

import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Cog

from config.config import CREATOR_NAME, version_info


class InfoCog(Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(
        name='about',
        description='Botの情報を返します'
    )
    @app_commands.guilds(discord.Object(id=808959433010577439))
    async def about(self, interaction: discord.Interaction):
        await interaction.response.defer()

        guilds = len(self.bot.guilds)

        raw_ping = self.bot.latency
        ping = round(raw_ping * 1000)

        embed = discord.Embed(title='Bot Infomation', description='', color=discord.Colour.blue())
        embed.add_field(name='Version', value='v{0.major}.{0.minor}.{0.micro}-{0.releaselevel}'.format(version_info), inline=True)
        embed.add_field(name='Library', value='{}'.format('discord.py'), inline=True)
        embed.add_field(name='Creator', value='{}'.format(CREATOR_NAME), inline=True)
        embed.add_field(name='Server', value='{}guilds'.format(guilds), inline=True)
        embed.add_field(name='Ping', value='{}ms'.format(ping), inline=True)
        embed.set_footer(text='{}'.format(datetime.now().strftime('%Y/%m/%d %H:%M:%S')), icon_url=self.bot.user.display_avatar.url)

        await interaction.followup.send(embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(InfoCog(bot))
