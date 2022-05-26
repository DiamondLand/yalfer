import discord
import random
import sqlite3
import asyncio
import time
from discord.ext import commands
from cogs.economic.economic import EconomicCogFunctionality
from cogs.economic.mining import MiningCogFunctionality


class MiningCog(commands.Cog):

	def __init__(self, client):
		self.client = client
		self.prises = {
			"rtx 3090": "10000000",
			"RTX 3090": "10000000",
			"6900 xt": "2000000",
			"6900 XT": "2000000",
			"rtx 3080": "1500000",
			"6800 xt": "1300000",
			"rtx 3070": "1300000",
			"rtx 2080 ti": "1000000",
			"rtx a6000": "1000000",
			"rx 6700 xt": "1000000",
			"titan v": "800000",
			"rtx 2080": "600000",
			"rtx 2070": "500000",
			"rx 5700": "200000",
			"rtx 2060": "120000"
			}

		self.moneys_ = {
			"rtx 3090": "10000000",
			"RTX 3090": "10000000",
			"6900 xt": "2000000",
			"6900 XT": "2000000",
			"rtx 3080": "1500000",
			"6800 xt": "1300000",
			"rtx 3070": "1300000",
			"rtx 2080 ti": "1000000",
			"rtx a6000": "1000000",
			"rx 6700 xt": "1000000",
			"titan v": "800000",
			"rtx 2080": "600000",
			"rtx 2070": "500000",
			"rx 5700": "200000",
			"rtx 2060": "120000"
		}
		self.chances_to_broke = [
			12, 12, 13, 13, 8, 17, 8, 9, 11, 2, 14, 10, 18, 47, 50
		]
		self.connection = sqlite3.connect("database.db")
		self.cursor = self.connection.cursor()

	@commands.command(aliases = ['Майнинг', 'майнинг'])
	async def m_info(self, ctx):
		await ctx.send(
			file=discord.File(fp="videocards.png")
		)
	@commands.command(aliases = ['Мкупить', 'мкупить'])
	async def m_buy(self, ctx, *videocard_words):
		videocard = " ".join(videocard_words)
		if not (videocard in list(self.prises.keys())):
			emb = discord.Embed(colour = discord.Color.red(), description = 'Такой видеокарты `не существует`!')
			await ctx.send(embed = emb)
		else:
			user_data = EconomicCogFunctionality.get_user_data(
				self.cursor,
				self.connection,
				ctx.message.author,
				ctx.guild
			)
			wallet = user_data[3]
			member = ctx.message.author
			server = ctx.guild
			prise = int(self.prises[videocard])

			if prise > wallet:
				emb = discord.Embed(colour = discord.Color.red(), description = 'У вас нет такой суммы!')
				await ctx.send(embed = emb)
			else:
				MiningCogFunctionality.add_videocard(
					videocard,
					1,
					server,
					member,
					self.cursor,
					self.connection
				)
				EconomicCogFunctionality.change_balance(
					self.cursor,
					self.connection,
					ctx.message.author,
					ctx.guild,
					- prise,
					user_data
				)
				emb = discord.Embed(colour = discord.Color.green(), description = f'Вы купили `{videocard}`!')
				await ctx.send(embed = emb)

	@commands.command(aliases = ['Мпродать', 'мпродать'])
	async def m_sold(self, ctx, *videocard_words):
		videocard = " ".join(videocard_words)
		if not (videocard in list(self.moneys_.keys())):
			emb = discord.Embed(colour = discord.Color.red(), description = 'У вас `нет` такой видеокарты!')
			await ctx.send(embed = emb)
		else:
			user_data = EconomicCogFunctionality.get_user_data(
				self.cursor,
				self.connection,
				ctx.message.author,
				ctx.guild
			)
			wallet = user_data[3]
			member = ctx.message.author
			server = ctx.guild
			prise = int(self.prises[videocard])
			MiningCogFunctionality.delete_videocards(
                    videocard,
                    1,
                    server,
					ctx.message.author,
                    self.cursor,
                    self.connection
                )
			EconomicCogFunctionality.change_balance(
					self.cursor,
					self.connection,
					ctx.message.author,
					ctx.guild,
					+ prise,
					user_data
				)
			emb = discord.Embed(color = 0xffd700, description = f'Вы продали `{videocard}`!')
			await ctx.send(embed = emb)
			
	@commands.has_permissions(administrator=True)
	@commands.command(aliases = ['Мубрать', 'мубрать', 'Мудалить', 'мудалить'])
	async def m_remove(self, ctx, member: discord.Member, amount = 0, *videocard_words):
		videocard = " ".join(videocard_words)
		if not (videocard in list(self.moneys_.keys())):
			emb = discord.Embed(colour = discord.Color.red(), description = f'У {member.mention} `нет` такой видеокарты!')
			await ctx.send(embed = emb)
		else:
			"""
			:param ctx:
			:param member:
			:return:
			"""
			user_data = EconomicCogFunctionality.get_user_data(
				self.cursor,
				self.connection,
				member,
				ctx.guild
			)
			wallet = user_data[3]
			prise = int(self.prises[videocard])
			MiningCogFunctionality.delete_videocards(
					videocard,
					amount,
					ctx.guild,
					member,
                    self.cursor,
                    self.connection
                )
			
			emb = discord.Embed(color = 0xffd700, description = f'{member.mention} лишился `{amount}` `{videocard}`!')
			await ctx.send(embed = emb)

	@commands.has_permissions(administrator=True)
	@commands.command(aliases = ['Мвыдать', 'мвыдать'])
	async def m_get(self, ctx, member: discord.Member, amount = 1, *videocard_words):
		videocard = " ".join(videocard_words)
		if not (videocard in list(self.prises.keys())):
			emb = discord.Embed(colour = discord.Color.red(), description = 'Такой видеокарты `не существует`!')
			await ctx.send(embed = emb)
		else:
			"""
			:param ctx:
			:param member:
			:return:
			"""
			user_data = EconomicCogFunctionality.get_user_data(
				self.cursor,
				self.connection,
				member,
				ctx.guild
			)
			prise = int(self.prises[videocard])
			wallet = user_data[3]
			MiningCogFunctionality.add_videocard(
						videocard,
						amount,
						ctx.guild,
						member,
						self.cursor,
						self.connection,
					)
			
			emb = discord.Embed(color = 0xffd700, description = f'{member.mention} получил `{amount}` `{videocard}`!')
			await ctx.send(embed = emb)

	@commands.command(aliases = ['Мферма', 'мферма'])
	async def m_my_farm(self, ctx):
		self.cursor.execute(
			"SELECT * FROM graphics_cards WHERE guild_id = ? AND member_id = ?",
			(
				ctx.guild.id,
				ctx.message.author.id
			)
		)
		result = self.cursor.fetchall()
		author = ctx.message.author
		embed = discord.Embed(
			description=f"Майнинг ферма пользователя {author.mention}!",
			color = 0xffd700
		)
		embed.set_thumbnail(
			url=ctx.message.author.avatar_url
		)
		for element in result:
			if element[3] != 0:
				embed.add_field(
					name=f"Видеокарты `{element[2].title()}`:",
					value=f"Количество: `{element[3]}`"
				)
		await ctx.send(embed=embed)

	@commands.command(aliases = ['Мстоп', 'мстоп'])
	async def m_end(self, ctx):
		MiningCogFunctionality.DB_mining_set(
			ctx=ctx,
			cursor=self.cursor,
			connection=self.connection,
			value=False
		)
		emb = discord.Embed(color = 0xffd700, description = 'Сессия завершена!')
		await ctx.send(embed = emb)

	@commands.command(aliases = ['Мстарт', 'мстарт'])
	@commands.cooldown(1, 500, commands.BucketType.member)
	async def m_start(self, ctx):
		self.cursor.execute("SELECT * FROM is_mining WHERE guild_id = ? AND member_id = ?",
							(ctx.guild.id, ctx.message.author.id))
		is_mining_data = self.cursor.fetchone()
		if is_mining_data is None:
			pass
		elif is_mining_data[2] == 0:
			pass
		else:
			author = ctx.message.author
			emb = discord.Embed(colour = discord.Color.red(), description = f'{author.mention}, вы уже майните! Остановка предыдущей сессии...')
			await ctx.send(embed = emb)
			MiningCogFunctionality.DB_mining_set(
				ctx=ctx,
				cursor=self.cursor,
				connection=self.connection,
				value=False
			)
		MiningCogFunctionality.DB_mining_set(
			ctx=ctx,
			cursor=self.cursor,
			connection=self.connection,
			value=True
		)
		self.connection.commit()
		user_data = EconomicCogFunctionality.get_user_data(
			self.cursor,
			self.connection,
			ctx.message.author,
			ctx.guild
		)
		server = ctx.guild
		member = ctx.message.author
		emb = discord.Embed(color = 0xffd700, description = 'Запуск видюх...')
		discord_message =  await ctx.send(embed = emb)
		await asyncio.sleep(3)
		mined_moneys = 0
		total_time = 0
		while True:
			self.cursor.execute(
				"SELECT * FROM is_mining WHERE guild_id = ? AND member_id = ?",
				(
					server.id,
					member.id
				)
			)
			is_mining_data = self.cursor.fetchone()
			if is_mining_data is None:
				return
			elif is_mining_data[2] == 0:
				return
			author = ctx.message.author
			embed = discord.Embed(
				description=f"Майнинг ферма пользователя {author.mention}!",
				color = 0xffd700
			)
			embed.set_thumbnail(
				url=ctx.message.author.avatar_url
			)
			self.cursor.execute(
				"SELECT * FROM graphics_cards WHERE guild_id = ? AND member_id = ?",
				(
					ctx.guild.id,
					ctx.message.author.id
				)
			)
			result = self.cursor.fetchall()
			for element in result:
				if element[3] != 0:
					msg = ""
					mined_moneys_for_one = int(
						self.moneys_[element[2]]
					) / (6 * 2 * 20) * random.randint(1, 40) * element[3]
					mined_moneys += mined_moneys_for_one
					msg += f"Кэш: `{round(mined_moneys_for_one, 2)}`, растёт каждые `30` сек!\n"
					chances_to_broke = int(
						self.chances_to_broke[list(self.prises.keys()).index(str(element[2]))]
					)
					un_chances = 100 - chances_to_broke
					amount_of_broken = 0

					for i in range(int(element[3])):
						random_number = random.randint(0, un_chances)
						another_random_number = random.randint(0, un_chances)
						if (random_number == another_random_number):
							amount_of_broken += 1

					if amount_of_broken != 0:
						msg += f"`{amount_of_broken}` видеокарт сломано\n"
						MiningCogFunctionality.delete_videocards(
							element[2],
							amount_of_broken,
							ctx.guild,
							ctx.message.author,
							self.cursor,
							self.connection
						)
					embed.add_field(
						name=f"Информация о сессии с видеокартами `{element[2].title()}`:",
						value=f"{msg}"
					)
					embed.set_footer(
						text=f"Налог: {round(mined_moneys / 5, 2)} 💰\nСчет за электричество: {round(mined_moneys / 8, 2)} 💰"
					)
				await discord_message.edit(embed=embed)
				EconomicCogFunctionality.change_balance(
					self.cursor,
					self.connection,
					ctx.message.author,
					ctx.guild,
					+ mined_moneys,
					EconomicCogFunctionality.get_user_data(
						self.cursor,
						self.connection,
						ctx.message.author,
						ctx.guild,
					)
				)
			total_time += 30
			await asyncio.sleep(30)
			if total_time == 90:
				author = ctx.message.author
				emb = discord.Embed(colour = discord.Color.red(), description = f'{author.mention}, вюдюхи перегрелись...\nДля продолжения, `перезапустите`')
				await ctx.send(embed = emb)
				MiningCogFunctionality.DB_mining_set(
					ctx=ctx,
					cursor=self.cursor,
					connection=self.connection,
					value=False
				)
				return
				


# setup for cog
def setup(client):
	client.add_cog(MiningCog(client))
