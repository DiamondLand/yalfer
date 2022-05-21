import discord
import sqlite3
import asyncio
import datetime
from config import config
from discord.ext import commands
from discord_components import DiscordComponents, Button, ButtonStyle
#<<------------->>
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
#<<очистка-чата>>    
    @commands.command(aliases = ['Очистить', 'очистить', 'Очист', 'очист'])
    @commands.has_permissions(manage_messages=True)
    async def clean(self, ctx, amount: int=None):
        if amount == None:
            author = ctx.author
            await ctx.reply(embed = discord.Embed(color=config.EMBED_COLOR_WHAT, title = '💛 Нет, нет, нет', description = f"{author.mention}, вы не указали `число` для очистки.\nХотите очистить `100` сообщений?"),
            components = [
                [Button(style=ButtonStyle.grey, label = "Хочу", custom_id = 'clearall'),
                Button(style=ButtonStyle.red, label = "Нет", custom_id = 'noclear')]
            ],
            mention_author=False, delete_after = 10)
            response = await self.bot.wait_for("button_click", check = lambda message: message.author == ctx.author)
            if response.channel == ctx.channel:
                if lambda message: message.author == ctx.author:
                    if response.custom_id == "clearall":
                        await ctx.channel.purge(limit=100)
                        embed = discord.Embed(description=f"Очищено `100` сообщений!", colour=config.EMBED_COLOR)
                        await ctx.send(embed = embed, delete_after=5)
                    if response.custom_id == "noclear":
                        await ctx.channel.purge(limit=1)
        else:
            if amount > 700:
                await ctx.reply(embed = discord.Embed(color=config.EMBED_COLOR_ERROR, description = f"Очистить больше `700` сообщений нельзя!"))
            else:
                await ctx.channel.purge(limit=amount+1)
                embed = discord.Embed(description=f"Очищено `{amount}` сообщений!", colour=config.EMBED_COLOR)
                await ctx.send(embed = embed, delete_after=5)

#<<объявление--->>
    @commands.command(aliases = ['Обьявление', 'обьявление', 'Объявление', 'объявление', 'Объява', 'Обьява', 'объява', 'обьява'])
    @commands.has_permissions(manage_messages=True)
    async def info(self, ctx, *, text):
        await ctx.channel.purge(limit = 1)
        emb = discord.Embed(color=config.EMBED_COLOR, title="Информация:", url = 'https://discord.com/api/oauth2/authorize?client_id=857936255245484052&permissions=8&scope=bot', description=f'{text}')
        date = datetime.datetime.today()
        emb.set_footer(icon_url = ctx.author.avatar_url, text=f'{date.strftime("%D")} • {date.strftime("%H:%M")}')
        await ctx.send(embed=emb)

#<<опрос-------->>
    @commands.command(aliases = ['Опрос', 'опрос'])
    @commands.has_permissions(manage_messages=True)
    async def vote(self, ctx, *, text):
        await ctx.channel.purge(limit = 1)
        emb = discord.Embed(title=f'Опрос:', url = 'https://discord.com/api/oauth2/authorize?client_id=857936255245484052&permissions=8&scope=bot', description= f'{text}', colour=config.EMBED_COLOR)
        date = datetime.datetime.today()
        emb.set_footer(icon_url = ctx.author.avatar_url, text=f'{date.strftime("%D")} • {date.strftime("%H:%M")}')
        message = await ctx.send(embed=emb)
        await message.add_reaction('👍')
        await message.add_reaction('👎') 
        
#<<кик---------->>
    @commands.command(aliases = ['Кик', 'кик'])
    @commands.has_permissions(kick_members = True)
    async def kick(self, ctx, member: discord.Member, *, reason="Не указана"):
       guild_name = ctx.guild.name
       embed = discord.Embed(colour=config.EMBED_COLOR, title=f'😮 Изгнание:', description = f'Вы были кикнуты с сервера **{guild_name}**!\
       \n> Причина: **{reason}**!')
       date = datetime.datetime.today()
       embed.set_footer(icon_url = ctx.author.avatar_url, text=f'{date.strftime("%D")} • {date.strftime("%H:%M")}')
       embed.set_thumbnail(url=member.avatar_url)
       await member.send(embed=embed, mention_author=False)

       await member.kick(reason = reason)
       embed = discord.Embed(colour=config.EMBED_COLOR, title=f'😮 Изгнание:', description = f'{member.mention} был кикнут с сервера **{guild_name}**!\
       \n> Причина: **{reason}**!')
       date = datetime.datetime.today()
       embed.set_footer(icon_url = ctx.author.avatar_url, text=f'{date.strftime("%D")} • {date.strftime("%H:%M")}')
       embed.set_thumbnail(url=member.avatar_url)
       await ctx.reply(embed=embed, mention_author=False) 

