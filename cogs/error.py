import discord
from discord.ext import commands
from discord.ext.commands import Cog


import traceback


class ErrorCog(Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            emb = discord.Embed(title="エラーが発生しました", description="そのコマンドは見つかりませんでした。ごめんなさい。", color=discord.Color.red())
            await ctx.reply(embed=emb)
        elif isinstance(error, commands.NotOwner):
            emb = discord.Embed(title="エラーが発生しました", description="そのコマンドは見つかりませんでした。ごめんなさい。", color=discord.Color.red())
            await ctx.reply(embed=emb)
        elif isinstance(error, commands.PrivateMessageOnly):
            emb = discord.Embed(title="エラーが発生しました", description="このコマンドはDM(ダイレクトメッセージ)でのみ利用可能です。", color=discord.Color.red())
            await ctx.reply(embed=emb)
            await ctx.author.send("DM限定コマンドはこちらで送信してください。")
        elif isinstance(error, commands.MissingRequiredArgument):
            emb = discord.Embed(title="エラーが発生しました", description="パラメータが不足しています。ヘルプコマンドなどで確認してください。", color=discord.Color.red())
            await ctx.reply(embed=emb)
        elif isinstance(error, commands.CommandOnCooldown):
            emb = discord.Embed(title="エラーが発生しました", description=f"現在クールダウン中です...\nあと{error.retry_after}秒後に再試行してください。", color=discord.Color.red())
            await ctx.reply(embed=emb)
        elif isinstance(error, commands.UserNotFound):
            emb = discord.Embed(title="エラーが発生しました", description="ユーザーが見つかりませんでした。", color=discord.Color.red())
            await ctx.reply(embed=emb)
        elif isinstance(error, commands.HybridCommandError):
            ch = 1021461009925415062

            view = discord.ui.View()
            style = discord.ButtonStyle.link
            Server = discord.ui.Button(style=style, label="Support server", url="https://discord.gg/zwbvUPTZHc")
            Twitter = discord.ui.Button(style=style, label="Twitter", url="https://twitter.com/syukur1ch")
            GitHub = discord.ui.Button(style=style, label="GitHub", url="https://github.com/syu-kuri/Spla3bot")
            view.add_item(item=Server)
            view.add_item(item=Twitter)
            view.add_item(item=GitHub)

            embed = discord.Embed(title="エラー情報", description="", color=0xf00)
            if isinstance(ctx.channel, discord.channel.DMChannel):
                embed.add_field(name="エラー発生サーバー名", value=ctx.channel, inline=False)
                embed.add_field(name="エラー発生サーバーID", value=ctx.channel.id, inline=False)
                embed.add_field(name="エラー発生ユーザー名", value=ctx.author.name, inline=False)
                embed.add_field(name="エラー発生ユーザーID", value=ctx.author.id, inline=False)
                embed.add_field(name="エラー発生コマンド", value=ctx.message.content, inline=False)
                embed.add_field(name="発生エラー", value=error, inline=False)

                t = f"```py\n{''.join(traceback.TracebackException.from_exception(error))}```"
                embed.add_field(name="発生エラー", value=t if len(t < 2048) else f"```py\n{error}\n```", inline=False)

                m = await self.bot.get_channel(ch).send(embed=embed)
                emb = discord.Embed(title="エラーが発生しました", description=f"何らかのエラーが発生しました。ごめんなさい。\nこのエラーについて問い合わせるときは下記のコードも一緒にお知らせください", color=discord.Color.red())
                emb.add_field(name="問い合わせID", value=m.id)
                await ctx.reply(embed=emb, view=view)
            else:
                embed.add_field(name="エラー発生サーバー名", value=ctx.guild.name, inline=False)
                embed.add_field(name="エラー発生サーバーID", value=ctx.guild.id, inline=False)
                embed.add_field(name="エラー発生ユーザー名", value=ctx.author.name, inline=False)
                embed.add_field(name="エラー発生ユーザーID", value=ctx.author.id, inline=False)
                embed.add_field(name="エラー発生コマンド", value=ctx.message.content, inline=False)
                embed.add_field(name="発生エラー", value=error, inline=False)
                m = await self.bot.get_channel(ch).send(embed=embed)
                emb = discord.Embed(title="エラーが発生しました", description=f"何らかのエラーが発生しました。ごめんなさい。\nこのエラーについて問い合わせるときは下記のコードも一緒にお知らせください", color=discord.Color.red())
                emb.add_field(name="問い合わせID", value=m.id)
                await ctx.reply(embed=emb, view=view)
        else:
            ch = 1021461009925415062

            view = discord.ui.View()
            style = discord.ButtonStyle.link
            Server = discord.ui.Button(style=style, label="Support server", url="https://discord.gg/zwbvUPTZHc")
            Twitter = discord.ui.Button(style=style, label="Twitter", url="https://twitter.com/syukur1ch")
            GitHub = discord.ui.Button(style=style, label="GitHub", url="https://github.com/syu-kuri/Spla3bot")
            view.add_item(item=Server)
            view.add_item(item=Twitter)
            view.add_item(item=GitHub)

            embed = discord.Embed(title="エラー情報", description="", color=0xf00)
            if isinstance(ctx.channel, discord.channel.DMChannel):
                embed.add_field(name="エラー発生サーバー名", value=ctx.channel, inline=False)
                embed.add_field(name="エラー発生サーバーID", value=ctx.channel.id, inline=False)
                embed.add_field(name="エラー発生ユーザー名", value=ctx.author.name, inline=False)
                embed.add_field(name="エラー発生ユーザーID", value=ctx.author.id, inline=False)
                embed.add_field(name="エラー発生コマンド", value=ctx.message.content, inline=False)
                embed.add_field(name="発生エラー", value=error, inline=False)

                t = f"```py\n{''.join(traceback.TracebackException.from_exception(error))}```"
                embed.add_field(name="発生エラー", value=t if len(t < 2048) else f"```py\n{error}\n```", inline=False)

                m = await self.bot.get_channel(ch).send(embed=embed)
                emb = discord.Embed(title="エラーが発生しました", description=f"何らかのエラーが発生しました。ごめんなさい。\nこのエラーについて問い合わせるときは下記のコードも一緒にお知らせください", color=discord.Color.red())
                emb.add_field(name="問い合わせID", value=m.id)
                await ctx.reply(embed=emb, view=view)
            else:
                embed.add_field(name="エラー発生サーバー名", value=ctx.guild.name, inline=False)
                embed.add_field(name="エラー発生サーバーID", value=ctx.guild.id, inline=False)
                embed.add_field(name="エラー発生ユーザー名", value=ctx.author.name, inline=False)
                embed.add_field(name="エラー発生ユーザーID", value=ctx.author.id, inline=False)
                embed.add_field(name="エラー発生コマンド", value=ctx.message.content, inline=False)
                embed.add_field(name="発生エラー", value=error, inline=False)
                m = await self.bot.get_channel(ch).send(embed=embed)
                emb = discord.Embed(title="エラーが発生しました", description=f"何らかのエラーが発生しました。ごめんなさい。\nこのエラーについて問い合わせるときは下記のコードも一緒にお知らせください", color=discord.Color.red())
                emb.add_field(name="問い合わせID", value=m.id)
                await ctx.reply(embed=emb, view=view)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ErrorCog(bot))