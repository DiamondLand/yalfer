from importlib.resources import contents
import discord
import error_send
import sqlite3
import os
import json
from loguru import logger
from config import config
from discord.ext import commands
from discord_components import DiscordComponents

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
        \n• Кастомные команды\
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

        server_id = message.guild
        file_path = f"custom/{server_id}.json"
        if not os.path.exists(file_path):
            my_file = open(f"custom/{server_id}.json", "w+", encoding='utf-8')
            my_file.write("{}")
            my_file.close()
        else:
            pass

        file_path = f"warnings/{server_id}.json"
        if not os.path.exists(file_path):
            my_file = open(f"warnings/{server_id}.json", "w+", encoding='utf-8')
            my_file.write("{}")
            my_file.close()
        else:
            pass
        
        with open(f'custom/{server_id}.json', 'r') as json_file:
            castom_commands = json.load(json_file)

        if castom_commands and (message.content[1:] in castom_commands.keys()):
            embed=discord.Embed(color=config.EMBED_COLOR, description=castom_commands[message.content[1:]])
            await message.reply(embed=embed, mention_author=False)
            return

        
#<<------------->>
def setup(bot):
    bot.add_cog(Events(bot))