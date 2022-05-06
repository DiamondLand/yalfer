import discord
from config import config

async def send_error(context, error):
    embed = discord.Embed(colour=config.EMBED_COLOR_ERROR, description = f'❌ {error}')
    await context.reply(embed = embed, mention_author=False)