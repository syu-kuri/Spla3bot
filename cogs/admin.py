import discord
from discord.ext import commands


class AdminCog(commands.Cog, name="Bot製作者のみ使用可能コマンド"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command(name="reload", hidden=True)
    @commands.is_owner()
    async def reload(self, inter, extension):
        await self.bot.reload_extension(f"cogs.{extension}")
        embed = discord.Embed(title='リロード成功', description=f'{extension} Cog をリロードしました。', color=0xff00c8)
        await inter.reply(embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(AdminCog(bot))
