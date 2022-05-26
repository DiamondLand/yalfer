import discord
import json
import sqlite3
import requests
from cogs.animals.animals import AnimalsCogFunctionality
from discord.ext import commands

class Animals(commands.Cog):

	def __init__(self, client):
		self.client = client 
		self.connection = sqlite3.connect("database.db")
		self.cursor = self.connection.cursor()

	@commands.command(aliases = ['Лиса', 'лиса', 'Лис', 'лис', 'Лисичка', 'лисичка'])
	async def fox(self, ctx):
		await ctx.channel.purge(limit=1)
		link = AnimalsCogFunctionality.get_animal_image_url("fox")
		await AnimalsCogFunctionality.send_animal_image_embed(self.cursor, ctx, link, "Лисичка:")

	@commands.command(aliases = ['Пёс', 'пёс', 'Пес', 'пес', 'Собака', 'собака', 'Собакен', 'собакен'])
	async def dog(self, ctx):
		await ctx.channel.purge(limit=1)
		link = AnimalsCogFunctionality.get_animal_image_url("dog")
		await AnimalsCogFunctionality.send_animal_image_embed(self.cursor, ctx, link, "Собакен:")

	@commands.command(aliases = ['Кот', 'кот', 'Кошка', 'кошка', 'Кошак', 'кошак'])
	async def cat(self, ctx):
		await ctx.channel.purge(limit=1)
		link = AnimalsCogFunctionality.get_animal_image_url("cat")
		await AnimalsCogFunctionality.send_animal_image_embed(self.cursor, ctx, link, "Кошак:")

def setup(client):
	client.add_cog(Animals(client))