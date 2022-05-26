import discord
from config import config

async def send_error(context, error):
    embed = discord.Embed(description = f":no_entry_sign: {error}", color=config.EMBED_COLOR_ERROR)
    await context.reply(embed = embed, mention_author=False)