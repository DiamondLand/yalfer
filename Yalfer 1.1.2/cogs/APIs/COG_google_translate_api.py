import discord
import asyncio
import googletrans
from discord.ext import commands
from googletrans import Translator
from cogs.APIs.google_translate import GoogleTranslateCogFunctionality


class GoogleTransApi(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.translator = Translator()

    @commands.command()
    async def translate(self, ctx, src, dist, *args):
        """ Отправляет в текстовый канал текст,
        переведенный из языка src в язык dist """
        text = " ".join(args)
        total = GoogleTranslateCogFunctionality.get_translated_text(
            text,
            src,
            dist
        )
        await asyncio.sleep(0.3)
        await ctx.send(
            total
        )

    @commands.command()
    async def translate_send(self, ctx, member: discord.Member, src, dist, *args):
        text = " ".join(args)
        total = GoogleTranslateCogFunctionality.get_translated_text(
            text,
            src,
            dist
        )
        try:
            await ctx.channel.purge(limit=1)
        except:
            pass
        await member.send(total)

    @commands.command()
    async def translate_msg(self, ctx, src, dist, *args):
        text = " ".join(args)
        total = GoogleTranslateCogFunctionality.get_translated_text(
            text,
            src,
            dist
        )
        try:
            await ctx.channel.purge(limit=1)
        except:
            pass
        await ctx.send(
            f"<@{ctx.author.id}> said (by translateAPI): {total}"
        )


def setup(client):
    client.add_cog(GoogleTransApi(client))