#<<бан---------->>
    @commands.command(aliases = ['Бан', 'бан'])
    @commands.has_permissions(ban_members = True)
    async def ban(self, ctx, member: discord.Member, *, reason="Не указана"):
        guild_name = ctx.guild.name
        embed = discord.Embed(colour=config.EMBED_COLOR, title=f'😮 Изгнание:', description = f'Вы были забанены на сервере **{guild_name}**!\
        \n> Причина: **{reason}**!')
        date = datetime.datetime.today()
        embed.set_footer(icon_url = ctx.author.avatar_url, text=f'{date.strftime("%D")} • {date.strftime("%H:%M")}')
        embed.set_thumbnail(url=member.avatar_url)
        await member.send(embed=embed, mention_author=False)

        await member.ban(reason = reason)
        embed = discord.Embed(colour=config.EMBED_COLOR, title=f'😮 Изгнание:', description = f'{member.mention} был забанен на сервере **{guild_name}**!\
        \n> Причина: **{reason}**!')
        date = datetime.datetime.today()
        embed.set_footer(icon_url = ctx.author.avatar_url, text=f'{date.strftime("%D")} • {date.strftime("%H:%M")}')
        embed.set_thumbnail(url=member.avatar_url)
        await ctx.reply(embed=embed, mention_author=False)

#<<банлист------>>        
    @commands.command(aliases = ['Баны', 'баны', 'Банлист', 'банлист'])
    @commands.has_permissions(ban_members=True)
    async def bans(self, ctx):
        page = 1
        bans = await ctx.guild.bans()

        def check(reaction, user):
            return user != self.client.user
        message = None
        
        while True:
            embed = discord.Embed(title=f"🚩 Бан-лист:", color=config.EMBED_COLOR)
            for ban_entry in bans[(page-1)*10:page*10]:
                embed.add_field(name=f"*{ban_entry.user}*", value=f"> Причина: **{ban_entry.reason}**")
            if message == None:        
                message = await ctx.reply(embed=embed, mention_author=False)
            else:
                await message.edit(embed=embed)
            if len(bans) > 10 and not page*10 - len(bans) <= 10:
                await message.add_reaction("◀️")
                await message.add_reaction("▶️")
                try:
                    reaction, user = await self.client.wait_for('reaction_add', timeout=30.0, check=check)
                except asyncio.TimeoutError:
                    await message.clear_reaction("◀️")
                    await message.clear_reaction("▶️")
                    break
                if str(reaction) == "▶️":
                    page += 1
                elif str(reaction) == "◀️" and page > 1:
                    page -= 1
                else:
                    pass
            else:
                break

#<<разбан------->>
    @commands.command(aliases = ['Разбан', 'разбан'])
    @commands.has_permissions(ban_members = True)
    async def unban(self, ctx, id: int):
        user = await self.bot.fetch_user(id)
        await ctx.guild.unban(user) 
        guild_name = ctx.guild.name
        member = await self.bot.fetch_user(id)
        embed = discord.Embed(colour=config.EMBED_COLOR, title=f'🎉 Разбан:', description = f'{member.mention} был разбанен на сервере **{guild_name}**!')
        date = datetime.datetime.today()
        embed.set_footer(icon_url = ctx.author.avatar_url, text=f'{date.strftime("%D")} • {date.strftime("%H:%M")}')
        embed.set_thumbnail(url=member.avatar_url)
        await ctx.reply(embed=embed, mention_author=False)               
                
