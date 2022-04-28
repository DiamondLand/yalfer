import discord
import error_send
import sqlite3
import os
from discord.ext import commands
from loguru import logger
from discord_components import DiscordComponents
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
connection = sqlite3.connect("database.db", timeout=10)
cursor = connection.cursor()
bot.logger = logger


@bot.event
async def on_ready():
    logger.info(f"Hi, {config.DEVELOPER}!")
    DiscordComponents(bot)
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
            await  to_send.send(embed=embed)

for folder in os.listdir("cogs"):
    for file in os.listdir(f"cogs/{folder}"):
        if file.endswith(".py") and file.startswith("COG_"):
            bot.load_extension(f"cogs.{folder}.{file[:-3]}") 
            logger.info(f"import \"F:\Yalfer\Yalfer 3.0\cogs/{folder}/{file}\"")

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
    if str(error) == "Command raised an exception: AttributeError: <discord.embeds.Embed object at 0x000001EC2E81A440>":
        return
    if str(error) == "returnCommand raised an exception: AttributeError: 'MiningCog' object has no attribute 'get_prefix'":
        return
    if str(error) == "Command raised an exception: HTTPException: 400 Bad Request (error code: 50035): Invalid Form Body In message_reference: Unknown message":
        return
    if str(error) == "Command raised an exception: TypeError: unsupported operand type(s) for +: 'NoneType' and 'int'":
        return
    if str(error) == "Command raised an exception: NotFound: 404 Not Found (error code: 10008): Unknown Message":
        return
    if str(error) == "Command raised an exception: OverflowError: Python int too large to convert to SQLite INTEGER":
        await error_send.send_error(ctx, "Слишком большое значение!")
        return
    emb = discord.Embed(color=config.EMBED_COLOR_ERROR, description = f':no_entry_sign: {error}')
    await ctx.send(embed = emb)

#Запуск-----------------------------------
token = open ('token.txt', 'r').readline()
bot.run(token)