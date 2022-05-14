import discord
import error_send
import sqlite3
import urllib
import re
import datetime
from config import config
from discord.ext import commands
from discord_components import DiscordComponents, Button, ButtonStyle
#<<------------->>
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
#<<пинг--------->>
    @commands.command(aliases = ['Пинг', 'пинг'])
    async def ping(self, ctx):
        emb = discord.Embed(title = '🏓 Понг!', description=f"Задержка составляет: `{round(self.bot.latency * 1000)} ms`", colour=config.EMBED_COLOR)
        date = datetime.datetime.today()
        emb.set_footer(icon_url = ctx.author.avatar_url, text=f'{date.strftime("%D")} • {date.strftime("%H:%M")}')
        await ctx.reply(embed=emb, mention_author=False)

#<<донат--------->>    
    @commands.command(aliases = ['Донат', 'донат'])
    async def donate(self, ctx):
        emb = discord.Embed(title = '💚 Пожертвовать', url = 'https://yoomoney.ru/to/410017396938739', 
        description=f"Донат - один из важных атрибутов поддержки автора. Именно Вы являетесь ключом к разработке {config.NAME}. Каждый пользователь улучшает проект, вкладывая в него свою веру и внимание, а донат является самым быстрым способом визуализации своего интереса, причём далеко не единственным!", colour=config.EMBED_COLOR)
        emb.set_footer(text=f'{config.DEVELOPER} • {config.NAME}  {config.VERSION}')
        await ctx.reply(embed=emb, mention_author=False,
        components = [
            [Button(style=ButtonStyle.URL, label = "Комьюнити", url='https://discord.gg/FBvkhNhcUT'),
            Button(style=ButtonStyle.URL, label = "Пожертвовать", url='https://yoomoney.ru/to/410017396938739')]
        ],)

#<<личка-------->>
    @commands.command(aliases = ['Личка', 'личка', 'ЛС', 'лс'])
    async def dm(self, ctx, member: discord.Member, *, text):
        await ctx.channel.purge(limit = 1)
        author = ctx.message.author
        emb = discord.Embed(color=config.EMBED_COLOR, title = '💌 Личное сообщение:', description = f'> Результат выполнения:\n\
        > **Доставлено!**')
        date = datetime.datetime.today()
        emb.set_footer(icon_url = ctx.author.avatar_url, text=f'{date.strftime("%D")} • {date.strftime("%H:%M")}')
        await ctx.send(embed = emb)

        emb = discord.Embed(color=config.EMBED_COLOR, title = '💌 Личное сообщение:', description = f'{author.mention} передал тебе: *{text}*')
        date = datetime.datetime.today()
        emb.set_footer(icon_url = ctx.author.avatar_url, text=f'{date.strftime("%D")} • {date.strftime("%H:%M")}')
        await member.send(embed = emb)

#<<ютуб--------->>
    @commands.command(aliases = ['Ютуб', 'ютуб', 'Ютьюб', 'ютьюб'])
    async def youtube(self, ctx, *, search):
        query_string = urllib.parse.urlencode({'search_query': search})
        html_content = urllib.request.urlopen('http://www.youtube.com/results?' + query_string)
        search_results = re.findall(r"watch\?v=(\S{11})", html_content.read().decode())
        await ctx.reply(embed = discord.Embed(color=config.EMBED_COLOR, title = '❤ YouTube:', description = f"Запрос `{search}` был обработан:"),
        components = [
            Button(style=ButtonStyle.URL, label = "Смотреть", url='http://www.youtube.com/watch?v='+search_results[0])
        ],
        mention_author=False)

#<<сказать------>>
    @commands.command(aliases = ['Сказать', 'сказать'])
    async def say(self, ctx, *, text):
        await ctx.channel.purge(limit = 1)
        emb = discord.Embed(color=config.EMBED_COLOR, title = '😺 Сказать:', description=f'> {text}')
        date = datetime.datetime.today()
        emb.set_footer(icon_url = ctx.author.avatar_url)
        await ctx.send(embed=emb)

#<<аватарка----->>
    @commands.command(aliases=['ава', 'Ава', 'аватарка', 'Аватарка'])
    async def avatar(self, ctx, member: discord.Member = None):
        if member == None:
            avatar = ctx.author.avatar_url
        else:
            avatar = member.avatar_url
        await ctx.reply(avatar, mention_author=False)

#<<слова-------->>
    @commands.command(aliases=['слова', 'Слова'])
    async def letters(self, ctx, *args):
        emb = discord.Embed(color=config.EMBED_COLOR, title = '🔍 Подсчёт слов:', description = f"В данном сообщении `{len(args)}` слов(-а)")
        await ctx.reply(embed=emb, mention_author=False)  
        
#<<поворот------>>
    @commands.command(aliases = ['Поворот', 'поворот', 'Переворот', 'переворот'])
    async def flip(self, ctx, *, text: str):
        t_rev = text[::-1].replace("@", "@\u200B").replace("&", "&\u200B")
        emb = discord.Embed(color=config.EMBED_COLOR, title = '🔄 Переворот:', description=f"> Результат выполнения:\n\
        > **{t_rev}**")
        await ctx.reply(embed=emb, mention_author=False)
    
#<<инвайт------->>
    @commands.command(aliases = ['Инвайт', 'инвайт', 'Пригласить', 'пригласить'])
    async def invite(self, ctx):
        embed = discord.Embed(color=config.EMBED_COLOR, title = '💚 Добавить', url = 'https://discord.com/api/oauth2/authorize?client_id=857936255245484052&permissions=8&scope=bot', 
        description = f"**{config.NAME}** уже спешит к Вам на сервер!")
        embed.set_footer(text=f'{config.DEVELOPER} • {config.NAME}  {config.VERSION}')
        await ctx.reply(embed=embed,
        components = [
            [Button(style=ButtonStyle.URL, label = "Комьюнити", url='https://discord.gg/FBvkhNhcUT'),
            Button(style=ButtonStyle.URL, label = "Добавить", url='https://discord.com/api/oauth2/authorize?client_id=857936255245484052&permissions=8&scope=bot')]
        ],
        mention_author=False)
        
#<<сервера------>>
    @commands.command(aliases = ['Сервера', 'сервера'])
    async def servers(self, ctx):
        emb = discord.Embed(color = config.EMBED_COLOR, title = '💚 Пользователи:', url = 'https://discord.com/api/oauth2/authorize?client_id=857936255245484052&permissions=8&scope=bot',
        description="\n".join(map(str, self.bot.guilds)))
        await ctx.reply(embed=emb,
        components = [
            [Button(style=ButtonStyle.URL, label = "Комьюнити", url='https://discord.gg/FBvkhNhcUT'),
            Button(style=ButtonStyle.URL, label = "Добавить", url='https://discord.com/api/oauth2/authorize?client_id=857936255245484052&permissions=8&scope=bot')]
        ],
        mention_author=False)
#<<------------->>
def setup(bot):
   bot.add_cog(Utility(bot))