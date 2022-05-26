import discord
import random
import os
import asyncio
import sqlite3
from config import config
from discord.ext import commands
from bs4 import BeautifulSoup
from discord import player
from random import randint
from re import X
from io import BytesIO

class Fun(commands.Cog):
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

	#судьба------------------------------------------------
	@commands.command(aliases = ['Судьба', 'судьба'])
	@commands.cooldown(2, 100, commands.BucketType.member)
	async def fate(self, ctx, *, text):
		variable = ['Даааа! :innocent:', 'Ага щас :face_with_monocle: ', '100%', 'Нет и ещё раз нет! :no_entry_sign: ', 'Ты что?\nНЕТ! :four_leaf_clover: ', 'Не хочу тебя огорчать... :eyes: ', 'Как бы сказать помягче...\n||ДА!|| :heart_eyes:', 'Скорее нет, чем да :wave:', 'Маловероятно :moyai: ', 'Может быть :gem: ', 'Так и будет :heart_on_fire: ', 'А зачем это тебе?  :eggplant: ' ]
		emb = discord.Embed(color=config.EMBED_COLOR, description = '{}'.format(random.choice(variable)))
		await ctx.reply(embed=emb, mention_author=False)

	#орёл или решка----------------------------------------
	@commands.command(aliases=['Монетка', 'монетка', 'Монета', 'монета'])
	async def cointoss(self, ctx):
		choice = random.randint(1, 2)
		
		if choice == 1:
			await ctx.reply('Великолепная `решка` проглядывается на монетке!', mention_author=False)
		
		if choice == 2:
			await ctx.reply('Могучий `орёл` проглядывается на монетке!', mention_author=False)

	#дуэль-------------------------------------------------
	@commands.command(aliases = ['Дуэль', 'дуэль', 'Дуель', 'дуель'])
	async def duel(self, ctx, member: discord.Member = None):
		if member == ctx.author:
			return await ctx.send(embed=discord.Embed(title="Хмммм...", description="Играть самим с собой не получится!", colour=config.EMBED_COLOR,))
		if member:
			variable = [f'`{member}` был застрелен... :boom:\n\n`{ctx.author}` остался в живых! :four_leaf_clover: ', f'`{ctx.author}` был застрелен... :boom:\n`{member}` остался в живых! :four_leaf_clover: ']
			emb = discord.Embed(color=config.EMBED_COLOR, description = '{}'.format(random.choice(variable)))
			await ctx.send(embed = emb)

	#респект-------------------------------------------------
	@commands.command(aliases = ['Ф', 'ф', 'Респект', 'респект', 'Риспект', 'риспект'])
	async def f(self, ctx, *, text = None):
		await ctx.channel.purge(limit = 1)
		hearts = ["❤", "💛", "💚", "💙", "💜"]
		reason = f"{text} " if text else""
		emb = discord.Embed(color=config.EMBED_COLOR, description = f"{ctx.author.mention} респектнул {reason}{random.choice(hearts)}")
		await ctx.send(embed=emb)

	#краш-------------------------------------------------
	@commands.command(aliases=["Краш", "краш"])
	async def hotcalc(self, ctx, *, user: discord.Member = None):
		await ctx.channel.purge(limit = 1)
		user = user or ctx.author

		r = random.randint(1, 100)
		hot = r / 1.17

		if hot > 70:
			emoji = "💞"
		elif hot > 50:
			emoji = "💖"
		elif hot > 25:
			emoji = "❤"
		else:
			emoji = "💔"

		emb = discord.Embed(color=config.EMBED_COLOR, description = f"{user.mention} краш на `{hot:.2f}`% {emoji}!")
		await ctx.send(embed=emb)

			

#Cog-----------------------------------------------------
def setup(bot):
   bot.add_cog(Fun(bot))