from xml.sax.handler import feature_namespace_prefixes
import discord
from discord.ext import commands
import sqlite3
import time
import asyncio
from config import config
from Cybernator import Paginator as pag

class Info(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.connection = sqlite3.connect("database.db", timeout=10)
        self.cursor = self.connection.cursor()

    def get_prefix(self, cursor, message):
        cursor.execute(
            "SELECT * FROM prefixes WHERE guild_id = ?", 
            (
                message.guild.id,
            )
        )
        result = cursor.fetchone()
        if result is not None:
            return result[1]
        else:
            return "+"

    @commands.command(aliases = ['Хелп', 'хелп', 'Помощь', 'помощь', 'Команды', 'команды'])
    async def help(self, ctx):
        prefix = self.get_prefix(self.cursor, ctx.message)
        emb1 = discord.Embed(color = config.EMBED_COLOR, title = f':boomerang: Веселье', description = f'`{prefix}судьба <вопрос>`\n`{prefix}монетка`\n`{prefix}дуэль <@участник>`\n`{prefix}судьба <вопрос>`\n`{prefix}респект <текст>`\n`{prefix}краш <@участник>`\n`{prefix}кот` `{prefix}пёс` `{prefix}лиса`')
        emb2 = discord.Embed(color = config.EMBED_COLOR, title = f':money_with_wings: Экономика & Майнинг', description = f'`{prefix}баланс <@участник>`\
        \n`{prefix}вбанк <сумма>` `{prefix}избанка <сумма>`\
        \n`{prefix}кража <@участник>` `{prefix}передать <@участник> <сумма>`\
        \n`{prefix}установить <@участник> <сумма>` `{prefix}добавить <@участник> <сумма>`\
        \n`{prefix}устбанк <@участник> <сумма>` `{prefix}доббанк <@участник> <сумма>`\
        \n`{prefix}устбанк <@участник> <сумма>` `{prefix}доббанк <@участник> <сумма>`\
        \n`{prefix}бонус` `{prefix}лвлденьги <уровень>` `{prefix}работы` `{prefix}ставка <сумма>` `{prefix}пожертвовать <сумма>`\
        \n`{prefix}устбанк <@участник> <сумма>` `{prefix}доббанк <@участник> <сумма>`\
        \n`{prefix}вмагаз <@роль> <цена>` `{prefix}измагаза <@роль>`\
        \n`{prefix}магаз` `{prefix}купить <@роль>`\
        \n`{prefix}млист` `{prefix}мферма`\
        \n`{prefix}мкупить <видеокарта>` `{prefix}мпродать <видеокарта>`\
        \n`{prefix}мвыдать <@участник> <видеокарта>` `{prefix}мубрать <@участник> <видеокарта>`\
        \n`{prefix}мстарт`')
        emb3 = discord.Embed(color = config.EMBED_COLOR, title = f':postal_horn: Музыка', description = f'`{prefix}войти` `{prefix}выйти`\
        \n`{prefix}плей <песня>` `{prefix}очередь` `{prefix}скип`\
        \n`{prefix}пауза` `{prefix}продолжить` `{prefix}песня`\
        \n`{prefix}громкость <звук>` `{prefix}стоп`')
        emb4 = discord.Embed(color = config.EMBED_COLOR, title = f':pushpin: Модерация', description = f'`{prefix}очист <кол-во>`\
        \n`{prefix}объявление <текст>` `{prefix}опрос <текст>`\
        \n`{prefix}роль <@участник> <@роль>` `{prefix}удроль <@участник> <@роль>`\
        \n`{prefix}кик <@участник> <причина>` `{prefix}бан <@участник> <причина>`\
        \n`{prefix}мут <@участник> <причина>` `{prefix}размут <@участник>`\
        \n`{prefix}префикс <желаемый префикс>`')
        emb5 = discord.Embed(color = config.EMBED_COLOR, title = f':tools: Утилиты', description = f'`{prefix}пинг`\
        \n`{prefix}личка <@участник> <текст>`\
        \n`{prefix}ютуб <название>`\
        \n`{prefix}бот <текст>`\
        \n`{prefix}слова <текст>`\
        \n`{prefix}поворот <текст>`\
        \n`{prefix}лвл <@участник>`\
        \n`{prefix}инвайт` `{prefix}сервер`')
        embeds = [emb1, emb2, emb3, emb4, emb5]
        reactions = ['🔻', '🔺']
        message = await ctx.reply(embed=emb1, mention_author=False)
        page = pag(self.bot, message, use_more=False, embeds=embeds, reactions = reactions, timeout=100000000)
        await page.start()

    @commands.command(aliases = ['Работы', 'работы', 'Работа', 'работа'])
    async def work(self, ctx):
        await ctx.channel.purge(limit=1)
        prefix = self.get_prefix(self.cursor, ctx.message)
        emb = discord.Embed(color=config.EMBED_COLOR, title = 'Работы:', description = f'\
        :clipboard: **Учитель**\
        \n`{prefix}учитель`. Зарплата - `{config.TEACHER}`. Перерыв - `1 ч`.\
        \n\
        \n:airplane: **Пилот**\
        \n`{prefix}пилот`. Зарплата - `{config.PILOT}`. Перерыв - `2 ч`.\
        \n\
        \n:medical_symbol:  **Доктор**\
        \n`{prefix}доктор`. Зарплата - `{config.MEDIC}`. Перерыв - `3 ч`.')
        await ctx.send(embed=emb) 

#Cog-----------------------------------------------------
def setup(bot):
    bot.add_cog(Info(bot))
