import discord
from config import config

async def send_error(context, error):
    embed = discord.Embed(colour=config.EMBED_COLOR, title='Произошла ошибка!', description = f':no_entry_sign: {error}')
    embed.set_footer(text=f"❓ Вам следует обратиться к Diamond#7941")
    await context.reply(embed = embed, mention_author=False)