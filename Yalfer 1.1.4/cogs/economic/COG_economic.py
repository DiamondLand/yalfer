import sqlite3
import asyncio
import os
import sys
import random
import time
from discord import member
from discord.ext.commands.core import command
from loguru import logger
import discord
from discord.ext import commands
from discord.utils import get
from cogs.economic.economic import EconomicCogFunctionality
import send_translated_msg


class EconomyCog(commands.Cog):

	def __init__(self, client):
		self.client = client
		self.conn = sqlite3.connect("database.db")
		self.cursor = self.conn.cursor()
	
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

	@commands.command(aliases = ['Баланс', 'баланс', 'Бал', 'бал'])
	async def bal(self, ctx):
		"""
		:param ctx:
		:return:
		"""
		data = EconomicCogFunctionality.get_user_data(
			self.cursor,
			self.conn,
			ctx.message.author,
			ctx.guild
		)
		await EconomicCogFunctionality.send_balance_info(ctx, ctx.message.author, data)

	@commands.command(aliases = ['Пбаланс', 'пбаланс', 'Пбал', 'пбал'])
	async def gbal(self, ctx, member: discord.Member):
		"""
		:param ctx:
		:param member:
		:return:
		"""
		data = EconomicCogFunctionality.get_user_data(
			self.cursor,
			self.conn,
			member,
			ctx.guild
		)
		await EconomicCogFunctionality.send_balance_info(ctx, member, data)

	@commands.has_permissions(administrator=True)
	@commands.command(aliases = ['Устбаланс', 'устбаланс', 'Устбал', 'устбал'])
	async def set_wallet(self, ctx, member: discord.Member, balance: int):
		"""
		:param ctx:
		:param member:
		:param balance:
		:return:
		"""
		server = ctx.guild
		self.cursor.execute(
			"UPDATE economic SET wallet_balance = ? WHERE member_id = ? AND guild_id = ?",
			(
				balance,
				member.id,
				server.id
			)
		)
		self.conn.commit()
		emb = discord.Embed(color = 0xffd700, description = f'Баланс {member.mention} установлен на `{balance}`💸!')
		await ctx.send(embed = emb)
	  

	@commands.has_permissions(administrator=True)
	@commands.command(aliases = ['Доббаланс', 'доббаланс', 'Доббал', 'доббал'])
	async def add_bal(self, ctx, member: discord.Member, balance: int):
		"""
		:param ctx:
		:param member:
		:param balance:
		:return:
		"""
		user_data = EconomicCogFunctionality.get_user_data(
			self.cursor,
			self.conn,
			member,
			ctx.guild
		)
		EconomicCogFunctionality.change_balance(
			self.cursor,
			self.conn,
			member,
			ctx.guild,
			balance,
			user_data
		)
		emb = discord.Embed(color = 0xffd700, description = f'Успешно добавлено `{balance}`💸!')
		await ctx.send(embed = emb)

	@commands.command(aliases = ['Бонус', 'бонус'])
	@commands.cooldown(1, 3600, commands.BucketType.member)
	async def bonus(self, ctx, balance = 5000):
		user_data = EconomicCogFunctionality.get_user_data(
			self.cursor,
			self.conn,
			ctx.message.author,
			ctx.guild
		)
		member = ctx.message.author
		EconomicCogFunctionality.change_balance(
			self.cursor,
			self.conn,
			ctx.message.author,
			ctx.guild,
			balance,
			user_data
		)
		emb = discord.Embed(color = 0xffd700, description = f'{member.mention}, вы получили `{balance}`💸!')
		await ctx.send(embed = emb)

