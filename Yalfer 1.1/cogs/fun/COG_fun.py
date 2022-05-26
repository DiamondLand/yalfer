from math import degrees
import discord
import random
import os
from discord.enums import _is_descriptor
import youtube_dl
import asyncio
import datetime
import bs4

from discord.ext import commands
from bs4 import BeautifulSoup
from random import randint

class Fun(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	#утро----------------------------------------------------
	@commands.command(aliases = ['Утро', 'утро'])
	async def morning(self, ctx): 
		author = ctx.message.author
		await ctx.channel.purge(limit = 1)
		emb = discord.Embed(colour = discord.Color.gold(), description = f'{author.mention}, поздравляю с началом нового, прекрасного дня.\nДостигни своих целей!:blueberries:')
		await ctx.send(embed = emb)
		
	#ночь---------------------------------------------------
	@commands.command(aliases = ['Ночь', 'ночь'])
	async def night(self, ctx):
		author = ctx.message.author
		await ctx.channel.purge(limit = 1)
		emb = discord.Embed(colour = discord.Color.gold(), description = f'Желаю таких же сладких снов, как синнабона, дорогой {author.mention} :tea:')
		await ctx.send(embed = emb)

	#личка--------------------------------------------------
	@commands.command(aliases = ['Личка', 'личка'])
	async def personal(self, ctx, member: discord.Member, *, text):
		await ctx.channel.purge(limit = 1)
		author = ctx.message.author
		emb = discord.Embed(colour = discord.Color.gold(), description = f'{author.mention} передал тебе: **{text}**')
		await member.send(embed = emb)
		emb = discord.Embed(colour = discord.Color.green(), description = f':white_check_mark: {author.mention}, `личное сообщение` доставлено!')
		await ctx.send(embed = emb)

	#судьба------------------------------------------------
	@commands.command(aliases = ['Судьба', 'судьба'])
	async def fate(self, ctx, *, text):
		variable = ['Конечно! :comet: ', 'Ты что? **НЕТ**! :no_entry_sign: ', 'Возможно... :four_leaf_clover: ', 'Ни за что! :o: ', 'Естественно! :sparkles: ', 'Да, да, да! :ringed_planet: ']
		await ctx.send('{}'.format(random.choice(variable)))

	#орёл или решка----------------------------------------
	@commands.command(aliases = ['Орёл', 'орёл', 'орел', 'Орел'])
	async def eagle(self, ctx):
		variable = ['Выпала `решка`. Проигрыш! :stuck_out_tongue:', 'Выпал `орёл`. Победа! :tada:']
		await ctx.send('{}'.format(random.choice(variable)))

	@commands.command(aliases = ['Решка', 'решка'])
	async def tails(self, ctx):
		variable = ['Выпал `орёл`. Проигрыш! :stuck_out_tongue:', 'Выпала `решка`. Победа! :tada:']
		await ctx.send('{}'.format(random.choice(variable)))

	#ковид-------------------------------------------------
	@commands.command(aliases = ['Дуэль', 'дуэль', 'Дуель', 'дуель'])
	async def duel(self, ctx, member: discord.Member = None):
		if member is None:
			await ctx.send('Вы не указали @Участника, которого хотели позвать на дуэль!')
		else:
			a = random.randint(1,2)
			if a == 1:
				emb = discord.Embed(colour = discord.Color.gold(), description = f"Победитель - `{ctx.author}`\nПроигравший - `{member}`")
				await ctx.send(embed = emb)
			else:
				emb = discord.Embed(colour = discord.Color.gold(), description = f"Победитель - `{member}`\nПроигравший - `{ctx.author}`")
				await ctx.send(embed = emb)
	

	#дата--------------------------------------------------
	@commands.command(aliases = ['Дата', 'дата'])
	async def date(self, ctx):
		dt = datetime.datetime.now()
		day = str(dt).split(" ")[0]
		time = str(dt).split(" ")[1].split(".")[0]
		emb = discord.Embed(colour = discord.Color.gold(), title="Дата", description=day)
		emb.add_field(name="Время [МСК]", value=time, inline=False)
		await ctx.send(embed=emb)

#Cog-----------------------------------------------------
def setup(bot):
   bot.add_cog(Fun(bot))