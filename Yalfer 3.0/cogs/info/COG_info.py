from tabnanny import check
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
        emb = discord.Embed(title = "Меню помощи:", description=f"**Yalfer** - полностью бесплатный и многофункциональный бот, включающий в себя как основные, так и неформальные функции.\
        \nВы можете ознакомиться с ними ниже:\n\n*< >* - обязательный аргумент.\n*[ ]* - дополнительный аргумент\n\nПометка `🔴` означает то, что команду может использовать человек с активированной ролью Администратора\
        \n(Настройки сервера --> Роли --> Изменить роль --> Права доступа --> Администратор). Иные команды администрирования могут использовать люди, обладающими полномочиями для выполнения этих команд.", colour=config.EMBED_COLOR)
        emb.set_footer(text=f'{config.DEVELOPER}')
        await ctx.send(embed = emb, components = [
            Select(
                placeholder = "Выберите категорию:",
                options = [
                    SelectOption(label = "Веселье", value = "Веселье", emoji='✨'),
                    SelectOption(label = "Экономика", value = "Экономика", emoji='🏆'),
                    SelectOption(label = "Майнинг", value = "Майнинг", emoji='💹'),
                    SelectOption(label = "Музыка", value = "Музыка", emoji='📯'),
                    SelectOption(label = "Модерация", value = "Модерация", emoji='📌'),
                    SelectOption(label = "Утилиты", value = "Утилиты", emoji='🔎'),
                    #SelectOption(label = "Дополнительно", value = "Дополнительно", emoji='💎')
                ])])
        embed1 = discord.Embed(title="✨ Веселье", colour=config.EMBED_COLOR)
        embed1.add_field(name=f"{prefix}респект <текст>/[@Участник]", value="Респектуть участнику/тексту.", inline=False)
        embed1.add_field(name=f"{prefix}краш <@Участник>", value="Узнать уровень симпатии бота к участнику.", inline=False)
        embed1.add_field(name=f"{prefix}дуэль <@Участник>", value="Выбрать оружие и вступить в схватку.", inline=False)
        embed1.add_field(name=f"{prefix}судьба <вопрос>", value="Предсказать свою судьбу.", inline=False)
        embed1.add_field(name=f"{prefix}монетка", value="Перейти в панель игры.", inline=False)

        embed2 = discord.Embed(title="🏆 Экономика", colour=config.EMBED_COLOR)
        embed2.add_field(name=f"{prefix}баланс [@Участник]", value="Узнать баланс свой/участника.", inline=False)
        embed2.add_field(name=f"{prefix}вбанк <сумма>", value="Перевести деньги на банковский счёт.", inline=False)
        embed2.add_field(name=f"{prefix}избанка <сумма>", value="Перевести деньги в наличку.", inline=False)
        embed2.add_field(name=f"{prefix}кража <@Участник>", value="Украсть у участника наличку.", inline=False)
        embed2.add_field(name=f"{prefix}бонус", value="Получить ежечасный бонус", inline=False)
        embed2.add_field(name=f"{prefix}работы", value="Список доступных работ.", inline=False)
        embed2.add_field(name=f"{prefix}передать <@Участник> <сумма>", value="Поделиться наличкой с участником.", inline=False)
        embed2.add_field(name=f"{prefix}пожертвовать <сумма>", value="Избавиться от налички.", inline=False)
        embed2.add_field(name=f"{prefix}казино <сумма>", value="Сыграть в казино.", inline=False)
        embed2.add_field(name=f"{prefix}магаз ", value="Магазин сервера.", inline=False)
        embed2.add_field(name=f"{prefix}купить <@Роль> ", value="Приобрести роль из магазина сервера.", inline=False)

        embed3 = discord.Embed(title="💹 Майнинг", colour=config.EMBED_COLOR)
        embed3.add_field(name=f"{prefix}млист", value="Список видеокарт.", inline=False)
        embed3.add_field(name=f"{prefix}мкупить <видюха>", value="Купить видеокарту.", inline=False)
        embed3.add_field(name=f"{prefix}мпродать <видюха>", value="Продать видеокарту.", inline=False)
        embed3.add_field(name=f"{prefix}курс", value="Узнать курс для обмена коинов.", inline=False)
        embed3.add_field(name=f"{prefix}мферма [@Участник]", value="Списки видеокарт ваших/участника.", inline=False)
        embed3.add_field(name=f"{prefix}мстарт", value="Начать майнить.", inline=False)

        embed4 = discord.Embed(title="📯 Музыка", colour=config.EMBED_COLOR)
        embed4.add_field(name=f"{prefix}войти", value="Подключение бота к Вашему каналу.", inline=False)
        embed4.add_field(name=f"{prefix}плей <название>/[ссылка]", value="Воспроизведение композиции.", inline=False)
        embed4.add_field(name=f"{prefix}громкость <число>", value="Установить громкость от `1` до `100`.", inline=False)
        embed4.add_field(name=f"{prefix}пауза/продолжить", value="Остановить/продолжить воспроизведение.", inline=False)
        embed4.add_field(name=f"{prefix}скип", value="Пропуск композиции.", inline=False)
        embed4.add_field(name=f"{prefix}стоп", value="Отсоединение бота.", inline=False)

        embed5 = discord.Embed(title="📌 Модерация", colour=config.EMBED_COLOR)
        embed5.add_field(name=f"{prefix}очист [число]", value="Очистка чата.", inline=False)
        embed5.add_field(name=f"{prefix}роль <@Участник> <@Роль>", value="Выдать роль участнику.", inline=False)
        embed5.add_field(name=f"{prefix}удроль <@Участник> <@Роль>", value="Изъять роль у участника.", inline=False)
        embed5.add_field(name=f"{prefix}кик <@Участник> [Причина]", value="Выгнать участника с сервера.", inline=False)
        embed5.add_field(name=f"{prefix}бан <@Участник> [Причина]", value="Забанить участника на сервере.", inline=False)
        embed5.add_field(name=f"{prefix}мут <@Участник> [Причина]", value="Заглушить участника на сервере.", inline=False)
        embed5.add_field(name=f"{prefix}размут <@Участник>", value="Разглушить участника на сервере.", inline=False)
        embed5.add_field(name=f"{prefix}объява <текст>", value="Опубликовать новость на сервере.", inline=False)
        embed5.add_field(name=f"{prefix}опрос <текст>", value="Разместить голосование на сервере.", inline=False)
        embed5.add_field(name=f"{prefix}префикс <префикс> `🔴`", value="Изменить префикс бота на сервере.", inline=False)
        embed5.add_field(name=f"{prefix}установить <@Участник> <сумма> `🔴`", value="Установить наличку участнику.", inline=False)
        embed5.add_field(name=f"{prefix}добавить <@Участник> <сумма> `🔴`", value="Добавить наличку участнику.", inline=False)
        embed5.add_field(name=f"{prefix}устбанк <@Участник> <сумма> `🔴`", value="Установить банковский счёт участнику.", inline=False)
        embed5.add_field(name=f"{prefix}доббанк <@Участник> <сумма> `🔴`", value="Добавить на банковский счёт участнику.", inline=False)
        embed5.add_field(name=f"{prefix}усткоины <@Участник> <сумма> `🔴`", value="Установить коины участнику.", inline=False)
        embed5.add_field(name=f"{prefix}мвыдать <@Участник> <видеокарта> `🔴`", value="Выдать видеокарту участнику.", inline=False)
        embed5.add_field(name=f"{prefix}мубрать <@Участник> <видеокарта> `🔴`", value="Изъять видеокарту у участника.", inline=False)
        embed5.add_field(name=f"{prefix}вмагаз <@Роль> <цена> `🔴`", value="Добавить роль в магазин сервера.", inline=False)
        embed5.add_field(name=f"{prefix}измагаза <@Роль> `🔴`", value="Убрать роль из магазина сервера.", inline=False)  

        embed6 = discord.Embed(title="🔎 Утилиты", colour=config.EMBED_COLOR)
        embed6.add_field(name=f"{prefix}пинг", value="Задержка между Вами и Yalfer.", inline=False)
        embed6.add_field(name=f"{prefix}личка <@Участник> <текст>", value="Отправить участнику послание в личку.", inline=False)
        embed6.add_field(name=f"{prefix}ютуб <запрос>", value="Найти ролик на YouTube.", inline=False)
        embed6.add_field(name=f"{prefix}сказать <текст>", value="Сказать текст от лица бота.", inline=False)
        embed6.add_field(name=f"{prefix}слова <текст>", value="Посчитать слова в тексте.", inline=False)
        embed6.add_field(name=f"{prefix}поворот <текст>", value="Отзеркалить текст.", inline=False)
        embed6.add_field(name=f"{prefix}сервер", value="Информация про сервер.", inline=False)
        embed6.add_field(name=f"{prefix}сервера", value=f"Список серверов, на которых используется {config.NAME}.", inline=False)
        embed6.add_field(name=f"{prefix}инвайт", value=f"Добавить {config.NAME} на сервер/войти на сервер поддержки.", inline=False)

        #embed7 = discord.Embed(title="💎 Дополнительно", colour=config.EMBED_COLOR)
        
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
                #elif label == "Дополнительно":
                    #await event.respond(embed = embed7, ephemeral=True)

            except discord.NotFound:
                print("error.")


#Cog-----------------------------------------------------
def setup(bot):
    bot.add_cog(Info(bot))
