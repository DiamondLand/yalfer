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
            return "+"
    #очистка чата-----------------------------------------
    @commands.has_permissions(administrator=True)
    @commands.command(aliases = ['Почист', 'почист'])
    async def clear(self, ctx, limit: int):
        """
        :param ctx:
        :param limit:
        :return:
        """
        await ctx.channel.purge(limit=limit + 1)
        emb = discord.Embed(color = 0xffd700, description = f'`{ctx.author.display_name}` произвёл очистку чата! (`{limit}`)')
        await ctx.send(embed = emb, delete_after=5)

    @commands.has_permissions(administrator=True)
    @commands.command(aliases = ['Очист', 'очист'])
    async def clear_all(self, ctx):
        """
        :param ctx:
        :return:
        """
        await ctx.channel.purge()
        emb = discord.Embed(color = 0xffd700, description = f'`{ctx.author.display_name}` произвёл очистку чата! (`всё`)')
        await ctx.send(embed = emb, delete_after=5)

    #добавит роли------------------------------------------
    @commands.has_permissions(administrator=True)
    @commands.command(aliases = ['Доброль', 'доброль'])
    async def addrole(self, ctx, member: discord.Member, role: discord.Role):
        """
        :param ctx:
        :param member:
        :param role:
        :return:
        """
        await member.add_roles(role)
        emb = discord.Embed(color = 0xffd700, description = f'`{ctx.author.display_name}` выдал `{role}` {member.mention}!')
        await ctx.send(embed = emb)

    @commands.has_permissions(administrator=True)
    @commands.command(aliases = ['Удалроль', 'удалроль'])
    async def removerole(self, ctx, member: discord.Member, role: discord.Role):
        """
        :param ctx:
        :param member:
        :param role:
        :return:
        """
        await member.remove_roles(role)
        emb = discord.Embed(colour = discord.Color.green(), description = f'`{ctx.author.display_name}` забрал `{role}` у {member.mention}!')
        await ctx.send(embed = emb)
        
    #кик----------------------------------------------------
    @commands.command(aliases = ['Кик', 'кик'])
    @commands.has_permissions(administrator = True)
    async def kick(self, ctx, member: discord.Member, *, reason): 
       await member.kick(reason = reason)
       emb = discord.Embed(color = 0xffd700, title = 'Кик!', description = f'{member.mention} был `кикнут` \nКик выдал: `{ctx.author.display_name}` \nПричина: `{reason}`')
       await ctx.send(embed = emb)

    #бан----------------------------------------------------
    @commands.command(aliases = ['Бан', 'бан'])
    @commands.has_permissions(administrator = True)
    async def ban(self, ctx, member: discord.Member, *, reason): 
        await member.ban(reason = reason)
        emb = discord.Embed(color = 0xffd700, title = 'Бан!', description = f'{member.mention} был `забанен` \nБан выдал: `{ctx.author.display_name}` \nПричина: `{reason}`')
        await ctx.send(embed = emb)

    #мут----------------------------------------------------
    @commands.command(aliases = ['Мут', 'мут', 'Мьют', 'мьют'])
    @commands.has_permissions(administrator = True)
    async def mute(self, ctx, member: discord.Member, *, reason):
        await ctx.send('Выполнянется обработка...', delete_after=6)
        guild = ctx.guild
        mutedRole = discord.utils.get(guild.roles, name = 'Мут by Yalfer')
        if not mutedRole:
            mutedRole = await guild.create_role(name = 'Мут by Yalfer')
        for channel in guild.channels:
            await channel.set_permissions(mutedRole, speak = False, send_messages = False)
        await member.add_roles(mutedRole, reason = reason)
        emb = discord.Embed(color = 0xffd700, title = 'Мут!', description = f'{member.mention} был `замьючен` \nМут выдал: `{ctx.author.display_name}` \nПричина: `{reason}`')
        await ctx.send(embed = emb)

    #размут-------------------------------------------------
    @commands.command(aliases = ['Размут', 'размут', 'Размьют', 'размьют'])
    @commands.has_permissions(administrator = True)
    async def unmute(self, ctx, member: discord.Member):
        mutedRole = discord.utils.get(ctx.guild.roles, name = 'Мут by Yalfer')
        await member.remove_roles(mutedRole)
        emb = discord.Embed(color = 0xffd700, title = 'Размут!', description = f'{member.mention} был `размьючен` \nМут снял: `{ctx.author.display_name}`')
        await ctx.send(embed = emb)
    #префикс------------------------------------------------
    @commands.has_permissions(administrator = True)
    @commands.command(aliases = ['Префикс','префикс'])
    async def set_prefix(self, ctx, *, prefix: str):
        author = ctx.message.author
        self.cursor.execute("DELETE FROM prefixes WHERE guild_id = ?", (ctx.guild.id,))
        self.cursor.execute("INSERT INTO prefixes VALUES (?, ?)", (ctx.guild.id, prefix))
        self.connection.commit()
        emb = discord.Embed(color = 0xffd700, title = 'Префикс!', description = f'{author.mention} изменил префикс на `{prefix}`')
        await ctx.send(embed = emb)

    #список серверов---------------------------------------
    @commands.command(aliases = ['Серверлист', 'серверлист'])
    async def guilds(self, ctx):
        emb = discord.Embed(color = 0xffd700, title = 'Yalfer используется на:', description = "\n".join(map(str, self.bot.guilds)))
        await ctx.send(embed = emb)
    
#Cog-----------------------------------------------------
def setup(bot):
   bot.add_cog(Moderation(bot))