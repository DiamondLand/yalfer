import discord
from config import config

async def send_error(context, error):
    embed = discord.Embed(colour=config.EMBED_COLOR_ERROR, description = f'❌ {error}')
    await context.reply(embed = embed, mention_author=False) 

async def send_what(context, what):
    embed = discord.Embed(colour=config.EMBED_COLOR_WHAT, title='💛 Нет, нет, нет!', description = f'{what}')
    await context.reply(embed = embed, mention_author=False)