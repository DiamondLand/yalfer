from fuzzywuzzy import fuzz
import error_send
import discord
import sqlite3
from discord.ext import commands
from pymongo import MongoClient
import os
from loguru import logger

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
    logger.info("Discord.bot.guilds are ready!")
    await bot.change_presence(activity=discord.Game(name="базовый префикс +"))


for folder in os.listdir("cogs"):
    for file in os.listdir(f"cogs/{folder}"):
        if file.endswith(".py") and file.startswith("COG_"):
            bot.load_extension(f"cogs.{folder}.{file[:-3]}") 
            logger.info(f"import \"D:\Bots\Discord\Yalfer 1.1\cogs/{folder}/{file}\"")


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
    if isinstance(error, commands.BotMissingPermissions):
        await error_send.send_error(ctx, 
                "Извините, мне не хватает разрешений :(!"
        )
        return
    if isinstance(error, commands.MissingPermissions):
        await error_send.send_error(ctx, 
                "Отсутствуют разрешения!"
        )
        return
    if str(error) == "Command raised an exception: Forbidden: 403 Forbidden (error code: 50013): Missing Permissions":
        await error_send.send_error(ctx, 
            "Отсутствуют разрешения!"
        )
        return
    if str(error) == "Command raised an exception: AttributeError: 'NoneType' object has no attribute 'channel'":
        await error_send.send_error(ctx, "Вы не в голосовом канале!")
        return
    emb = discord.Embed(colour = discord.Color.red(), title = 'Ошибка!', description = f'{error}')
    await ctx.send(embed = emb)

#Запуск-----------------------------------
token = open ('token.txt', 'r').readline()
bot.run(token)