import discord

async def send_error(context, error):
    embed = discord.Embed(title = 'Ошибка!', description = f":no_entry_sign: {error}", color = discord.Color.red())
    await context.send(embed = embed)