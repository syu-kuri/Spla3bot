import discord
from discord.ext import commands
from discord.ext.commands import Cog


class AdminCog(Cog, name="Bot製作者のみ使用可能コマンド"):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command(name="reload", hidden=True)
    @commands.is_owner()
    async def reload(self, inter, extension):
        self.bot.reload_extension(f"cogs.{extension}")
        embed = discord.Embed(title='リロード成功', description=f'{extension} Cog をリロードしました。', color=0xff00c8)
        await inter.reply(embed=embed)

    @commands.command(name="get_error", hidden=True)
    @commands.is_owner()
    async def get_error(self, ctx, error_id):
        ch = 982915045891665940
        channel = self.bot.get_channel(ch)
        msg = await channel.fetch_message(error_id)
        embeds = msg.embeds
        for embed in embeds:
            dict = embed.to_dict()
        fields = dict['fields']
        emb = discord.Embed(title=dict['title'] + "取得", description="", color=dict['color'])
        for field in fields:
            emb.add_field(name=field['name'], value=field['value'], inline=field['inline'])
        await ctx.reply(embed=emb)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(AdminCog(bot))