import discord
from discord.ext import commands
import sqlite3
from config import config
from discord_components import DiscordComponents, Button, ButtonStyle, Select, SelectOption
#<<------------->>
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
#<<хелп--------->>
    @commands.command(aliases = ['Хелп', 'хелп', 'Помощь', 'помощь', 'Команды', 'команды'])
    async def help(self, ctx):
        prefix = self.get_prefix(self.cursor, ctx.message)
        emb = discord.Embed(title = "💚 Меню помощи:", url = 'https://discord.com/api/oauth2/authorize?client_id=857936255245484052&permissions=8&scope=bot', 
        description=f"**{config.NAME}** - полностью бесплатный и многофункциональный бот, включающий в себя как основные, так и неформальные функции.\n\n*< >* - обязательный аргумент.\n*[ ]* - дополнительный аргумент.\n", colour=config.EMBED_COLOR)
        emb.set_footer(text=f'{config.DEVELOPER} • {config.NAME} {config.VERSION}')
        await ctx.reply(embed = emb, components = [
            Select(
                placeholder = "Выберите категорию:",
                options = [
                    SelectOption(label = "Веселье", value = "Веселье", emoji='✨'),
                    SelectOption(label = "Экономика", value = "Экономика", emoji='🏆'),
                    SelectOption(label = "Майнинг", value = "Майнинг", emoji='💹'),
                    SelectOption(label = "Музыка", value = "Музыка", emoji='📯'),
                    SelectOption(label = "Модерация", value = "Модерация", emoji='📌'),
                    SelectOption(label = "Утилиты", value = "Утилиты", emoji='🔎'),
                    SelectOption(label = "Дополнительно", value = "Дополнительно", emoji='💎'),
                    SelectOption(label = "Настройки", value = "Настройки", emoji='🔒')
                ])], mention_author = False)

        embed1 = discord.Embed(title="✨ Веселье", colour=config.EMBED_COLOR, description = f'\
        \n> `{prefix}респект <@Участник>` - респекнуть пользователю.\
        \n> `{prefix}краш [@Участник]` - узнать уровень симпатии.\
        \n> `{prefix}дуэль <@Участник>` - вступить в схватку.\
        \n> `{prefix}судьба <вопрос>` - предсказать свою судьбу.\
        \n> `{prefix}орёл/решка` - базовая игра орёл или решка.\
        \n> `{prefix}панда/птица/енот` - очароваться животными.')

        embed2 = discord.Embed(title="🏆 Экономика", colour=config.EMBED_COLOR, description = f'\
        \n> `{prefix}баланс [@Участник]` - узнать баланс.\
        \n> `{prefix}вбанк <сумма>` - отправить сбережения в банк.\
        \n> `{prefix}кража <@Участник>` - совершить кражу.\
        \n> `{prefix}бонус` - получить ежечасный бонус.\
        \n> `{prefix}работы` - список доступных работ.\
        \n> `{prefix}передать <@Участник> <сумма>` - передать сбережения.\
        \n> `{prefix}пожертвовать <сумма>` - избавиться от сбережений.\
        \n> `{prefix}казино <сумма>` - сыграть в казино.\
        \n> `{prefix}магаз` - магазин сервера.\
        \n> `{prefix}купить <@Роль>` - купить привелегию из магазина.')

        embed3 = discord.Embed(title="💹 Майнинг:", colour=config.EMBED_COLOR, description = f'\
        \n> `{prefix}млист` - список видеокарт.\
        \n> `{prefix}мкупить <видеокарта>` - купить видеокарту.\
        \n> `{prefix}мпродать <видеокарта>` - продать видеокарту.\
        \n> `{prefix}мферма [@Участник]` - Майнинг ферма.\
        \n> `{prefix}мстарт` - начать майнить.')

        embed4 = discord.Embed(title="📯 Музыка:", colour=config.EMBED_COLOR, description = f'\
        \n> `{prefix}войти` - подключение бота к вашему каналу.\
        \n> `{prefix}плей <название>/[ссылка]` - воспроизведение композиции.\
        \n> `{prefix}громкость <число>` - регулирование звука.\
        \n> `{prefix}пауза/продолжить` - пауза/продолжение воспроизведения.\
        \n> `{prefix}очередь` - плейлист.\
        \n> `{prefix}скип` - пропустить композицию.\
        \n> `{prefix}стоп` - отсоединение бота.')

        embed5 = discord.Embed(title="📌 Модерация", colour=config.EMBED_COLOR, description = f'\
        \n> `{prefix}очист [число]` - очистить чат.\
        \n> `{prefix}кик <@Участник> [Причина]` - кикнуть пользователя.\
        \n> `{prefix}бан <@Участник> [Причина]` - забанить пользователя.\
        \n> `{prefix}банлист` - списки банов.\
        \n> `{prefix}варн <@Участник> [Причина]` - выдать предупреждение пользователю.\
        \n> `{prefix}удалварн <@Участник>` - очистить предупреждения пользователю.\
        \n> `{prefix}варны [@Участник]` - предупреждения пользователя.\
        \n> `{prefix}слоумод <секунды>` - активация медленного режима.\
        \n> `{prefix}разбан <ID>` - разбанить пользователя.\
        \n> `{prefix}мут <@Участник> <минуты> [Причина]` - заглушить пользователя.\
        \n> `{prefix}размут <@Участник> [Причина]` - разглушить пользователя.\
        \n> `{prefix}объява <текст>` - разместить объявление.\
        \n> `{prefix}опрос <текст>` - разместить опрос.')

        embed6 = discord.Embed(title="🔎 Утилиты", colour=config.EMBED_COLOR, description = f'\
        \n> `{prefix}пинг` - узнать задержку.\
        \n> `{prefix}кастом` - список кастомных команд.\
        \n> `{prefix}личка <@Участник> <текст>` - отправить пользователю послание.\
        \n> `{prefix}ютуб <запрос>` - найти видео на YouTube.\
        \n> `{prefix}сказать <текст>` - написать от лица бота.\
        \n> `{prefix}слова <текст>` - подсчитать слова в предложении.\
        \n> `{prefix}поворот <текст>` - отзеркалить текст.\
        \n> `{prefix}ава [@Участник]` - вывести аватарку в чат.\
        \n> `{prefix}юзер [@Участник]` - информация о пользователе.\
        \n> `{prefix}сервера` - список серверов, использующих {config.NAME}.')

        embed7 = discord.Embed(title="💎 Дополнительно:", colour=config.EMBED_COLOR, description = f'\
        \n> `{prefix}донат` - поддержать разработчика.\
        \n> `{prefix}инвайт` - пригласить бота на Ваш сервер.\
        \n> `{prefix}поддержка` - войти на сервер поддержки.')

        embed8 = discord.Embed(title="🔒 Настройки", colour=config.EMBED_COLOR, description = f'\
        \n> `{prefix}префикс <префикс>` - установить префикс.\
        \n> `{prefix}команда <название> <ответ>` - добавить кастомную команду.\
        \n> `{prefix}удалком <название>` - удалить кастомную команду.\
        \n> `{prefix}установить <@Участник> <сумма>` - установить пользователю баланс.\
        \n> `{prefix}добавить <@Участник> <сумма>` - добавить пользователю баланс.\
        \n> `{prefix}устбанк <@Участник> <сумма>` - установить пользователю банк.\
        \n> `{prefix}доббанк <@Участник> <сумма>` - добавить пользователю банк.\
        \n> `{prefix}вмагаз <@Роль> <сумма>` - добавить роль в магазин сервера.\
        \n> `{prefix}измагаза <@Роль>` - изъять роль из магазина сервера.\
        \n> `{prefix}мвыдать <@Участник> <видеокарта>` - выдать пользователю видеокарту.\
        \n> `{prefix}мубрать <@Участник> <видеокарта>` - изъять у пользователя видеокарту.')
        
        while True:
            try:
                event = await self.bot.wait_for("select_option", check=None)
                label = event.values[0]
                if label == "Веселье":
                    await event.respond(embed = embed1, ephemeral=True)
                elif label == "Экономика":
                    await event.respond(embed = embed2, ephemeral=True)
                elif label == "Майнинг":
                    await event.respond(embed = embed3, ephemeral=True)
                elif label == "Музыка":
                    await event.respond(embed = embed4, ephemeral=True)
                elif label == "Модерация":
                    await event.respond(embed = embed5, ephemeral=True)
                elif label == "Утилиты":
                    await event.respond(embed = embed6, ephemeral=True)
                elif label == "Дополнительно":
                    await event.respond(embed = embed7, ephemeral=True)
                elif label == "Настройки":
                    await event.respond(embed = embed8, ephemeral=True)

            except discord.NotFound:
                print("error.")

    @commands.command(aliases = ['Работы', 'работы', 'Работа', 'работа'])
    async def work(self, ctx):
        emb = discord.Embed(color=config.EMBED_COLOR, title = f'🦺 Работы:', description = f'\
        \n> **Зарплаты:**\
        \n> Шахтёр: **{config.WORKER}**\
        \n> Пилот: **{config.PILOT}**\
        \n> Доктор: **{config.MEDIC}**\
        \n\
        \n> **Перерывы:**\
        \n> Шахтёр: **1 час**\
        \n> Пилот: **2 часа**\
        \n> Доктор: **3 часа**')
        await ctx.reply(embed=emb, mention_author=False)

    @commands.command(aliases= ['Бот', 'бот', 'Ботинфо', 'ботинфо'])
    async def bot(self, ctx):
        guild_name = ctx.guild.name
        prefix = self.get_prefix(self.cursor, ctx.message)
        emb = discord.Embed(color=config.EMBED_COLOR, title = f'💚 Информация о {config.NAME}:', description = f'\
        \n> Создатель: `{config.DEVELOPER}`\
        \n> Проект основан: `09.03.21`\
        \n> Версия: `{config.VERSION}` -> `{config.VERSION_START}`\
        \n\
        \n> **{guild_name}:**\
        \n> Префикс на сервере: `{prefix}`')
        await ctx.reply(embed=emb, mention_author=False)

    
#<<------------->>
def setup(bot):
    bot.add_cog(Info(bot))
