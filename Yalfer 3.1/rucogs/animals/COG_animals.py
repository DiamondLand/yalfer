import discord
import json
import sqlite3
import requests
from rucogs.animals.animals import AnimalsCogFunctionality
from discord.ext import commands

class Animals(commands.Cog):

    def __init__(self, client):
        self.client = client 
        self.connection = sqlite3.connect("database.db")
        self.cursor = self.connection.cursor()

    @commands.command(aliases = ['Панда', 'панда'])
    async def panda(self, ctx):
        link = AnimalsCogFunctionality.get_animal_image_url("panda")
        await AnimalsCogFunctionality.send_animal_image(self.cursor, ctx, link, "Панда")

    @commands.command(aliases = ['Птица', 'птица', 'Птичка', 'птичка'])
    async def bird(self, ctx):
        link = AnimalsCogFunctionality.get_animal_image_url("bird")
        await AnimalsCogFunctionality.send_animal_image(self.cursor, ctx, link, "Птичка")

    @commands.command(aliases = ['Енот', 'енот'])
    async def raccoon(self, ctx):
        link = AnimalsCogFunctionality.get_animal_image_url("raccoon")
        await AnimalsCogFunctionality.send_animal_image(self.cursor, ctx, link, "Енот")

def setup(client):
    client.add_cog(Animals(client))