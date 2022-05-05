import error_send
import discord
import random
import sqlite3
import asyncio
from config import config
from discord.ext import commands
from discord_components import DiscordComponents, Button, ButtonStyle, Select, SelectOption
#<<------------->>
class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.connection = sqlite3.connect("database.db")
        self.cursor = self.connection.cursor()

    def get_prefix(self, cursor, message):
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
#<<респект----->>
    @commands.command(aliases = ['Респект'])
    async def респект(self, ctx, *, text = None):
        hearts = ["❤", "💛", "💚", "💙", "💜"]
        reason = f"{text} " if text else""
        emb = discord.Embed(color=config.EMBED_COLOR, title = 'Уважение!', description = f"{ctx.author.mention} респектнул *{reason}* {random.choice(hearts)}")
        await ctx.reply(embed=emb, mention_author=False)

#<<дуэль------->>
    @commands.command(aliases = ['Дуэль', 'Дуель', 'дуель'])
    async def дуэль(self, ctx, member: discord.Member):
        if member == ctx.author:
            emb = discord.Embed(description="Сражаться самим собой не получится!", colour=config.EMBED_COLOR_ERROR)
            return await ctx.reply(embed=emb, mention_author=False)
        if member:
            emb = discord.Embed(description=f"У нас есть два соперника:\n1. `{ctx.author}`\n2. `{member}`", colour=config.EMBED_COLOR)
            emb.set_footer(text=f'Выбирает оружие: {ctx.author}. У него 10 секунд на поединок!', icon_url = ctx.author.avatar_url)
            await ctx.send(embed = emb,
            components = [
                [Button(style=ButtonStyle.blue, label = "Desert Eagle", emoji='💥', custom_id = 'desert_eagle'),
                Button(style=ButtonStyle.green, label = "Mauser", emoji='🔫', custom_id = 'mauser')]
            ], delete_after=10),
            while True:
                variable = [f'`{member}` потерпел поражение\n`{ctx.author}` остался в живых!',
                f'`{ctx.author}` был застрелен...\n`{member}` остался в живых!',
                f'`{member}` убежал с поля боя!\nДуэли не будет!',
                f'У `{member}` осечка!\n`{ctx.author}` остался в живых!',
                f'У `{ctx.author}` осечка!\n`{member}` остался в живых!']    
                interaction = response = await self.bot.wait_for("button_click", check = lambda message: message.author == ctx.author)
                if response.channel == ctx.channel:
                    if lambda message: message.author == ctx.author:
                        emb = discord.Embed(color=config.EMBED_COLOR, title=':cherry_blossom: Итоги поединка:', description = '{}'.format(random.choice(variable)))
                        emb.set_footer(text=f'Выбирает оружие: {ctx.author}', icon_url = ctx.author.avatar_url)
                        emb.set_thumbnail(url=member.avatar_url)
                        await ctx.send(embed = emb, delete_after=15)
                    else: 
                        interaction = emb = discord.Embed(color=config.EMBED_COLOR_ERROR, description = f"Вы не являетесь человеком, запросившем данную команду")
                        await interaction.ctx.reply(embed=emb, mention_author=False)

#<<краш--------->>
    @commands.command(aliases=['Краш', 'Лузер', 'лузер'])
    async def краш(self, ctx, *, user: discord.Member):
        user = user or ctx.author
        r = random.randint(1, 100)
        k = random.randint(1, 5)
        j = random.randint(1, 5)
        hot = r / k
        lus = r / j

        if hot > 70:
            emoji_love = "💞"
        elif hot > 50:
            emoji_love = "💖"
        elif hot > 25:
            emoji_love = "❤"
        else:
            emoji_love = "💔"
        
        if lus > 70:
            emoji_hate = "🤮"
        elif lus > 50:
            emoji_hate = "🙄"
        elif lus > 25:
            emoji_hate = "🎭"
        else:
            emoji_hate = "🩸"

        emb = discord.Embed(color=config.EMBED_COLOR, title=f'{user}:', description = f'Краш на `{hot:.2f}`% {emoji_love}!\
        \nЛузер на `{lus:.2f}`% {emoji_hate}!')
        emb.set_thumbnail(url=user.avatar_url)
        await ctx.reply(embed=emb, mention_author=False)

#<<судьба------->>
    @commands.command(aliases = ['Судьба'])
    async def судьба(self, ctx, *, text):
        variable = ['Даааа! :innocent:', 
        'Ага щас :face_with_monocle: ', '100%', 
        'Нет и ещё раз нет! :no_entry_sign: ', 
        'Ты что?\nНЕТ! :four_leaf_clover: ', 
        'Не хочу тебя огорчать... :eyes: ', 
        'Хо-хо-хо. YES :heart_eyes:', 
        'Скорее нет, чем да :wave:', 
        'Маловероятно :moyai: ', 
        'Может быть :gem: ', 
        'Так и будет :heart_on_fire: ', 
        'А зачем это тебе?  :eggplant: ']
        await ctx.reply('{}'.format(random.choice(variable)), mention_author=False)

#<<монетка------>>
    @commands.command(aliases=['Монетка', 'Монета', 'монета', 'Орёл', 'орёл', 'Орел', 'орел', 'Решка', 'решка'])
    async def монетка(self, ctx):
        while True:
            choice = random.randint(1, 2)
            author = ctx.author
            await ctx.send(embed = discord.Embed(color=config.EMBED_COLOR, description = f"{author.mention}, что ты выберешь?"),
            components = [
                [Button(style=ButtonStyle.blue, label = "Решка", emoji='🪙', custom_id = 'reshka'),
                Button(style=ButtonStyle.green, label = "Орёл", emoji='🦅', custom_id = 'orel')]
            ],
            mention_author=False, delete_after = 5)
        
            interaction = response = await self.bot.wait_for("button_click", check = lambda message: message.author == ctx.author)
            if response.channel == ctx.channel:
                if response.custom_id == "orel":
                    if choice == 1:
                        await interaction.send(':revolving_hearts: Ты угадал!\nМогучий `орёл` проглядывается на монетке!')
                    else:
                        await interaction.send(':pensive: Поражение...\nВеликолепная `решка` виднеется на монетке!')
                if response.custom_id == "reshka":
                    if choice == 1:
                        await interaction.send(':pensive: Поражение...\nМогучий `орёл` проглядывается на монетке!')
                    else:
                        await interaction.send(':revolving_hearts: Ты угадал!\nВеликолепная `решка` виднеется на монетке!')
#<<------------->>
def setup(bot):
   bot.add_cog(Fun(bot))            