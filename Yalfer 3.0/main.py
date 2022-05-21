import discord
import error_send
import sqlite3
import os
from loguru import logger
from discord_components import DiscordComponents
from discord.ext import commands
from config import errors
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

for folder in os.listdir("rucogs"):
    for file in os.listdir(f"rucogs/{folder}"):
        if file.endswith(".py") and file.startswith("COG_"):
            bot.load_extension(f"rucogs.{folder}.{file[:-3]}") 
            logger.info(f"import \"Yalfer 3.0/rucogs/{folder}/{file}\"")

bot_commands = list(bot.commands)
def leadingZero(time: str):
    if len(time) > 1:
        return time

    return "0" + time

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
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
                "Вы указали слишком много аргументов!"
        )
        return
    if isinstance(error, commands.MemberNotFound):
        await error_send.send_error(ctx, 
            "Пользователь не найден!"
        )
        return
    if isinstance(error, commands.BadArgument):
        await error_send.send_error(ctx, 
                "Вы указали неверный аргумент!"
        )
        return
    if isinstance(error, commands.MissingPermissions):
        await error_send.send_error(ctx, 
                "У Вас отсутствуют требуемые разрешения!"
        )
        return
    if str(error) == "Command raised an exception: Forbidden: 403 Forbidden (error code: 50013): Missing Permissions":
        await error_send.send_error(ctx, 
            "У Вас отсутствуют требуемые разрешения!"
        )
        return
    if str(error) in errors.PROCESS_ERROR:
        return
    if str(error) not in errors.PROCESS_ERROR:
        return
        
    emb = discord.Embed(color=config.EMBED_COLOR_ERROR, title = '❌ Ошибка:', description = f'{error}')
    await ctx.send(embed = emb)

#Запуск-----------------------------------
token = open ('token.txt', 'r').readline()
bot.run(token)