#доктор------------------------------------------------------------------------	
	@commands.command(aliases = ['Рдоктор', 'рдоктор'])
	@commands.cooldown(1, 10800, commands.BucketType.member)
	async def workdoctor(self, ctx, balance = 50000):
		user_data = EconomicCogFunctionality.get_user_data(
			self.cursor,
			self.conn,
			ctx.message.author,
			ctx.guild
		)
		member = ctx.message.author
		emb = discord.Embed(color = 0xffd700, title = 'Работа доктором:', description = f'Вы приходите в операционную и ждёте пациенита...')
		emb.set_footer(text = 'Ожидайте, пациента уже везут')
		await ctx.send(embed = emb)
		time.sleep(2)
		emb = discord.Embed(color = 0xffd700, title = 'Пациент прибыл!', description = f'Вы моете руки, надеваете перчатки и готовитесь к операции...')
		emb.set_footer(text = 'Ожидайте, идёт подготовка к операции')
		await ctx.send(embed = emb)
		time.sleep(2)
		emb = discord.Embed(color = 0xffd700, title = 'Подготовка завершена!', description = f'Подача наркоза. Пациент медлено засыпает...')
		emb.set_footer(text = 'Ожидайте, идёт операция')
		await ctx.send(embed = emb)
		time.sleep(3)
		emb = discord.Embed(color = 0xffd700, title = 'Завершение!', description = f'Всё прошло успешно. Пациента увозят в палату...')
		await ctx.send(embed = emb)
		member = ctx.message.author
		EconomicCogFunctionality.change_balance(
			self.cursor,
			self.conn,
			ctx.message.author,
			ctx.guild,
			balance,
			user_data
		)
		emb = discord.Embed(color = 0xffd700, description = f'{member.mention} получил `{balance}`💸 за работу доктором!')
		emb.set_footer(text = 'Возобновить данную работу можно через 2 часа!')
		await ctx.send(embed = emb)


#пилот------------------------------------------------------------
	@commands.command(aliases = ['Рпилот', 'рпилот'])
	@commands.cooldown(1, 7200, commands.BucketType.member)
	async def workpilot(self, ctx, balance = 25000):
		member = ctx.message.author
		user_data = EconomicCogFunctionality.get_user_data(
			self.cursor,
			self.conn,
			ctx.message.author,
			ctx.guild
		)
		emb = discord.Embed(color = 0xffd700, title = 'Работа пилотом:', description = f'Вы садитесь в самолёт и проводите ЧЕК перед взлётом...')
		emb.set_footer(text = 'Ожидайте, выполняется ЧЕК')
		await ctx.send(embed = emb)
		time.sleep(2)
		emb = discord.Embed(color = 0xffd700, title = 'Сбоев нет!', description = f'Вы выруливаете на ВПП и ждёте добро на взлёт...')
		emb.set_footer(text = 'Ожидайте добро на взлёт')
		await ctx.send(embed = emb)
		time.sleep(2)
		emb = discord.Embed(color = 0xffd700, title = 'Добро получено!', description = f'Вы взлетаете. Попутного ветра!')
		emb.set_footer(text = 'Ожидайте, полёт начался')
		await ctx.send(embed = emb)
		time.sleep(3)
		emb = discord.Embed(color = 0xffd700, title = 'Посадка!', description = f'Рейс успешно завершён!')
		await ctx.send(embed = emb)

		member = ctx.message.author
		EconomicCogFunctionality.change_balance(
			self.cursor,
			self.conn,
			ctx.message.author,
			ctx.guild,
			balance,
			user_data
		)
		emb = discord.Embed(color = 0xffd700, description = f'{member.mention} получил `{balance}`💸 за работу пилотом!')
		emb.set_footer(text = 'Возобновить данную работу можно через 2 часа!')
		await ctx.send(embed = emb)
