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

	@commands.command(aliases = ['Лиса', 'лиса', 'Лис', 'лис'])
	async def fox(self, ctx):
	    link = AnimalsCogFunctionality.get_animal_image_url("fox")
	    await AnimalsCogFunctionality.send_animal_image_embed(self.cursor, ctx, link, "Лиса:")

	@commands.command(aliases = ['Пёс', 'пёс', 'Пес', 'пес', 'Собака', 'собака'])
	async def dog(self, ctx):
	    link = AnimalsCogFunctionality.get_animal_image_url("dog")
	    await AnimalsCogFunctionality.send_animal_image_embed(self.cursor, ctx, link, "Собака:")

	@commands.command(aliases = ['Кот', 'кот', 'Кошка', 'кошка'])
	async def cat(self, ctx):
	    link = AnimalsCogFunctionality.get_animal_image_url("cat")
	    await AnimalsCogFunctionality.send_animal_image_embed(self.cursor, ctx, link, "Кошка:")

def setup(client):
	client.add_cog(Animals(client))