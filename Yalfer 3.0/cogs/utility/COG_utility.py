import discord
import error_send
from datetime import datetime
import sqlite3
import urllib
import requests
import json
import re
import io
from bs4 import BeautifulSoup as bs
from config import config
from discord.ext import commands
from discord_components import DiscordComponents, Button, ButtonStyle

class Utility(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.connection = sqlite3.connect("database.db", timeout=10)
        self.cursor = self.connection.cursor()

    def get_prefix(self, cursor, message):
        cursor.execute(
            "SELECT * FROM prefixes WHERE guild_id = ?", 
            (
                message.guild.id
            )
        )
        result = cursor.fetchone()
        if result is not None:
            return result[1]
        else:
            return "+"
            

    #пинг--------------------------------------------------
    @commands.command(aliases = ['Пинг', 'пинг'])
    async def ping(self, ctx):
        emb = discord.Embed(description=f"**🏓Понг!**\nЗадержка составляет: `{round(self.bot.latency * 1000)}ms`", colour=config.EMBED_COLOR)
        await ctx.reply(embed=emb, mention_author=False)

    #личка--------------------------------------------------
    @commands.command(aliases = ['Личка', 'личка'])
    async def personal(self, ctx, member: discord.Member, *, text):
        await ctx.channel.purge(limit = 1)
        author = ctx.message.author
        await ctx.send(embed = discord.Embed(color=config.EMBED_COLOR, description = f"{author.mention}, слово не воробей!\nОтправляем Ваше послание?"),
        components = [
            [Button(style=ButtonStyle.green, label = "Отправить", custom_id = 'sendDM'), 
            Button(style=ButtonStyle.red, label = "Выйти", custom_id = 'nosendDM')]
        ],
        mention_author=False, delete_after=10)

        response = await self.bot.wait_for("button_click")
        if response.channel == ctx.channel:
            if response.custom_id == "sendDM":
                emb = discord.Embed(color=config.EMBED_COLOR, description = f'✅ Отправлено!')
                await ctx.send(embed = emb, mention_author=False, delete_after = 5)
                emb = discord.Embed(color=config.EMBED_COLOR, description = f'{author.mention} передал тебе: *{text}*')
                await member.send(embed = emb)
            else:
                emb = discord.Embed(color=config.EMBED_COLOR, description = f'❌ Отмена отправки!')
                await ctx.send(embed = emb, mention_author=False, delete_after = 5)

    #ютуб--------------------------------------------------
    @commands.command(aliases = ['Ютуб', 'ютуб', 'Ютьюб', 'ютьюб'])
    async def youtube(self, ctx, *, search):
        author = ctx.message.author
        query_string = urllib.parse.urlencode({'search_query': search})
        html_content = urllib.request.urlopen('http://www.youtube.com/results?' + query_string)
        search_results = re.findall(r"watch\?v=(\S{11})", html_content.read().decode())
        await ctx.reply(embed = discord.Embed(color=config.EMBED_COLOR, description = f"Запрос `{search}` был обработан:"),
        components = [
            Button(style=ButtonStyle.URL, label = "Смотреть", url='http://www.youtube.com/watch?v='+search_results[0])
        ],
        mention_author=False)

    #бот-------------------------------------------------
    @commands.command(aliases = ['Бот', 'бот'])
    async def bot(self, ctx, *, text):
        await ctx.channel.purge(limit = 1)
        author = ctx.message.author
        emb = discord.Embed(color=config.EMBED_COLOR, description=f'{author.mention}: {text}')
        await ctx.send(embed=emb)

    #слова-------------------------------------------------
    @commands.command(aliases=['Слова', 'слова'])
    async def wordcount(self, ctx, *args):
        emb = discord.Embed(color=config.EMBED_COLOR, description = f"В данном сообщении `{len(args)}` слов(-а)")
        await ctx.reply(embed=emb, mention_author=False) 

    #поворот-------------------------------------------------
    @commands.command(aliases = ['поворот', 'Поворот', 'Переворот', 'переворот'])
    async def reverse(self, ctx, *, text: str):
        t_rev = text[::-1].replace("@", "@\u200B").replace("&", "&\u200B")
        emb = discord.Embed(color=config.EMBED_COLOR, description=f"🔁 {t_rev}")
        await ctx.reply(embed=emb)
    
    #добавить--------------------------------------------------------------------------
    @commands.command(aliases = ['инвайт', 'Инвайт', 'Пригласить', 'пригласить'])
    async def add(self, ctx):
        await ctx.reply(embed = discord.Embed(color=config.EMBED_COLOR, description = f"`{config.NAME}` уже спешит к Вам на сервер!"),
        components = [
            [Button(style=ButtonStyle.URL, label = "Комьюнити", url='https://discord.gg/FBvkhNhcUT'),
            Button(style=ButtonStyle.URL, label = "Добавить", url='https://discord.com/api/oauth2/authorize?client_id=857936255245484052&permissions=8&scope=bot')]
        ],
        mention_author=False)
        
    #сервера--------------------------------------------------------------------------
    @commands.command(aliases = ['сервера', 'Сервера'])
    async def guilds(self, ctx):
        emb = discord.Embed(color = config.EMBED_COLOR, description=f'`{config.NAME}` используется на:')
        emb.set_footer(text = "\n".join(map(str, self.bot.guilds)))
        await ctx.reply(embed=emb,
        components = [
            [Button(style=ButtonStyle.URL, label = "Комьюнити", url='https://discord.gg/FBvkhNhcUT'),
            Button(style=ButtonStyle.URL, label = "Добавить", url='https://discord.com/api/oauth2/authorize?client_id=857936255245484052&permissions=8&scope=bot')]
        ],
        mention_author=False)

    #сервер--------------------------------------------------------------------------
    @commands.command(aliases = ['Сервер', 'сервер'])
    async def s_info(self, ctx):
        guild_name = ctx.guild.name
        embed = discord.Embed(title=f"Информация о {guild_name}", color = config.EMBED_COLOR)
        guild_id = ctx.guild.id
        embed.add_field(name="Количество пользователей:", value=f"`{ctx.guild.member_count}`")
        embed.add_field(name="ID сервера:", value=f"`{guild_id}`")
        embed.add_field(name=f"Категории и каналы: `{len(ctx.guild.categories) + len(ctx.guild.channels)}`:", value=f"Категории `{len(ctx.guild.categories)}` | Текстовые каналы: `{len(ctx.guild.text_channels)}` | Голосовые каналы: `{len(ctx.guild.voice_channels)}`", inline=False)
        embed.add_field(name=f"Дата создания:", value=f"||{ctx.guild.created_at}||")
        embed.set_thumbnail(url=ctx.guild.icon_url)
        await ctx.send(embed=embed)


#Cog-----------------------------------------------------
def setup(bot):
   bot.add_cog(Utility(bot))