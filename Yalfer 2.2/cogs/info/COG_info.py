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
        self.connection = sqlite3.connect("database.db")
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
        \n`{prefix}бонус` `{prefix}работы` `{prefix}ставка <сумма>` `{prefix}пожертвовать <сумма>`\
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

    @commands.command(aliases = ['Знакомство', 'знакомство'])
    async def thehelp(self, ctx):
        prefix = self.get_prefix(self.cursor, ctx.message)
        member = ctx.message.author		
        emb1 = discord.Embed(color = config.EMBED_COLOR, title = f'Добро пожаловать, {member.name}', description = 'Я - Yalfer, ваш индивидуальный помощник.')
        emb2 = discord.Embed(color = config.EMBED_COLOR, title = ':money_with_wings: Экономика:', description = f'Деньги - залог успеха, но их надо зарботать: `{prefix}работы`, а `{prefix}бонус` поможет вам быстрее дойти до цели!\
        \nТы азартный? Да, у нас так можно! `{prefix}казино <сумма>`.\nНу вот ты заработал первые деньги, теперь время узнать совой баланс: `{prefix}бал`.\
        \nДеньги ты можешь закинуть на банковский счёт, откуда их невозможно украсть (`{prefix}кража <@участник>`): `{prefix}вбанк <сумма>`. Хочешь вернуть наличку? `{prefix}избанка <сумма>`, но помни - пока деньги в банке их нельзя потратить!\
        \nYalfer даёт возможность создавать магазины, но тут каждый владелец горазд на своё... Магазин открывается командой `{prefix}магаз`. Там же ты можешь купить привелегию: `{prefix}купить <@роль>`\
        \nYalfer любит щедрых, поэтому ты можешь передать участнику нужную сумму денег: `{prefix}передать <@участник> <сумма>`, но а если ты уж очень богат - можешь пожертвовать свои деньги: `{prefix}пожертововать <сумма>`')
        emb3 = discord.Embed(color = config.EMBED_COLOR, title = ':desktop: Майнинг:', description = f'Список доступных видеокарт: `{prefix}млист`. Вы можете майнинть, имея минимум 1 видеокарту `{prefix}мстарт`.\
        \nВсё просто, но вам нужны деньги... Они имеются? - Воу, поздравляю! Ты можешь купить свою первую видюху по команде `{prefix}мкупить <название>`.\
        \nПомни, видеокарты имеет свойство ломаться, но ты можешь продать её в любое время: `{prefix}мпродать  <название>`.')
        emb4 = discord.Embed(color = config.EMBED_COLOR, title = ':boomerang: Веселье:', description = f'От экономической деятельности тоже нужно отдыхать!\
        \nХочешь узнать свою судьбу? `{prefix}судьба <вопрос>`\
        \nВсе пользователи хороши, но на сколько процентов `{prefix}краш <@участник>`.\
        \nЧто-то понравилось? Хочешь кинуть респект? `{prefix}респект <текст>`.\
        \nВызови совего кента на дуэль `{prefix}дуэль <@участник>`.\
        \nЧто же выпадет `{prefix}монетка`.\
        \nМилые фоточки к вашим услугам `{prefix}лис`|`{prefix}кот`|`{prefix}пёс`')
        emb5 = discord.Embed(color = config.EMBED_COLOR, title = ':postal_horn: Музыка:', description = f'Музыка так успокаивает. Для включения нужно зайти в войс и прописать `{prefix}плей <название>` или же `{prefix}p <название>`\
        \nНадо отойти покушать? `{prefix}пауза` | `{prefix}продолжить`.\
        \nОткрыть плейлист `{prefix}очередь` или же `{prefix}плейлист`.\
        \nПропустить песню? Не проблема: `{prefix}скип`.\
        \n`{prefix}громкость <число>` настроит звучание.')
        emb6 = discord.Embed(color = config.EMBED_COLOR, title = ':tools: Утилиты:', description = f'\
        \nХочешь прислать участнику секретик? `{prefix}личка <@участник> <текст>` поможет!\
        \nПередать сообщение в канал через бота не помешает `{prefix}бот <текст>`.\
        \nТекст умеет переворачиваться... Не знал(-а)? {prefix}поворот <текст>\
        \nКак быстро найти ролик на YouTube? `{prefix}ютуб <запрос>`\
        \nТы активен? посмотри свой уровень! `{prefix}лвл`\
        \nНужно посчитать слова в предложении? `{prefix}слова <текст>`')
        emb7 = discord.Embed(color = config.EMBED_COLOR, title = ':pushpin: Модерация:', description = f'`{prefix}хелп`')
        emb8 = discord.Embed(color = config.EMBED_COLOR, description = f'{member.mention}, приятного использования!')
        emb8.set_footer(text = f'Есть вопросы? {prefix}хелп')
        embeds = [emb1, emb2, emb3, emb3, emb4, emb5, emb6, emb7, emb8]
        reactions = ['🔻', '🔺']
        message = await ctx.reply(embed=emb1, mention_author=False)
        page = pag(self.bot, message, use_more=False, embeds=embeds, reactions = reactions, timeout=100000000)
        await page.start()

#Cog-----------------------------------------------------
def setup(bot):
    bot.add_cog(Info(bot))