#учитель--------------------------------------------------------
	@commands.command(aliases = ['Ручитель', 'ручитель'])
	@commands.cooldown(1, 3600, commands.BucketType.member)
	async def workteacher(self, ctx, balance = 10000):
		member = ctx.message.author

		user_data = EconomicCogFunctionality.get_user_data(
			self.cursor,
			self.conn,
			ctx.message.author,
			ctx.guild
		)
		emb = discord.Embed(color = 0xffd700, title = 'Работа учителем:', description = f'Вы заходите в кабинет директора на планёрку...')
		emb.set_footer(text = 'Ожидайте, идёт планёрка')
		await ctx.send(embed = emb)
		time.sleep(2)
		emb = discord.Embed(color = 0xffd700, title = 'Планёрка проведена!', description = f'Вы идёте в кабинет и ждёте начало урока...')
		emb.set_footer(text = 'Ожидайте, урок скоро начнётся')
		await ctx.send(embed = emb)
		time.sleep(2)
		emb = discord.Embed(color = 0xffd700, title = 'Звонок на урок!', description = f'Дети заходят в класс, начинаются уроки!')
		emb.set_footer(text = 'Ожидайте, урок начался')
		await ctx.send(embed = emb)
		time.sleep(3)
		emb = discord.Embed(color = 0xffd700, title = 'Звонок с урока!', description = f'Все уроки прощли, ваш рабочий день завершён!')
		await ctx.send(embed = emb)

		member = ctx.message.author
		EconomicCogFunctionality.change_balance(
			self.cursor,
			self.conn,
			ctx.message.author,
			ctx.guild,
			balance,
			user_data
		)
		emb = discord.Embed(color = 0xffd700, description = f'{member.mention} получил `{balance}`💸 за работу учителем!')
		emb.set_footer(text = 'Возобновить данную работу можно через 1 час!')
		await ctx.send(embed = emb)

	@commands.command(aliases = ['Передать', 'передать'])
	async def send_gift(self, ctx, member: discord.Member, cash: int):
		"""
		:param ctx:
		:param member:
		:param cash:
		:return:
		"""
		user_data = EconomicCogFunctionality.get_user_data(
			self.cursor,
			self.conn,
			ctx.message.author,
			ctx.guild
		)
		getter_balance = int(
			EconomicCogFunctionality.get_user_data(
				self.cursor,
				self.conn,
				member,
				ctx.guild
			)[3]
		)
		users_balance = int(
			user_data[3]
		)
		if int(cash) > users_balance:
			emb = discord.Embed(colour = discord.Color.red(), description = 'У вас `нет` такой суммы!')
			await ctx.send(embed = emb)
		else:
			self.cursor.execute(
				"UPDATE economic SET wallet_balance = ? WHERE member_id = ? AND guild_id = ?",
				(
					users_balance - int(cash),
					ctx.message.author.id,
					ctx.guild.id
				)
			)
			self.cursor.execute(
				"UPDATE economic SET wallet_balance = ? WHERE member_id = ? AND guild_id = ?",
				(
					getter_balance + int(cash),
					member.id,
					ctx.guild.id
				)
			)
			self.conn.commit()
			author = ctx.message.author
			emb = discord.Embed(color = 0xffd700, description = f'{author.mention}, вы передали {member.mention} `{cash}`💸!')
			await ctx.send(embed = emb)

	@commands.has_permissions(administrator=True)
	@commands.command(aliases = ['Удалбаланс', 'удалбаланс', 'Удалбал', 'удалбал'])
	async def del_bal(self, ctx, member: discord.Member, balance: int):
		"""
		:param ctx:
		:param member:
		:param balance:
		:return:
		"""
		user_data = EconomicCogFunctionality.get_user_data(
			self.cursor,
			self.conn,
			member,
			ctx.guild
		)
		server = ctx.guild
		if user_data[3] < int(balance):
			emb = discord.Embed(colour = discord.Color.red(), description = f'{member.mention} `не имеет` такой суммы!')
			await ctx.send(embed = emb)
		else:
			EconomicCogFunctionality.change_balance(
				self.cursor,
				self.conn,
				member,
				ctx.guild,
				- balance,
				user_data
			)
			emb = discord.Embed(color = 0xffd700, description = f'Успешно удалено `{balance}`💸!')
			await ctx.send(embed = emb)

	@commands.command(aliases = ['Пожертовать', 'пожертвовать'])
	async def fond(self, ctx, balance: int):
		"""
		:param ctx:
		:param balance:
		:return:
		"""
		user_data = EconomicCogFunctionality.get_user_data(
			self.cursor,
			self.conn,
			ctx.message.author,
			ctx.guild
		)
		server = ctx.guild
		if user_data[3] < int(balance):
			emb = discord.Embed(colour = discord.Color.red(), description = 'У вас `нет` такой суммы!')
			await ctx.send(embed = emb)
		else:
			EconomicCogFunctionality.change_balance(
				self.cursor,
				self.conn,
				ctx.message.author,
				ctx.guild,
				- balance,
				user_data
			)
			author = ctx.message.author
			emb = discord.Embed(color = 0xffd700, description = f'{author.mention}, спасибо вам! Вы пожертвовали `{balance}`💸!')
			await ctx.send(embed = emb)

	@commands.has_permissions(administrator=True)
	@commands.command(aliases = ['Добмагаз', 'добмагаз'])
	async def add_shop_item(self, ctx, role: discord.Role, prise: int):
		"""
		:param ctx:
		:param role:
		:param prise:
		:return:
		"""
		self.cursor.execute(
			"INSERT INTO economic_shop_item VALUES(?, ?, ?)",
			(
				ctx.guild.id,
				role.id,
				prise
			)
		)
		self.conn.commit()
		emb = discord.Embed(color = 0xffd700, description = f'{role.mention} успешно добавлена!')
		await ctx.send(embed = emb)

	@commands.has_permissions(administrator=True)
	@commands.command(aliases = ['Удалмагаз', 'удалмагаз'])
	async def del_shop_item(self, ctx, role: discord.Role):
		"""
		:param ctx:
		:param role:
		:return:
		"""
		self.cursor.execute(
			"DELETE FROM economic_shop_item WHERE guild_id = ? AND role_id = ?",
			(
				ctx.guild.id,
				role.id,
			)
		)
		self.conn.commit()
		emb = discord.Embed(color = 0xffd700, description = f'{role.mention} успешно удалена!')
		await ctx.send(embed = emb)

	@commands.command(aliases = ['Магаз', 'магаз', 'Магазин', 'магазин'])
	async def shop(self, ctx):
		prefix = self.get_prefix(self.cursor, ctx.message)
		"""
		:param ctx:
		:return:
		"""
		data = EconomicCogFunctionality.get_all_shop_items(
			self.cursor,
			ctx.guild
		)
		data.reverse()
		emb = discord.Embed(color = 0xffd700, title="Магазин ролей:")
		for item in data:
			emb.add_field(name=f"Роль: `{ctx.guild.get_role(item[1]).name}`", value=f"Цена: `{item[2]}`", inline=False)
			emb.set_footer(text = f'Купить: {prefix}купить @роль')
		await ctx.send(embed = emb)

	@commands.command(aliases = ['Купить', 'купить'])
	async def buy(self, ctx, role: discord.Role):
		"""
		:param ctx:
		:param role:
		:return:
		"""
		data = EconomicCogFunctionality.get_all_shop_items(
			self.cursor,
			ctx.guild
		)
		role_exists = False
		balance = 0
		for item in data:
			if item[1] == role.id:
				role_exists = True
				balance = item[2]
				break
		member = ctx.message.author
		if not role_exists:
			await ctx.send("Такой роли `нет` в магазине!")
		else:
			user_data = EconomicCogFunctionality.get_user_data(self.cursor, self.conn, ctx.message.author, ctx.guild)
			server = ctx.guild
			if user_data[3] < int(balance):
				emb = discord.Embed(colour = discord.Color.red(), description = f'{ctx.message.author.mention} Вы не можете купить роль {role.mention}. У вас нет такой суммы денег!')
				await ctx.send(embed = emb)
			else:
				EconomicCogFunctionality.change_balance(
					self.cursor,
					self.conn,
					member,
					ctx.guild,
					- balance,
					user_data
				)
				await ctx.message.author.add_roles(role)
				emb = discord.Embed(color = 0xffd700, description = f'{ctx.message.author.mention}, вы получили {role.mention}!')
				await ctx.send(embed = emb)

# setup function
def setup(client):
	"""
	:param client:
	:return:
	"""
	client.add_cog(EconomyCog(client))

