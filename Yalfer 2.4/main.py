import error_send
import discord
import re
import sqlite3
import os
import json
import time
import random
from discord.ext import commands
from pymongo import MongoClient
from loguru import logger
from config import config

#logger.add("logs/log_{time}.log", format="{level} -> {message} at {time}", level="INFO", rotation="2 MB",compression="zip")


def get_prefix(client, message):
    cursor.execute("SELECT * FROM prefixes WHERE guild_id = ?", (message.guild.id,))
    result = cursor.fetchone()
    if result is None:
        return "+"
    else:
        return result[1]

bot = commands.Bot(command_prefix=get_prefix)
bot.remove_command('help')
connection = sqlite3.connect("database.db", timeout=10)
cursor = connection.cursor()
bot.logger = logger


@bot.event
async def on_ready():
    logger.info(f"Hi, {config.DEVELOPER}!")
    await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.playing, name=f"+хелп || +инвайт"))

@bot.command
async def guilds(ctx):
    await ctx.send("\n".join(bot.guilds))


@bot.event
async def on_guild_join(guild):
        to_send = next((
            chan for chan in sorted(guild.channels, key=lambda x: x.position)
            if chan.permissions_for(guild.me).send_messages and isinstance(chan, discord.TextChannel)
        ), None)

        if to_send:
            embed = discord.Embed(color=config.EMBED_COLOR, description = config.JOIN_MSG) 
            embed.set_image(url = 'https://i.yapx.ru/Qa220.png')
            await  to_send.send(embed=embed)

for folder in os.listdir("cogs"):
    for file in os.listdir(f"cogs/{folder}"):
        if file.endswith(".py") and file.startswith("COG_"):
            bot.load_extension(f"cogs.{folder}.{file[:-3]}") 
            logger.info(f"import \"F:\Yalfer\Yalfer 2.4\cogs/{folder}/{file}\"")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await error_send.send_error(ctx, 
                "Отсутствует обязательный аргумент: " + f"`{str(error).split()[0]}`"
        )
        return
    if isinstance(error, commands.TooManyArguments):
        await error_send.send_error(ctx, 
                "Слишком много аргументов!"
        )
        return
    if isinstance(error, commands.MemberNotFound):
        await error_send.send_error(ctx, 
            "Пользователь не найден!"
        )
        return
    if isinstance(error, commands.BadArgument):
        await error_send.send_error(ctx, 
                "Неверный аргумент!"
        )
        return
    if isinstance(error, commands.MissingPermissions):
        await error_send.send_error(ctx, 
                "У вас отсутствуют требуемые разрешения"
        )
        return
    if str(error) == "Command raised an exception: Forbidden: 403 Forbidden (error code: 50013): Missing Permissions":
        await error_send.send_error(ctx, 
            "У вас отсутствуют требуемые разрешения!"
        )
        return
    if str(error) == "Command raised an exception: AttributeError: 'NoneType' object has no attribute 'channel'":
        await error_send.send_error(ctx, "Вы не в голосовом канале!")
        return
    if str(error) == "Command raised an exception: TypeError: 'NoneType' object is not subscriptable":
        await error_send.send_error(ctx, "Не найдено. Повторите попытку")
        return
    if str(error) == "Command raised an exception: SyntaxError: unexpected EOF while parsing (<string>, line 1)": 
        return 
    if str(error) == "Command raised an exception: AttributeError: 'MiningCog' object has no attribute 'conn'": 
        return
    if str(error) == "Command raised an exception: SyntaxError: invalid syntax (<string>, line 1)":
        return
    if str(error) == "Command raised an exception: SyntaxError: unexpected EOF while parsing (<string>, line 0)":
        return
    if str(error) == "returnCommand raised an exception: AttributeError: 'MiningCog' object has no attribute 'get_prefix'":
        return
    if str(error) == "Command raised an exception: FileNotFoundError: [Errno 2] No such file or directory: '.\assets\videocards.png'":
        return
    if str(error) == "Command raised an exception: TypeError: unsupported operand type(s) for +: 'NoneType' and 'int'":
        return
    if str(error) == "Command raised an exception: NotFound: 404 Not Found (error code: 10008): Unknown Message":
        return
    if str(error) == "Command raised an exception: AttributeError: 'NoneType' object has no attribute 'is_paused'":
        return
    if str(error) == "Command raised an exception: TypeError: expected string or bytes-like object":
        return
    if str(error) == "Command raised an exception: OverflowError: Python int too large to convert to SQLite INTEGER":
        await error_send.send_error(ctx, "Слишком большое значение!")
        return
    emb = discord.Embed(color=config.EMBED_COLOR_ERROR, description = f':no_entry_sign: {error}')
    await ctx.reply(embed = emb)

'''
@bot.event
async def on_message(msg):
    if msg.author == bot.user:
        return
    guild_id = msg.guild.id
    prefix = get_prefix(bot, msg)
    test = config.TEST
    cursor.execute(
        "SELECT * FROM log_channel WHERE guild_id = ?",
        (
            guild_id,
        )
    )
    result = cursor.fetchone()
    guild_id = msg.guild.id
    prefix = get_prefix(bot, msg)
    cursor.execute(
        "SELECT * FROM log_channel WHERE guild_id = ?",
        (
            guild_id,
        )
    )

    result = cursor.fetchone()
    amount_of_big_letters = 0
    REGEX_EN = re.compile(r"[A-Z]")
    REGEX_RU = re.compile(r"[А-Я]")
    amount_of_big_letters += len(REGEX_EN.findall(msg.content))
    amount_of_big_letters += len(REGEX_RU.findall(msg.content))
    if amount_of_big_letters > 5 and msg.author != bot.user:
        if result is not None:
            channel = discord.utils.get(msg.guild.channels, id=int(result[1]))
            embed = discord.Embed(title=f":no_entry: Caps Lock!", color=config.EMBED_COLOR_LOG, description=f"{msg.author.mention} использовал очень много капса:", inline = False)
            embed.add_field(name= f"Сообщение: `{msg.content}`", value=f"Количество больших букв: `{amount_of_big_letters}`\nКанал: `#{msg.channel.name}`")
            embed.add_field(name= f"ID сообщения: `{msg.id}`", value=f"Ссылка: {msg.jump_url}", inline = False)
            embed.set_thumbnail(
                url=msg.author.avatar_url
            )
            try:
                await channel.send(embed=embed)
            except:
                embed = discord.Embed(title=f":no_entry: Логи выключены!", color=config.EMBED_COLOR_ERROR, description=f"Администрация может включить систему логирования по команде {prefix}лог <#канал>")
                await msg.channel.send(embed=embed)   
'''

#Запуск-----------------------------------
token = open ('token.txt', 'r').readline()
bot.run(token)