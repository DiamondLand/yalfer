import discord
from discord.ext import commands
import sqlite3

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
     
	#хелп-------------------------------------------------
	@commands.command(aliases = ['Хелп', 'хелп', 'Помощь', 'помощь', 'Команды', 'команды'])
	async def help(self, ctx): 
		prefix = self.get_prefix(self.cursor, ctx.message)
		emb = discord.Embed(colour = discord.Color.blurple(), title = 'СПИСОК КОМАНД:', description = f'\
		\n**:small_orange_diamond: Фан:**\
        \n`{prefix}утро`/`{prefix}ночь` `{prefix}дата` `{prefix}личка [@участник][текст]` `{prefix}судьба [вопрос]`\n`{prefix}дуэль [@участник]` `{prefix}орёл`/`{prefix}решка` `{prefix}лиса`/`{prefix}пёс`/`{prefix}кошка`\
		\n\
		\n**:small_orange_diamond: Модерация:**\
        \n`{prefix}кик [@участник][причина]` `{prefix}бан [@участник][причина]` `{prefix}почист [число]` `{prefix}очист` `{prefix}доброль [@участник][@роль]`\n`{prefix}удалроль [@участник][@роль]` `{prefix}префикс [префикс]`\
		\n\
		\n**:small_orange_diamond: Утилиты:**\
		\n`{prefix}лвл` `{prefix}бот` `{prefix}серверлист`\
		\n\
		\n**:small_orange_diamond: Музыка:**\
        \n`{prefix}плей [название / ютуб-ссылка]` `{prefix}пауза` `{prefix}продолжить` `{prefix}стоп`\
		\n\
		\n**:small_orange_diamond: Экономика:**\
        \n`{prefix}лвлденьги [ваш лвл]` `{prefix}бал` `{prefix}бонус` `{prefix}пожертвовать [сумма]`\n`{prefix}пбал [@участник]` `{prefix}передать [@участник] [сумма]` `{prefix}магаз` `{prefix}купить [@роль]`\
		\n\
		\n**:small_orange_diamond: Экономика_админы:**\
		\n`{prefix}устбал [@участник][сумма]` `{prefix}доббал [@участник][сумма]`\n`{prefix}удалбал [@участник] [сумма]` `{prefix}добмагаз [@роль] [цена]` `{prefix}удалмагаз [@роль]`\
		\n\
		\n**~~Майнинг:~~**\
		\n~~`{prefix}майнинг` `{prefix}мкупить [видеокарта]` `{prefix}мпродать [видеокарта]` `{prefix}мферма` `{prefix}мстарт` `{prefix}мстоп`~~\
		\n\
		\n**~~Майнинг_админы:~~**\
		\n~~`{prefix}мубрать [@участник][кол-во][видеокарта]`\n`{prefix}мвыдать [@участник][кол-во][видеокарта]`~~\
		\n\
		\n**:small_orange_diamond: Описание команд:**\
		\n**Подробнее** ознакомиться с командами вам поможет `{prefix}[категория]хелп`.\n**Пример:** `{prefix}фанхелп`\n')
		emb.set_footer(text = f'Добавить бота: {prefix}добавить | Патреон: {prefix}патреон')
		await ctx.send(embed = emb)

	@commands.command(aliases = ['Фанхелп', 'фанхелп'])
	async def funhelp(self, ctx):
		prefix = self.get_prefix(self.cursor, ctx.message)
		emb = discord.Embed(colour = discord.Color.blurple(), title = 'О фановых командах:', description = f'\
		\n:small_orange_diamond:\
		\n`{prefix}утро`/`{prefix}ночь` - пожелания\
		\n`{prefix}дата` - дата и время\
		\n`{prefix}личка [@участник][текст]` - передача сообщений в ЛС\
		\n`{prefix}судьба [вопрос]` - игра "Шар судьбы"\
		\n`{prefix}дуэль [@участник]` - игра "Дуэль"\
		\n`{prefix}орёл`/`{prefix}решка` - игра "Орёл или Решка"\
		\n`{prefix}лиса`/`{prefix}пёс`/`{prefix}кошка` - фоточки\
		\n:small_orange_diamond:\
		\nОзнакомиться с остальными командами: `{prefix}хелп`')
		emb.set_footer(text = 'Спасибо за выбор Yalfera')
		await ctx.send(embed = emb)

	@commands.command(aliases = ['Музыкахелп', 'музыкахелп'])
	async def musichelp(self, ctx):
		prefix = self.get_prefix(self.cursor, ctx.message)
		emb = discord.Embed(colour = discord.Color.blurple(), title = 'О фановых командах:', description = f'\
		\nПеред началом прослушивания, войдите в войс\
		\n:small_orange_diamond:\
		\n`{prefix}плей [название / ютуб-ссылка]` - воспроизведение\
		\n`{prefix}пауза` - поставить воспроизведение на паузу\
		\n`{prefix}продолжить` - продолжить воспроизведение\
		\n`{prefix}стоп` - окончание воспроизведения | Выход бота из войса\
		\n:small_orange_diamond:\
		\nОзнакомиться с остальными командами: `{prefix}хелп`')
		emb.set_footer(text = 'Спасибо за выбор Yalfera')
		await ctx.send(embed = emb)

	@commands.command(aliases = ['Модерацияхелп', 'модерацияхелп'])
	async def moderationhelp(self, ctx):
		prefix = self.get_prefix(self.cursor, ctx.message)
		emb = discord.Embed(colour = discord.Color.blurple(), title = 'О модерации:', description = f'\
		\nРазумеется, данную категорию могут использовать только те, у кого в роли есть **Права Администратора**!\
		\n:small_orange_diamond:\
		\n`{prefix}кик [@участник][причина]` - кик\
		\n`{prefix}бан [@участник][причина]` - бан\
		\n`{prefix}почист [число]` - удалить [число] сообщений\
		\n`{prefix}очист` - удалить все сообщения в чате\
		\n`{prefix}доброль [@участник][@роль]` - выдать роль\
		\n`{prefix}удалроль [@участник][@роль]` - изъять роль\
		\n`{prefix}префикс [префикс]` - изменить префикс\
		\n:small_orange_diamond:\
		\nОзнакомиться с остальными командами: `{prefix}хелп`')
		emb.set_footer(text = 'Спасибо за выбор Yalfera')
		await ctx.send(embed = emb)

	#лвлхелп-------------------------------------------------
	@commands.command(aliases = ['Утилитыхелп', 'утилитыхелп', 'Утилитхелп', 'утилитхелп', 'Лвлхелп', 'лвлхелп'])
	async def lvlhelp(self, ctx):
		prefix = self.get_prefix(self.cursor, ctx.message)
		emb = discord.Embed(colour = discord.Color.blurple(), title = 'О системе уровней:', description = f'\
		\nВы пишите сообщения и получаете уровень, который можете обменять на игровые деньги:\
		\nДопустим, что вы получили `3` лвл и пишите `{prefix}лвлденьги 3`. Вы обнуляете свой уровень, но получаете деньги, в зависимости от уровня\
		\nИгровые монеты вы можете тратить на покупку ролей в магазине сервера или на видеокарты для майнинга (`{prefix}экономикахелп`)\
		\n:small_orange_diamond:\
		\n`{prefix}лвл` - ваш лвл и сколько осталось до нового\
		\n`{prefix}бот` - информация о боте\
		\n`{prefix}серверлист` - информация о серверах, где есть Yalfer\
		\n:small_orange_diamond:\
		\nОзнакомиться с остальными командами: `{prefix}хелп`')
		emb.set_footer(text = 'Спасибо за выбор Yalfera')
		await ctx.send(embed = emb)

	#экохелп-------------------------------------------------
	@commands.command(aliases = ['Экохелп', 'экохелп', 'Экономикахелп', 'экономикахелп', 'Экономика_админыхелп', 'экономика_админыхелп', 'Экономика_Админыхелп', 'экономика_Админыхелп'])
	async def ecohelp(self, ctx):
		prefix = self.get_prefix(self.cursor, ctx.message)
		emb = discord.Embed(colour = discord.Color.blurple(), title = 'О системе экономики:', description = f'\
		\nДеньги получаются за майнинг `{prefix}майнингхелп`, ежечасный бонус `{prefix}бонус` и активность `{prefix}лвлхелп`: Допустим, у вас `1000000` игровых монет. Вы можете купить роль в магазине сервера или вложиться в майнинг. Также, вы можете передавать деньги другому пользователю и тд...\
		\nРазумеется, модерационные команды этой категории могут использовать только те, у кого в роли есть **Права Администратора**!\
		\n:small_orange_diamond:\
		\n`{prefix}бал` - ваш баланс\
	 	\n`{prefix}пбал [@участник]` - баланс @участника\
		\n`{prefix}бонус` - получение ежечасного бонуса (15000)\
		\n`{prefix}пожертвовать [сумма]` - удалить [сумму] со своего аккаунта\
		\n`{prefix}лвлденьги [ваш лвл]` - получение денег за ваш лвл\
		\n`{prefix}устбал [@участник][сумма]` - установить баланс @участнику\
		\n`{prefix}доббал [@участник][сумма]` - добавить денег @участнику\
		\n`{prefix}удалбал [@участник] [сумма]` - удалить с баланса @участника сумму\
		\n`{prefix}передать [@участник] [сумма]` - передать деньги **из своего кошелька**\
		\n`{prefix}добмагаз [@роль] [цена]` - поставить @роль в магазин сервера\
		\n`{prefix}удалмагаз [@роль]` - удалить @роль из магазина сервера\
		\n`{prefix}магаз` - магазин сервера\
		\n`{prefix}купить [@роль]` - купить @роль\
		\n:small_orange_diamond:\
		\nОзнакомиться с остальными командами бота: `{prefix}хелп`')
		emb.set_footer(text = 'Спасибо за выбор Yalfera')
		await ctx.send(embed = emb)

	#майнингхелп-------------------------------------------------
	@commands.command(aliases = ['Майнингхелп', 'майнингхелп', 'Майнинг_админыхелп', 'майнинг_админыхелп', 'Майнинг_Админыхелп', 'майнинг_Админыхелп'])
	async def mininghelp(self, ctx):
		prefix = self.get_prefix(self.cursor, ctx.message)
		emb = discord.Embed(colour = discord.Color.blurple(), title = 'О системе майнинга:', description = f'\
		\nДопустим, у вас `10000000`. Вы покупаете нужную вам видеокарту. Затем, запускаете майнинг: процесс пошёл, вы получаете коины, но не надо забывать, что есть счёт за электричество / видеокарта может сломаться!\
		\nУ разных видеокарт разные шансы на поломку, разная прибыль и тд...\
		\nРазумеется, модерационные команды этой категории могут использовать только те, у кого в роли есть **Права Администратора**!\
		\n:small_orange_diamond:\
		\n`{prefix}майнинг` - перечень видеокарт\
		\n`{prefix}мкупить [видеокарта]` - купить видеокарту\
		\n`{prefix}мпродать [видеокарта]` - продать видеокарту\
		\n`{prefix}мубрать [@участник][кол-во][видеокарта]` - изъять видеокарту у @участника\
		\n`{prefix}мвыдать [@участник][кол-во][видеокарта]` - выдать видеокарту @участнику\
		\n`{prefix}мферма` - ваша ферма\
		\n`{prefix}мстарт` - начать майнинг\
		\n`{prefix}мстоп` - остановить майнинг\
		\n:small_orange_diamond:\
		\nОзнакомиться с остальными командами бота: `{prefix}хелп`')
		emb.set_footer(text = 'Спасибо за выбор Yalfera | Майнинг был полностью придуман Огурчик#9017')
		await ctx.send(embed = emb)

	#бот---------------------------------------------------------
	@commands.command(aliases = ['Бот', 'бот'])
	async def bot(self, ctx):
		prefix = self.get_prefix(self.cursor, ctx.message)
		emb = discord.Embed(colour = discord.Color.blurple(), title = 'О боте:', description = f'\
		\n**Бот с экономикой, системой майнинга, модерацией и различными фановыми командами**\
		\n:small_orange_diamond:\
		\nСоздатель: `Simofor#3533`\
		\nСоавтор систем: `Огурчик#9017`\
		\nДата начала работы: `21.03.21`\
		\nВерсия: `1.1.2` | Выход версии: `19.05.21`\
		\nПрефикс по умолчанию `+` | Префикс на сервере `{prefix}`\
		\n:small_orange_diamond:\
		\nОзнакомиться с командами: `{prefix}хелп`\
		\nПатреон: `{prefix}патреон` | Сервер поддержки: `{prefix}дс`|\n Добавить бота на сервер: `{prefix}добавить`')
		emb.set_footer(text = 'Спасибо за выбор Yalfera')
		await ctx.send(embed = emb)


	#патреон-------------------------------------------------
	@commands.command(aliases = ['Патреон', 'патреон', 'донат', 'Донат'])
	async def patreon(self, ctx):
		emb = discord.Embed(colour = discord.Color.blurple(), title = 'Patreon', url = 'https://www.patreon.com/simoforyalferdiscordbot' )
		emb.add_field(name = '`Поддержка на Patreon`', value = 'Для тех, кто хочет `поддержать` мои старания', inline = False)
		await ctx.send(embed = emb)

	#добавить-----------------------------------------------
	@commands.command(aliases = ['Добавить', 'добавить'])
	async def add(self, ctx):
	   emb = discord.Embed(colour = discord.Color.blurple(), title = 'Добавить', url = 'https://discord.com/api/oauth2/authorize?client_id=829311432335032321&permissions=8&scope=bot')
	   emb.add_field(name = '`Добавить бота`', value = 'Для тех, кто хочет `добавить бота` на свой сервер', inline = False)
	   await ctx.send(embed = emb)

	#дс------------------------------------------------------
	@commands.command(aliases = ['Дс', 'дс'])
	async def discord(self, ctx):
	   emb = discord.Embed(colour = discord.Color.blurple(), title = 'Сервер', url = 'https://discord.gg/ZJzBU8BZ/swdHNG7Jye')
	   emb.add_field(name = '`Дискорд сервер`', value = 'Для тех, кто хочет `зайти на сервер поддержки`', inline = False)
	   await ctx.send(embed = emb)


#Cog-----------------------------------------------------
def setup(bot):
   bot.add_cog(Info(bot))
