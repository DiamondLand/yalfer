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
		emb = discord.Embed(colour = discord.Color.blurple(), title = 'СПИСОК КОМАНД:', description = f'**Фановые:**\
		\n---\
        \n`{prefix}утро` / `{prefix}ночь` `{prefix}дата` `{prefix}личка [@участник][текст]` `{prefix}судьба [вопрос]` `{prefix}дуэль @Участник` `{prefix}орёл` / `{prefix}решка` `{prefix}лиса` / `{prefix}пёс` / `{prefix}кошка`\
        \n--\
		\n**Модерация:**\
		\n---\
        \n`{prefix}кик` `{prefix}бан` `{prefix}очист [число]` `{prefix}префикс [префикс]`\
		\n--\
        \n**Утилиты:**\
		\n---\
		\n`{prefix}лвлхелп` `{prefix}экохелп` `{prefix}майнингхелп` `{prefix}бот` `{prefix}лвл` `{prefix}сервер` `{prefix}серверлист`\
		\n--\
		\n**Музыка:**\
		\n---\
        \n`{prefix}плей [песня]` `{prefix}пауза` `{prefix}продолжить` `{prefix}стоп`\
		\n--\
        \n**Экономика:**\
		\n---\
        \n`{prefix}лвлденьги [ваш лвл]` `{prefix}бал` `{prefix}бонус [@участник]` `{prefix}пбал [@участник]` `{prefix}передать [@участник] [сумма]` `{prefix}магаз` `{prefix}купить [@роль]`\
		\n---\
		\n**Экономика (Админы):**\
		\n---\
		\n`{prefix}устбал [@участник][сумма]` `{prefix}доббал [@участник][сумма]` `{prefix}удалбал [@участник] [сумма]` `{prefix}добмагаз [@роль] [цена]` `{prefix}удалмагаз [@роль]`\
		\n---\
		\n**Майнинг:**\
		\n--\
		\n`{prefix}майнинг` `{prefix}мкупить [название]` `{prefix}мферма` `{prefix}мстарт` `{prefix}мстоп`')
		emb.set_footer(text = f'Добавить бота: {prefix}добавить | Патреон: {prefix}патреон')
		await ctx.send(embed = emb)

	#лвлхелп-------------------------------------------------
	@commands.command(aliases = ['Лвлхелп', 'лвлхелп'])
	async def lvlhelp(self, ctx):
		prefix = self.get_prefix(self.cursor, ctx.message)
		emb = discord.Embed(colour = discord.Color.blurple(), title = 'О системе уровней:', description = f'\
		\nВы пишите сообщения и получаете уровень, который можете обменять на игровые деньги:\
		\n---\
		\nДопустим, что вы получили `3` лвл и пишите `{prefix}лвлденьги 3`. Вы обнуляете свой уровень, но получаете деньги, в зависимости от уровня\
		\n---\
		\nИгровые монеты вы можете тратить на покупку ролей в магазине сервера или на видеокарты для майнинга.\
		\n---\
		\nОзнакомиться с командами: `{prefix}хелп`')
		emb.set_footer(text = 'Спасибо за выбор Yalfera')
		await ctx.send(embed = emb)

	#экохелп-------------------------------------------------
	@commands.command(aliases = ['Экохелп', 'экохелп'])
	async def ecohelp(self, ctx):
		prefix = self.get_prefix(self.cursor, ctx.message)
		emb = discord.Embed(colour = discord.Color.blurple(), title = 'О системе экономики:', description = f'\
		\nДеньги получаются за майнинг `{prefix}майнингхелп`, ежечасный бонус `{prefix}бонус` и активность `{prefix}лвлхелп`: Допустим, у вас `1000000` игровых монет. Вы можете купить роль в магазине сервера или вложиться в майнинг. Также, вы можете передавать деньги другому пользователю и тд...\
		\n---\
		\n`{prefix}бал` - ваш баланс\
		\n---\
	 	\n`{prefix}пбал [@участник]` - баланс @участника\
		\n---\
		\n`{prefix}бонус [@участник]` - получение ежечасного бонуса (15000)\
		\n---\
		\n`{prefix}лвлденьги [ваш лвл]` - получение денег за ваш лвл\
		\n---\
		\n`{prefix}устбал [@участник][сумма]` - установить баланс @участнику\
		\n---\
		\n`{prefix}доббал [@участник][сумма]` - добавить денег @участнику\
		\n---\
		\n`{prefix}удалбал [@участник] [сумма]` - удалить с баланса @участника сумму\
		\n---\
		\n`{prefix}передать [@участник] [сумма]` - передать деньги **из своего кошелька**\
		\n---\
		\n`{prefix}добмагаз [@роль] [цена]` - поставить @роль в магазин сервера\
		\n---\
		\n`{prefix}удалмагаз [@роль]` - удалить @роль из магазина сервера\
		\n---\
		\n`{prefix}магаз` - магазин сервера\
		\n---\
		\n`{prefix}купить [@роль]` - купить @роль\
		\n---\
		\nОзнакомиться с остальными командами бота: `{prefix}хелп`')
		emb.set_footer(text = 'Спасибо за выбор Yalfera')
		await ctx.send(embed = emb)

	#майнингхелп-------------------------------------------------
	@commands.command(aliases = ['Майнингхелп', 'майнингхелп'])
	async def mininghelp(self, ctx):
		prefix = self.get_prefix(self.cursor, ctx.message)
		emb = discord.Embed(colour = discord.Color.blurple(), title = 'О системе майнинга:', description = f'\
		\nДопустим, у вас `10000000`. Вы покупаете нужную вам видеокарту. Затем, запускаете майнинг: процесс пошёл, вы получаете коины, но не надо забывать, что есть счёт за электричество / видеокарта может сломаться!\
		\nУ разных видеокарт разные шансы на поломку, разная прибыль и тд...\
		\n---\
		\n`{prefix}майнинг` - перечень видеокарт\
		\n---\
		\n`{prefix}мкупить [название]` - купить видеокарту\
		\n---\
		\n`{prefix}мферма` - ваша ферма\
		\n---\
		\n`{prefix}мстарт` - начать майнинг\
		\n---\
		\n`{prefix}мстоп` - остановить майнинг\
		\n---\
		\nОзнакомиться с остальными командами бота: `{prefix}хелп`')
		emb.set_footer(text = 'Спасибо за выбор Yalfera | Майнинг был полностью придуман Огурчик#9017')
		await ctx.send(embed = emb)

	#бот---------------------------------------------------------
	@commands.command(aliases = ['Бот', 'бот'])
	async def bot(self, ctx):
		prefix = self.get_prefix(self.cursor, ctx.message)
		emb = discord.Embed(colour = discord.Color.blurple(), title = 'О боте:', description = f'\
		\n---\
		\n**Бот с экономикой, системой майнинга, модерацией и различными фановыми командами**\
		\n---\
		\nСоздатель: `Simofor#3533`\
		\n---\
		\nСоавтор систем: `Огурчик#9017`\
		\n---\
		\nДата начала работы: `21.03.21`\
		\n---\
		\nВерсия: `1.1` | Выход версии: `05.05.21`\
		\n---\
		\nПрефикс по умолчанию `+` | Префикс на сервере `{prefix}`\
		\n---\
		\nОзнакомиться с командами: `{prefix}хелп`\
		\n---\
		\nПатреон: `{prefix}патреон` | Сервер поддержки: `{prefix}дс` | Добавить бота на сервер: `{prefix}добавить`')
		emb.set_footer(text = 'Спасибо за выбор Yalfera')
		await ctx.send(embed = emb)

	#сервер-------------------------------------------------
	@commands.command(aliases = ['Сервер', 'сервер'])
	async def s_info(self, ctx):
		prefix = self.get_prefix(self.cursor, ctx.message)
		embed = discord.Embed(color = discord.Color.blurple(), title="Информация о сервере:")
		guild_id = ctx.guild.id
		guild_name = ctx.guild.name
		guild_owner = ctx.guild.owner
		embed.add_field(name="**Название сервера:**", value=f"`{guild_name}`", inline=False)
		embed.add_field(name="Регион:", value=f"`{ctx.guild.region}`", inline=False)
		embed.add_field(name="**Префикс на сервере:**", value=f"`{prefix}`", inline=False)
		embed.add_field(name="**Количество пользователей:**", value=f"`{ctx.guild.member_count}`")
		embed.add_field(name="**ID сервера:**", value=f"`{guild_id}`")
		embed.add_field(name=f"**Категории и каналы [**`{len(ctx.guild.categories) + len(ctx.guild.channels)}`**]:**",
						value=f"**Категории:** `{len(ctx.guild.categories)}` | **Текстовые каналы:** `{len(ctx.guild.text_channels)}` | **Голосовые каналы:** `{len(ctx.guild.voice_channels)}`",
						inline=False)
		embed.add_field(name=f"**Дата создания:**", value=f"`{ctx.guild.created_at}`")
		embed.set_thumbnail(url=ctx.guild.icon_url)
		await ctx.send(embed=embed)

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