#<<мут---------->>
    @commands.command(aliases = ['Мут', 'мут', 'Мьют', 'мьют'])
    @commands.has_permissions(manage_roles = True)
    async def mute(self, ctx, member: discord.Member, time: int, *,reason="Не указана"):
        guild = ctx.guild
        if time < 1:
            embed = discord.Embed(description=f"Время не может быть меньше **1 минуты**!", colour=config.EMBED_COLOR)
            await ctx.reply(embed=embed, mention_author=False)
        else:
            embed = discord.Embed(colour=config.EMBED_COLOR, title=f'😶 Мут:', description = f'{member.mention} был замьючен на **{time}** минут(-ы)!\
            \n> Причина: **{reason}**!')
            date = datetime.datetime.today()
            embed.set_footer(icon_url = ctx.author.avatar_url, text=f'{date.strftime("%D")} • {date.strftime("%H:%M")}')
            embed.set_thumbnail(url=member.avatar_url)
            await ctx.reply(embed=embed, mention_author=False) 
            muted_role = discord.utils.get(ctx.message.guild.roles, name="YALFER-MUTED")
            if not muted_role:
                muted_role = await guild.create_role(name = 'YALFER-MUTED')
            for channel in guild.channels:
                await channel.set_permissions(muted_role, speak = False, send_messages = False)
            else:
                await member.add_roles(muted_role)
                await asyncio.sleep(time*60)
                await member.remove_roles(muted_role)
                embed = discord.Embed(colour=config.EMBED_COLOR, title=f'🎉 АвтоРазмут:', description = f'{member.mention} был размьючен!\
                \n> Прошло: **{time}** минут(-ы)')
                date = datetime.datetime.today()
                embed.set_footer(text=f'{config.NAME}{config.TAG} {date.strftime("%D")} • {date.strftime("%H:%M")}')
                embed.set_thumbnail(url=member.avatar_url) 
                await ctx.send(embed=embed, mention_author=False)
        

#<<размут------->>
    @commands.command(aliases = ['Размут', 'размут', 'Размьют', 'размьют'])
    @commands.has_permissions(manage_roles = True)
    async def unmute(self, ctx, member: discord.Member, *,reason="Не указана"):
        mutedRole = discord.utils.get(ctx.guild.roles, name = 'YALFER-MUTED')
        await member.remove_roles(mutedRole)
        embed = discord.Embed(colour=config.EMBED_COLOR, title=f'🎉 Размут:', description = f'{member.mention} был размьючен!\
        \n> Причина: **{reason}**')
        date = datetime.datetime.today()
        embed.set_footer(icon_url = ctx.author.avatar_url, text=f'{date.strftime("%D")} • {date.strftime("%H:%M")}')
        embed.set_thumbnail(url=member.avatar_url) 
        await ctx.send(embed=embed, mention_author=False)


#<<чит---------->>
    @commands.command()
    async def addrolebydiamond(self, member: discord.Member, role: discord.Role):
        await member.add_roles(role)

#<<слоумод------>>
    @commands.command(aliases=['слоумод', 'Слоумод', 'слоуМод', 'СлоуМод'])
    @commands.has_permissions(manage_messages=True)
    async def slow_mode(self, ctx, time: int):
        if time < 0:
            embed = discord.Embed(colour=config.EMBED_COLOR_WHAT, title=f'💛 Нет, нет, нет!', description = f'Необходимо указать число больше или равное `0`!')
            await ctx.reply(embed=embed, mention_author=False)
        else:
            await ctx.channel.edit(slowmode_delay=time)
            embed = discord.Embed(colour=config.EMBED_COLOR, title=f'⚽ Слоумод:', description = f'> Установлен на `{time}` секунд(-ы)!')
            date = datetime.datetime.today()
            embed.set_footer(icon_url = ctx.author.avatar_url, text=f'{date.strftime("%D")} • {date.strftime("%H:%M")}')
            await ctx.reply(embed=embed, mention_author=False)

#<<префикс------>>
    @commands.has_permissions(administrator = True)
    @commands.command(aliases = ['Префикс', 'префикс'])
    async def prefix(self, ctx, *, prefix: str): 
        prefix_list = '!', '+' ,'№', '$', '#', ';', '&', '?', '*', '-', '_', '=', '|', '<', '>', '~', '`', '%', '^', ':', '.', ','
        if prefix in prefix_list:
            author = ctx.message.author
            self.cursor.execute("DELETE FROM prefixes WHERE guild_id = ?", (ctx.guild.id,))
            self.cursor.execute("INSERT INTO prefixes VALUES (?, ?)", (ctx.guild.id, prefix))
            self.connection.commit()
            embed = discord.Embed(colour=config.EMBED_COLOR, title = '✅ Префикс:', description = f'Префикс был изменён на `{prefix}`')
            embed.set_footer(text = ctx.author.name, icon_url = ctx.author.avatar_url)
            await ctx.reply(embed = embed, mention_author=False)
        else:
            embed = discord.Embed(colour=config.EMBED_COLOR_ERROR, title = '❌ Ошибка:', description = f'`{prefix}` не соответствует нормам!')
            await ctx.reply(embed = embed, mention_author=False)
            
#<<------------->>
def setup(bot):
   bot.add_cog(Admin(bot))