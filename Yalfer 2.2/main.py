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
from collections.abc import Sequence

connection = sqlite3.connect("database.db")
cursor = connection.cursor()


def get_prefix(bot, message):
    cursor.execute(
        "SELECT * FROM prefixes WHERE guild_id = ?", 
        (
            message.guild.id,
        )
    )
    result = cursor.fetchone()
    if result is not None:
        return result[1]
    else:
        return "+"

bot = commands.Bot(command_prefix = get_prefix)
bot.remove_command("help")


@bot.event
async def on_ready():
    logger.info(f"Hi, {config.DEVELOPER}!")
    guilds = await bot.fetch_guilds(limit = None).flatten()
    await bot.change_presence(status = discord.Status.online, activity = discord.Activity(name=f'команды в +хелп', type= discord.ActivityType.watching))

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
            logger.info(f"import \"F:\Yalfer\Yalfer 2.1\cogs/{folder}/{file}\"")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await error_send.send_error(ctx, 
                "Отсутствует обязательный аргумент: " + f"({str(error).split()[0]})"
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
                "Отсутствуют разрешения у участника или бота!"
        )
        return
    if str(error) == "Command raised an exception: Forbidden: 403 Forbidden (error code: 50013): Missing Permissions":
        await error_send.send_error(ctx, 
            "Отсутствуют разрешения у участника или бота!"
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
    if str(error) == "Command raised an exception: SyntaxError: invalid syntax (<string>, line 1)":
        return
    if str(error) == "Command raised an exception: SyntaxError: unexpected EOF while parsing (<string>, line 0)":
        return
    if str(error) == "returnCommand raised an exception: AttributeError: 'MiningCog' object has no attribute 'get_prefix'":
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



#Запуск-----------------------------------
token = open ('token.txt', 'r').readline()
bot.run(token)