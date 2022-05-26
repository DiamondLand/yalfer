import discord
import sqlite3
from discord.ext import commands

class Moderation(commands.Cog):

	def __init__(self, bot):
		self.bot = bot
		self.connection = sqlite3.connect("database.db")
		self.cursor = self.connection.cursor()

	def get_prefix(self, cursor, message):
		cursor.execute(
			"SELECT * FROM prefixes WHERE guild_id = ?", 
			(
				message.guild.id
			)
		)
		result = cursor.fetchone()
		if result is not None:
			return result[1]
		else:
			return "."

	#очистка чата-------------------------------------------
	@commands.command(aliases = ['Очист', 'очист'])
	@commands.has_permissions(administrator = True)
	async def clear(self, ctx, amount = 0):
		await ctx.channel.purge(limit = amount + 1)
		author = ctx.message.author
		if amount <= 0:
			emb = discord.Embed(colour = discord.Color.red(), description  = f'{author.mention}, укажите, `правдивое` число для удаления!')
			await ctx.send(embed = emb)
		else:
			emb = discord.Embed(colour = discord.Color.green(), description  = f':white_check_mark: {author.mention} произвёл очистку чата на `{amount}` сообщений!')
			await ctx.send(embed = emb)
		
	@commands.command(aliases = ['Почист', 'почист'])
	@commands.has_permissions(administrator = True)
	async def clear_member(ctx, member: discord.Member):
		await ctx.channel.purge(limit=None, check=lambda m: m.author==member)
		author = ctx.message.author
		emb = discord.Embed(colour = discord.Color.green(), description  = f':white_check_mark: {author.mention} удалил сообщения от `{member}`!')
		await ctx.send(embed = emb)

	#бан----------------------------------------------------
	@commands.command(aliases = ['Бан', 'бан'])
	@commands.has_permissions(administrator = True)
	async def ban(self, ctx, member: discord.Member, *, reason): 
		await ctx.channel.purge(limit = 1)
		await member.ban(reason = reason)
		emb = discord.Embed(colour = discord.Color.red(), title = 'Бан!', description = f'{member.mention} был `забанен` \nБан выдал: `{ctx.author.display_name}` \nПричина: `{reason}`')
		await ctx.send(embed = emb)
     
	#префикс------------------------------------------------
	@commands.has_permissions(administrator = True)
	@commands.command(aliases = ['Префикс','префикс'])
	async def set_prefix(self, ctx, *, prefix: str):
		author = ctx.message.author
		self.cursor.execute("DELETE FROM prefixes WHERE guild_id = ?", (ctx.guild.id,))
		self.cursor.execute("INSERT INTO prefixes VALUES (?, ?)", (ctx.guild.id, prefix))
		self.connection.commit()
		emb = discord.Embed(colour = discord.Color.red(), description = f'**ЗАМЕНА!** {author.mention} изменил префикс на `{prefix}`')
		await ctx.send(embed = emb)

	#список серверов------------------------------------------------
	@commands.command(aliases = ['Серверлист', 'серверлист'])
	async def guilds(self, ctx):
		emb = discord.Embed(colour = discord.Color.blurple(), title = 'Yalfer используется на:', description = "\n".join(map(str, self.bot.guilds)))
		await ctx.send(embed = emb)

#Cog-----------------------------------------------------
def setup(bot):
   bot.add_cog(Moderation(bot))