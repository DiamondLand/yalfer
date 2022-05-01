import error_send
import discord
import random
import sqlite3
from config import config
from discord.ext import commands
from discord_components import DiscordComponents, Button, ButtonStyle, Select, SelectOption

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
    
    #орёл или решка----------------------------------------
    @commands.command(aliases=['Монетка', 'монетка', 'Монета', 'монета', 'Орёл', 'орёл', 'Орел', 'орел', 'Решка', 'решка'])
    async def cointoss(self, ctx):
        await ctx.channel.purge(limit=1)
        while True:
            choice = random.randint(1, 2)
            author = ctx.author
            await ctx.send(embed = discord.Embed(color=config.EMBED_COLOR, description = f"{author.mention}, что ты выберешь?"),
            components = [
                [Button(style=ButtonStyle.blue, label = "Решка", emoji='🪙', custom_id = 'reshka'),
                Button(style=ButtonStyle.green, label = "Орёл", emoji='🦅', custom_id = 'orel')]
            ],
            mention_author=False, delete_after = 8)
        
            interaction = response = await self.bot.wait_for("button_click")
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

        
    #судьба------------------------------------------------
    @commands.command(aliases = ['Судьба', 'судьба'])
    async def fate(self, ctx, *, text):
        variable = ['Даааа! :innocent:', 'Ага щас :face_with_monocle: ', '100%', 'Нет и ещё раз нет! :no_entry_sign: ', 'Ты что?\nНЕТ! :four_leaf_clover: ', 'Не хочу тебя огорчать... :eyes: ', 'Как бы сказать помягче...\n||ДА!|| :heart_eyes:', 'Скорее нет, чем да :wave:', 'Маловероятно :moyai: ', 'Может быть :gem: ', 'Так и будет :heart_on_fire: ', 'А зачем это тебе?  :eggplant: ' ]
        emb = discord.Embed(color=config.EMBED_COLOR, description = '{}'.format(random.choice(variable)))
        await ctx.reply(embed=emb, mention_author=False)

    #дуэль-------------------------------------------------
    @commands.command(aliases = ['Дуэль', 'дуэль', 'Дуель', 'дуель'])
    async def duel(self, ctx, member: discord.Member):
        if member == ctx.author:
            return await ctx.send(embed=discord.Embed(description="Играть самим с собой не получится!", colour=config.EMBED_COLOR_ERROR))
        if member:
            await ctx.send(embed=discord.Embed(description=f"У нас есть два соперника:\n\n1. `{ctx.author}`\n2. `{member}`", colour=config.EMBED_COLOR),
            components = [
            Select(
                placeholder = "Выбери оружие:",
                options = [
                    SelectOption(label = "Desert Eagle", value = "Desert Eagle"),
                    SelectOption(label = "Mauser HSc", value = "Mauser HSc"),
                    SelectOption(label = "Glock 18", value = "Glock 18"),
                    SelectOption(label = "Five-seveN", value = "Five-seveN")
                ]
            )
        ],
        delete_after = 10)

        variable = [f'`{member}` потерпел поражение и был застрелен\n`{ctx.author}` остался в живых!',
        f'`{ctx.author}` был застрелен...\n`{member}` остался в живых!']    
        await self.bot.wait_for("select_option")
        emb = discord.Embed(color=config.EMBED_COLOR_ERROR, title=':cherry_blossom: Итоги поединка:', description = '{}'.format(random.choice(variable)))
        await ctx.send(embed = emb)

    #респект-------------------------------------------------
    @commands.command(aliases = ['Ф', 'ф', 'Респект', 'респект', 'Риспект', 'риспект'])
    async def f(self, ctx, *, text = None):
        await ctx.channel.purge(limit = 1)
        hearts = ["❤", "💛", "💚", "💙", "💜"]
        reason = f"{text} " if text else""
        emb = discord.Embed(color=config.EMBED_COLOR, description = f"{ctx.author.mention} респектнул {reason} {random.choice(hearts)}")
        await ctx.send(embed=emb)

    #краш-------------------------------------------------
    @commands.command(aliases=["Краш", "краш"])
    async def hotcalc(self, ctx, *, user: discord.Member):
        user = user or ctx.author

        r = random.randint(1, 100)
        hot = r / 1.17

        if hot > 70:
            emoji = "💞"
        elif hot > 50:
            emoji = "💖"
        elif hot > 25:
            emoji = "❤"
        else:
            emoji = "💔"

        emb = discord.Embed(color=config.EMBED_COLOR, description = f"{user.mention} краш на `{hot:.2f}`% {emoji}!")
        await ctx.reply(embed=emb, mention_author=False)

            

#Cog-----------------------------------------------------
def setup(bot):
   bot.add_cog(Fun(bot))