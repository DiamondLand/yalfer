import discord
import error_send
import sqlite3
import os
import time
from loguru import logger
from discord.ext import commands
from config import config


def get_prefix(client, message):
    cursor.execute("SELECT * FROM prefixes WHERE guild_id = ?", (message.guild.id,))
    result = cursor.fetchone()
    if result is None:
        return "+"
    else:
        return result[1]

bot = commands.Bot(command_prefix=get_prefix, intents=discord.Intents.all())
bot.remove_command('help')
connection = sqlite3.connect("database.db")
cursor = connection.cursor()
bot.logger = logger

for folder in os.listdir("cogs"):
    for file in os.listdir(f"cogs/{folder}"):
        if file.endswith(".py") and file.startswith("COG_"):
            bot.load_extension(f"cogs.{folder}.{file[:-3]}") 
            logger.info(f"import \"D:\Yalfer\Yalfer 3.0\cogs/{folder}/{file}\"")

bot_commands = list(bot.commands)
def leadingZero(time: str):
    if len(time) > 1:
        return time

    return "0" + time

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        command_ = str(error).replace("is not found", "")
        command_ = command_[9:-2]
        return

    if isinstance(error, commands.CommandOnCooldown):
        
        command_ = str(error).replace("You are on cooldown. Try again in", " s")
        command_ = command_[9:-2]
        cd = round(error.retry_after)
        minutes = str(cd // 60)
        seconds = str(cd % 60)
        await error_send.send_what(ctx, 
               f"Вы сможете использовать это через: **{leadingZero(minutes)}** минут, **{leadingZero(seconds)}** секунд!"
        )
        return 
    if isinstance(error, commands.MissingRequiredArgument):
        await error_send.send_what(ctx, 
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
    if str(error) == "Command raised an exception: HTTPException: 400 Bad Request (error code: 50035): Invalid Form Body In message_reference: Unknown message": 
        return 
    if str(error) == "Command raised an exception: NotFound: 404 Not Found (error code: 0): Interaction is unknown (you have already responded to the interaction or responding took too long)": 
        return 
    if str(error) == "Command raised an exception: TypeError: argument of type 'NoneType' is not iterable": 
        return
    if str(error) == "Command raised an exception: SyntaxError: invalid syntax (<string>, line 1)":
        return
    if str(error) == "Command raised an exception: AttributeError: <discord.embeds.Embed object at 0x000001EC2E81A440>":
        return
    if str(error) == "returnCommand raised an exception: AttributeError: 'MiningCog' object has no attribute 'get_prefix'":
        return
    if str(error) == "Command raised an exception: HTTPException: 400 Bad Request (error code: 50035): Invalid Form Body In message_reference: Unknown message":
        return
    if str(error) == "Command raised an exception: TypeError: unsupported operand type(s) for +: 'NoneType' and 'int'":
        return
    if str(error) == "Command raised an exception: HTTPException: 400 Bad Request (error code: 40060): Interaction has already been acknowledged.":
        return
    if str(error) == "Command raised an exception: NotFound: 404 Not Found (error code: 10008): Unknown Message":
        return
    if str(error) == "Command raised an exception: HTTPException: 400 Bad Request (error code: 50035): Invalid Form Body In message_reference: Unknown message":
        return
    if str(error) == "Command raised an exception: OverflowError: Python int too large to convert to SQLite INTEGER":
        await error_send.send_error(ctx, "Слишком большое значение!")  
        return
    if str(error) == "Command raised an exception: HTTPException: 400 Bad Request (error code: 50035): Invalid Form Body\nIn message_reference: Unknown message":
        return 
    if str(error) == "Command raised an exception: HTTPException: 400 Bad Request (error code: 50006): Cannot send an empty message":
        return
        
    emb = discord.Embed(color=config.EMBED_COLOR_ERROR, description = f':no_entry_sign: {error}')
    await ctx.send(embed = emb)

#Запуск-----------------------------------
token = open ('token.txt', 'r').readline()
bot.run(token)