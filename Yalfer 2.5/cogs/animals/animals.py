import discord
import json
import requests
import discord
from config import config

class AnimalsCogFunctionality:

	@staticmethod
	def get_animal_image_url(animal_name: str):
		response = requests.get(f'https://some-random-api.ml/img/{animal_name}')
		json_data = json.loads(response.text)
		return json_data['link']

	@staticmethod
	async def send_animal_image_embed(cursor, ctx, link, animal):
		embed = discord.Embed(color = config.EMBED_COLOR, description = 
            f"{animal.title()}", 
        )
		embed.set_image(url = link)
		await ctx.send(embed = embed)