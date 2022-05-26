import discord
import os
import asyncio
import youtube_dl
from discord.ext import commands
from youtube_search import YoutubeSearch
from discord import utils


class music(commands.Cog):

	def __init__(self, client):
		self.client = client

	@commands.command(aliases = ['Плэй', 'плэй', 'Плей', 'плей'])
	async def play(self, ctx, *url_words):
		url = " ".join(url_words)
		try:
			voice = discord.utils.get(
			self.client.voice_clients,
				guild=ctx.guild
			)
			voice.stop()
		except:
			pass
		FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
		ydl_opts = {'format': 'bestaudio'}
		with youtube_dl.YoutubeDL(ydl_opts) as ydl:
			try:
				info = ydl.extract_info(url, download=False)
			except:
				to_search = url
				results = YoutubeSearch(to_search, max_results=1).to_dict()
				NEW_URL = ("https://youtube.com" + results[0]["url_suffix"])
				info = ydl.extract_info(NEW_URL, download = False)
				emb = discord.Embed(colour = discord.Color.blurple(), title = 'Проигрывание...', url = f'{NEW_URL}')
				emb.set_footer(text = 'Рекомендуемая громкость: 80%')
				await ctx.send(embed = emb)
			URL = info['formats'][0]['url']
		voiceChannel = ctx.message.author.voice.channel
		try:
			await voiceChannel.connect()
		except:
			pass
		voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
		voice.play(discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))

	@commands.command(aliases = ['Стоп', 'стоп', 'Выйти', 'выйти'])
	async def stop(self, ctx):
		voice_client = ctx.guild.voice_client
		if voice_client:
			await voice_client.disconnect()
			emb = discord.Embed(colour = discord.Color.green(), description = ':white_check_mark: Бот отключился!')
			await ctx.send(embed = emb)
		else:
			await ctx.send("Бот не находится в голосовом канале")

	@commands.command(aliases = ['Пауза', 'пауза'])
	async def pause(self, ctx):
		voice = discord.utils.get(
			self.client.voice_clients,
			guild=ctx.guild
		)
		if voice.is_playing():
			voice.pause()
			emb = discord.Embed(colour = discord.Color.blurple(), description = 'Пауза...')
			await ctx.send(embed = emb)
		else:
			emb = discord.Embed(colour = discord.Color.red(), description = 'Сейчас нет активных песен!')
			await ctx.send(embed = emb)

	@commands.command(aliases = ['Продолжить', 'продолжить'])
	async def resume(self, ctx):
		voice = discord.utils.get(
			self.client.voice_clients,
			guild=ctx.guild
		)
		if voice.is_paused():
			voice.resume()
			emb = discord.Embed(colour = discord.Color.blurple(), description = 'Продолжаю...')
			await ctx.send(embed = emb)
		else:
			emb = discord.Embed(colour = discord.Color.red(), description = 'Сейчас нет песен на паузе!')
			await ctx.send(embed = emb)


def setup(client):
	client.add_cog(music(client))