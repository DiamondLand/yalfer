import discord
import sqlite3
from config import config
from discord.ext import commands
from loguru import logger
from discord_components import DiscordComponents
#<<------------->>

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.connection = sqlite3.connect("database.db", timeout=10)
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
#<<готовность-->> 
    @commands.Cog.listener()
    async def on_ready(self):
        logger.info(f"Hi, {config.DEVELOPER}!")
        DiscordComponents(self.bot)
        await self.bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.playing, name=f"+хелп || +инвайт"))

#<<канал-------->>
    @commands.command(aliases = ['Чат', 'чат'])
    @commands.has_permissions(administrator=True)
    async def set_chat(self, ctx, channel: discord.TextChannel):             
        channel_id = channel.id
        guild_id = ctx.guild.id
        role = config.ROLE
        hi_text = config.HI_TEXT
        bye_text = config.BYE_TEXT
        self.cursor.execute(
            "SELECT * FROM server_for_members WHERE guild_id = ?",
            (
                guild_id,
            )
        )
        result = self.cursor.fetchone()
        if result is None:
            self.cursor.execute(
                "INSERT INTO server_for_members VALUES(?, ?, ?, ?, ?)",
                (
                    guild_id,
                    channel_id,
                    role.id,
                    hi_text,
                    bye_text
                )
            )
            self.connection.commit()
        else:
            self.cursor.execute(
                "UPDATE server_for_members SET channel_id = ? WHERE guild_id = ?",
                (
                    channel_id,
                    guild_id
                )
            )
            self.connection.commit()
            embed = discord.Embed(colour=config.EMBED_COLOR, title=f'Приветственный канал:', description = f'💖 Добавлен чат для приветствий - {channel.mention}!')
            embed.set_footer(text= ctx.author, icon_url = ctx.author.avatar_url) 
            await ctx.reply(embed=embed, mention_author=False)

    @commands.command(aliases = ['удчат', 'Удчат'])
    @commands.has_permissions(administrator=True)
    async def chat_off(self, ctx):
        guild = ctx.guild
        guild_id = guild.id
        self.cursor.execute(
            "DELETE FROM server_for_members WHERE guild_id = ?",
            (
                guild_id,
            )
        )
        self.connection.commit()
        embed = discord.Embed(colour=config.EMBED_COLOR, title=f'Приветственный канал:', description = f'💔 Убран чат для приветствий!')
        embed.set_footer(text= ctx.author, icon_url = ctx.author.avatar_url) 
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(aliases = ['Чатроль', 'чатроль'])
    @commands.has_permissions(administrator=True)
    async def chat_role_off(self, ctx, role: discord.Role):
        channel_id = config.CHANNEL
        guild_id = ctx.guild.id
        hi_text = config.HI_TEXT
        bye_text = config.BYE_TEXT
        self.cursor.execute(
            "INSERT INTO server_for_members VALUES(?, ?, ?, ?, ?)",
            (
                guild_id,
                channel_id,
                role.id,
                hi_text,
                bye_text
            )
        )
        self.connection.commit()
        embed = discord.Embed(colour=config.EMBED_COLOR, title=f'Приветственный канал:', description = f'💖 Установлена роль для новичков - {role.mention}!')
        embed.set_footer(text= ctx.author, icon_url = ctx.author.avatar_url) 
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(aliases = ['Удчатроль', 'удчатроль'])
    @commands.has_permissions(administrator=True)
    async def chat_off(self, ctx, role: discord.Role):
        self.cursor.execute(
            "DELETE FROM server_for_members WHERE guild_id = ? AND role_id = ?",
            (
                ctx.guild.id,
                role.id,
            )
        )
        self.connection.commit()
        embed = discord.Embed(colour=config.EMBED_COLOR, title=f'Приветственный канал:', description = f'💔 Убрана роль для новичков - {role.mention}!')
        embed.set_footer(text= ctx.author, icon_url = ctx.author.avatar_url) 
        await ctx.reply(embed=embed, mention_author=False)

#<<------------->>
def setup(bot):
   bot.add_cog(Events(bot))