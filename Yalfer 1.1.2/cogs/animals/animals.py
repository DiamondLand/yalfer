import discord
import json
import requests
import discord
import send_translated_msg

class AnimalsCogFunctionality:

	@staticmethod
	def get_animal_image_url(animal_name: str):
		""" Эта функция возвращает ссылку на картинку
		с животным animal_name отдавая запрос в some-random-api.ml
		"""
		response = requests.get(f'https://some-random-api.ml/img/{animal_name}')
		json_data = json.loads(response.text)
		return json_data['link']

	@staticmethod
	async def send_animal_image_embed(cursor, ctx, link, animal):
		""" Эта функция отправляет в текстовый канал в discord-е
		embed с изображением животного
		"""
		embed = discord.Embed(color = discord.Color.gold(), title = 
            f"{animal.title()}", 
        )
		embed.set_image(url = link)
		await ctx.send(embed = embed)