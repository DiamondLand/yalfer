
from selectors import EVENT_READ
import discord
import error_send
import sqlite3
from loguru import logger
from config import config
from discord.ext import commands
from discord_components import DiscordComponents
from rucogs.events.system import EventsCogFunctionality

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.connection = sqlite3.connect("database.db")
        self.cursor = self.connection.cursor()
        self.bot.logger = logger

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

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info(f"Hi, {config.DEVELOPER}!")
        DiscordComponents(self.bot)
        await self.bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.playing, name=f"+хелп || +инвайт"))

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        join_msg = f'👋 Привет-привет! Спасибо за выбор *{config.NAME}*!\
        \n\
        \n**{config.NAME}** - полностью бесплатный и многофункциональный бот, включающий в себя как основные, так и неформальные функции:\
        \n\
        \n• Веселье\
        \n• Экономика\
        \n• Майнинг\
        \n• Музыка\
        \n• Утилиты\
        \n• Модерация\
        \n\
        \nВы можете ознакомиться с ними по команде `+хелп`.'
        to_send = next((
            chan for chan in sorted(guild.channels, key=lambda x: x.position)
            if chan.permissions_for(guild.me).send_messages and isinstance(chan, discord.TextChannel)
        ), None)

        if to_send:
            embed = discord.Embed(color=config.EMBED_COLOR, description = join_msg) 
            await  to_send.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
'''    
    @commands.has_permissions(administrator=True)
    @commands.command(aliases = ['Добавитьроль', 'добавитьроль'])
    async def add_role(self, ctx, role: discord.Role):
        """
        :param ctx:
        :param role:
        :return:
        """
        self.cursor.execute(
            "INSERT INTO server_for_members VALUES(?, ?)",
            (
                ctx.guild.id,
                role.id,
            )
        )
        self.connection.commit()
        emb = discord.Embed(color = config.EMBED_COLOR, title=f'Приветственная роль:', description = f'💖 {role.mention} установлена как роль для новых участников!')
        await ctx.reply(embed = emb, mention_author=False)
    
    @commands.has_permissions(administrator=True)
    @commands.command(aliases = ['Убратьроль', 'убратьроль'])
    async def dell_role(self, ctx, role: discord.Role):
        """
        :param ctx:
        :param role:
        :return:
        """
        self.cursor.execute(
            "DELETE FROM server_for_members WHERE guild_id = ? AND role_id = ?",
            (
                ctx.guild.id,
                role.id,
            )
        )
        self.connection.commit()
        emb = discord.Embed(color = config.EMBED_COLOR, title=f'Приветственная роль:', description = f'💔 {role.mention} больше не является ролью для новых участников!')
        await ctx.reply(embed = emb, mention_author=False)
    
    @commands.command(aliases = ['Роли', 'роли'])
    async def roles(self, ctx):
        """
        :param ctx:
        :return:
        """
        data = EventsCogFunctionality.get_all_items(
            self.cursor,
            ctx.guild
        )
        data.reverse()
        emb = discord.Embed(color = config.EMBED_COLOR, title="Приветственные роли:")
        for item in data:
            emb.add_field(name=f'Роль для приветствий:', value=f"{ctx.guild.get_role(item[1]).mention}", inline=False)
        await ctx.send(embed = emb)
  
    @commands.Cog.listener()
    async def on_member_join(self, guild, member):
        role = item[1]
        data = EventsCogFunctionality.get_all_items(
            self.cursor,
            guild
        )
        for item in data:
            if item[1] == role.id:
                break
        join_member_msg = f'🍧 {member.mention} присоединился к {guild}!\
        \nНа сервере: `{guild.member_count}`\
        \nВыдана роль: {role.mention}'
        to_send = next((
            chan for chan in sorted(guild.channels, key=lambda x: x.position)
            if chan.permissions_for(guild.me).send_messages and isinstance(chan, discord.TextChannel)
        ), None)

        if to_send:
            embed = discord.Embed(color=config.EMBED_COLOR, description = join_member_msg) 
            await  to_send.send(embed=embed)
            await member.add_roles(role)
'''        
#<<------------->>
def setup(bot):
    """
    :param bot:
    :return:
    """
    bot.add_cog(Events(bot))