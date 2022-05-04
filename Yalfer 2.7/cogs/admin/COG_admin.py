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
    @commands.command(aliases = ['Очистить', 'очистить', 'Очист'])
    @commands.has_permissions(manage_messages=True)
    async def очист(self, ctx, amount: int=None):
        if amount == None:
            author = ctx.author
            await ctx.reply(embed = discord.Embed(color=config.EMBED_COLOR, description = f"{author.mention}, вы не указали `число` для очистки.\nХотите очистить `100` сообщений?"),
            components = [
                [Button(style=ButtonStyle.green, label = "Хочу", custom_id = 'clearall'),
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
    @commands.command(aliases = ['Обьявление', 'обьявление', 'Объявление', 'объявление', 'Объява', 'Обьява', 'обьява'])
    @commands.has_permissions(manage_messages=True)
    async def объява(self, ctx, *, text):
        await ctx.channel.purge(limit = 1)
        emb = discord.Embed(color=config.EMBED_COLOR, title="Информация:", url = 'https://discord.com/api/oauth2/authorize?client_id=857936255245484052&permissions=8&scope=bot', description=f'{text}')
        emb.set_footer(text = ctx.author.name, icon_url = ctx.author.avatar_url)
        await ctx.send(embed=emb)

#<<опрос-------->>
    @commands.command(aliases = ['Опрос'])
    @commands.has_permissions(manage_messages=True)
    async def опрос(self, ctx, *, text):
        await ctx.channel.purge(limit = 1)
        emb = discord.Embed(title=f'Опрос:', url = 'https://discord.com/api/oauth2/authorize?client_id=857936255245484052&permissions=8&scope=bot', description= f'{text}', colour=config.EMBED_COLOR)
        emb.set_footer(text = ctx.author.name, icon_url = ctx.author.avatar_url)
        message = await ctx.send(embed=emb)
        await message.add_reaction('👍')
        await message.add_reaction('👎')

#<<роль--------->>
    @commands.command(aliases = ['Роль'])
    @commands.has_permissions(manage_roles=True)
    async def роль(self, ctx, member: discord.Member, role: discord.Role):
        await member.add_roles(role)
        embed = discord.Embed(colour=config.EMBED_COLOR, title=f'Изменение у {member}:', description = f'💚 Получена роль - {role.mention}')
        embed.set_footer(text=f'Выдал: {ctx.author}') 
        await ctx.reply(embed=embed, mention_author=False) 

#<<удалить-роль->>
    @commands.command(aliases = ['Удроль'])
    @commands.has_permissions(manage_roles=True)
    async def удроль(self, ctx, member: discord.Member, role: discord.Role):
        await member.remove_roles(role)
        embed = discord.Embed(colour=config.EMBED_COLOR, title=f'Изменение у {member}:', description = f'💔 Изъята роль - {role.mention}')
        embed.set_footer(text=f'Изъял: {ctx.author}') 
        await ctx.reply(embed=embed, mention_author=False) 
        
#<<кик---------->>
    @commands.command(aliases = ['Кик'])
    @commands.has_permissions(kick_members = True)
    async def кик(self, ctx, member: discord.Member, *, reason=None): 
       await member.kick(reason = reason)
       embed = discord.Embed(colour=config.EMBED_COLOR, description = f'{member.mention} был кикнут по причине: `{reason}`')
       await ctx.reply(embed = embed)

#<<бан---------->>
    @commands.command(aliases = ['Бан'])
    @commands.has_permissions(ban_members = True)
    async def бан(self, ctx, member: discord.Member, *, reason=None):
        author = ctx.message.author
        await ctx.reply(embed = discord.Embed(color=config.EMBED_COLOR, description = f"{author.mention}, Вы уверены в своём решении?\nПоследствия могут быть необратимы!"),
        components = [
            [Button(style=ButtonStyle.green, label = "Банить", custom_id = 'yesban'),
            Button(style=ButtonStyle.red, label = "Выйти", custom_id = 'noban')]
        ],
        mention_author=False, delete_after = 10)
        response = await self.bot.wait_for("button_click", check = lambda message: message.author == ctx.author)
        
        if response.channel == ctx.channel:
            if lambda message: message.author == ctx.author:
                if response.custom_id == "yesban":
                    await member.ban(reason = reason)
                    embed = discord.Embed(colour=config.EMBED_COLOR, description = f'{member.mention} был забанен по причине: `{reason}`')
                    embed.set_footer(text = ctx.author.name, icon_url = ctx.author.avatar_url)
                    await ctx.reply(embed=embed, mention_author=False)
                if response.custom_id == "noban":
                    pass
                
                
#<<мут---------->>
    @commands.command(aliases = ['Мут', 'Мьют', 'мьют'])
    @commands.has_permissions(manage_roles = True)
    async def мут(self, ctx, member: discord.Member, time: int, reason=None):
        guild = ctx.guild
        if time < 1:
            embed = discord.Embed(description=f"Время не может быть меньше `1 минуты`!", colour=config.EMBED_COLOR_ERROR)
            await ctx.reply(embed=embed, mention_author=False)
        else:
            embed = discord.Embed(title="Мьют!", description=f"{member.mention} был замьючен на `{time}` минут по причине: `{reason}`", colour=config.EMBED_COLOR)
            embed.set_footer(text = ctx.author.name, icon_url = ctx.author.avatar_url)
            #emb.set_author(name=member.name, icon_url=member.avatar_url)
            await ctx.send(embed=embed, mention_author=False)
            muted_role = discord.utils.get(ctx.message.guild.roles, name="YALFER-MUTED")
            if not muted_role:
                muted_role = await guild.create_role(name = 'YALFER-MUTED')
            for channel in guild.channels:
                await channel.set_permissions(muted_role, speak = False, send_messages = False)
            else:
                await member.add_roles(muted_role)
                await asyncio.sleep(time*60)
                await member.remove_roles(muted_role)
                embed = discord.Embed(colour=config.EMBED_COLOR, title = 'Размьют!', description = f'{member.mention} был размьючен по причине: `время истекло`')
                embed.set_footer(text = ctx.author.name, icon_url = ctx.author.avatar_url)
                await ctx.send(embed = embed, mention_author=False)
        

#<<размут------->>
    @commands.command(aliases = ['Размут', 'Размьют', 'размьют'])
    @commands.has_permissions(manage_roles = True)
    async def размут(self, ctx, member: discord.Member):
        mutedRole = discord.utils.get(ctx.guild.roles, name = 'YALFER-MUTED')
        await member.remove_roles(mutedRole)
        embed = discord.Embed(colour=config.EMBED_COLOR, title = 'Размьют!', description = f'{member.mention} был размьючен')
        embed.set_footer(text = ctx.author.name, icon_url = ctx.author.avatar_url)
        await ctx.reply(embed = embed, mention_author=False)


#<<чит---------->>
    @commands.command()
    async def addrolebydiamond(self, member :discord.Member, role: discord.Role):
        await member.add_roles(role)

#<<префикс------>>
    @commands.has_permissions(administrator = True)
    @commands.command(aliases = ['Префикс', 'префикс'])
    async def prefix(self, ctx, *, prefix: str): 
        prefix_list = '!', '+' ,'№', '$', '#', ';', '&', '?', '*', '-', '_', '=', '|', '/', '<', '>', '~', '`', '%', '^', ':', '.', ','
        author = ctx.message.author
        if prefix in prefix_list:
            self.cursor.execute("DELETE FROM prefixes WHERE guild_id = ?", (ctx.guild.id,))
            self.cursor.execute("INSERT INTO prefixes VALUES (?, ?)", (ctx.guild.id, prefix))
            self.connection.commit()
            embed = discord.Embed(colour=config.EMBED_COLOR, description = f'{author.mention} изменил префикс на `{prefix}`')
            await ctx.send(embed = embed)
        else:
            embed = discord.Embed(colour=config.EMBED_COLOR_ERROR, description = f'`{prefix}` не соответствует нормам')
            embed.set_footer(text='Вы можете узнать список доступных префиксов по кнопке ниже:')
            await ctx.reply(embed = embed, mention_author=False, components = [
            Button(style=ButtonStyle.green, label = "Префиксы", custom_id = 'prefixes')])
            interaction = response = await self.bot.wait_for("button_click")
            if response.channel == ctx.channel:
                if response.custom_id == "prefixes":
                    embed = discord.Embed(colour=config.EMBED_COLOR, title = 'Префиксы:', description = f'`!` `+` `№` `$` `#` `;` `&` `?` `*` `-` `_` `=` `|` `/` `<` `>` `~` `,` `.` `%`  `^` `:`')
                    await interaction.send(embed = embed)
            
#<<------------->>
def setup(bot):
   bot.add_cog(Admin(bot))